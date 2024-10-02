"""Collectors - Process 2 of 4.

These are designed to pull ROI information from Flywheel for the input file,
utilizing the API to collect all supported ROIs (currently Rectangle, Ellipse, Freehand),
sort by task_id (24 char BSON if ROI was created via task, None if non-task),
and store the curated metadata for further processing.

Responsibilities:
1. Call /api/annotations, filtered by input file
2. Sort all collected annotations by task_id and measurement type
3. Store curated metadata for use by other worker classes

Full process:
1. Prep
2. Collect
3. Create
4. Convert

"""

import logging
import os
import typing as t
from abc import ABC
from requests.exceptions import ConnectionError, HTTPError

from fw_client import FWClient

from fw_gear_mask_exporter.objects.Files import FileObject

log = logging.getLogger(__name__)


class BaseCollector(ABC):
    """Class to gather and store ROI data from a file.

    Raises:
        Exception: If file type is not supported
    """

    # Type key set on each base class to identify which class to instantiate
    type_ = None

    def __init__(
        self,
        file_object: FileObject,
        orig_dir: os.PathLike,
        output_dir: os.PathLike,
        fw: FWClient,
        scope: str,
        completed_task_only: bool,
        all_file_versions: bool,
    ):
        """Initializes the BaseCollector to gather ROIs

        Args:
            file_object: File of which to collect ROIs
            orig_dir: From prepper.orig_dir
            output_dir: Directory in which outputs will be placed
            fw: Flywheel client, logged in with api-key
            scope: annotations scope, task, non-task, both
            completed_task_only: If true, only collect task ROIs from completed tasks
            all_file_versions: Whether to save ROIs found on all file versions instead of latest, default False
        """
        self.orig_dir = orig_dir
        self.file_object = file_object
        self.validROIs = [
            "RectangleRoi",
            "EllipticalRoi",
            "FreehandRoi",
            "CircleRoi",
            "ContourRoi",
        ]
        self.output_dir = output_dir
        self.fw = fw
        self.scope = scope
        self.completed_task_only = completed_task_only
        self.all_file_versions = all_file_versions

        self.annotations_by_task = {}
        self.get_annotations_by_task()
        self.all_task_ids = self.annotations_by_task.keys()

        self.roi_info = {
            task_id: {k: [] for k in self.validROIs} for task_id in self.all_task_ids
        }

    def get_annotations_by_task(self):
        # Getting file ID and version
        input_file_id = self.file_object.flywheel_file["file_id"]
        if self.all_file_versions:
            log.info(
                "Target input file id %s, all versions.",
                input_file_id,
            )
            # Retrieve all annotations regardless of version
            filter_params = "file_ref.file_id=" + str(input_file_id)
        else:
            input_file_version = self.file_object.flywheel_file["version"]
            log.info(
                "Target input file_id %s, version %s.",
                input_file_id,
                input_file_version,
            )
            # Retreiving all annotations matching file ID and version
            filter_params = (
                "file_ref.file_id="
                + str(input_file_id)
                + ",file_ref.version="
                + str(input_file_version)
            )

        try:
            # If there are a lot of annotations to collect, this may time out.
            all_file_annotations = self.fw.get(
                "/api/annotations", params={"filter": filter_params}
            )
        except (ConnectionError, HTTPError) as e:
            log.exception(
                "Annotation collection unsuccessful. If there are many annotations "
                "attached to the input file, read-timeout configuration may need to "
                f"be increased. Current read-timeout is set at {self.fw.timeout[1]}. "
                f"Exiting.\n{e}"
            )
            os.sys.exit(1)
        except Exception as e:
            log.exception(f"Annotation collection unsuccessful. Exiting.\n{e}")
            os.sys.exit(1)

        for a in all_file_annotations.results:
            file_id = a["task_id"]
            # "task_id" property is null (json) if not associated with a task,
            # or 24 char BSON id for associated task
            # json null is converted to None on load for Python use.
            if not self.check_valid_read_task(file_id):
                # Do not store result if check returns False
                pass
            elif (self.scope == "task" and not file_id) or (
                self.scope == "non-task" and file_id
            ):
                # As configured, these do not need to be stored.
                pass
            else:
                if file_id not in self.annotations_by_task.keys():
                    self.annotations_by_task[file_id] = [a]
                else:
                    self.annotations_by_task[file_id].append(a)

        # Log findings
        log.info(
            "%s total annotations found, %s task_ids with annotations within scope '%s'.",
            len(all_file_annotations.results),
            len(self.annotations_by_task.keys()),
            self.scope,
        )

    def collect(self):
        """Collects ROIs by by iterating through all_task_ids."""
        for task_id in self.all_task_ids:
            self.get_valid_ROIs_by_task(task_id)

    def get_valid_ROIs_by_task(self, task_id: t.Optional[str]) -> bool:
        # Annotations associated with specific task
        task_annotations = self.annotations_by_task[task_id]
        if len(task_annotations) == 0:
            error_message = (
                "Input File "
                + str(self.file_object.base_name)
                + " has no associated annotations."
            )
            log.warning(error_message)
            return False

        else:
            for ann in task_annotations:
                measurement_type = ann["data"]["toolType"]

                # Ensure this is an ROI type we can use
                if measurement_type not in self.validROIs:
                    log.info("Measurement type %s invalid, skipping", measurement_type)
                else:
                    self.roi_info[task_id][measurement_type].append(ann["data"])

        return True

    def check_valid_read_task(self, task_id: t.Optional[str]) -> bool:
        """Checks whether a returned annotation has a non-null task_id, and
        if so, verifies that the task_id corresponds to a valid read task.
        If completed_task_only == True, also checks for task status.

        Args:
            task_id: 24 char BSON id or None if not associated with read task

        Returns:
            bool: True if task_id is None, or if task_id refers to a valid read task.
            False if task_id refers to an invalid or deleted read task, or if
            completed_task_only==True and task status is not completed.
        """
        if not task_id:
            # Annotation is not connected to a read task
            return True
        else:
            try:
                read_task = self.fw.get(f"/api/readertasks/{task_id}")
                if not self.completed_task_only:
                    # Read task valid, in progress tasks okay
                    return True
                else:
                    if read_task["status"] == "Complete":
                        # Read task valid, task complete
                        return True
                    else:
                        # Read task valid, task incomplete
                        log.info(
                            "Annotation found connected to incomplete task_id %s, skipping.",
                            task_id,
                        )
                        return False
            except:  # noqa: E722
                # API call raised error
                # task_id is not connected to a valid read task
                log.info(
                    "Annotation found with invalid or deleted task_id %s, skipping.",
                    task_id,
                )
                return False

    @classmethod
    def factory(
        cls,
        type_: str,
        file_object: FileObject,
        orig_dir: os.PathLike,
        output_dir: os.PathLike,
        fw: FWClient,
        scope: str,
        completed_task_only: bool,
        all_file_versions: bool,
    ):
        """Return an instantiated Collector."""
        for sub in cls.__subclasses__():
            if type_.lower() == sub.type_:
                return sub(
                    file_object,
                    orig_dir,
                    output_dir,
                    fw,
                    scope,
                    completed_task_only,
                    all_file_versions,
                )
        # If no type_ matches a sub.type_, log exception and exit.
        log.exception("File type %s not supported.", type_)
        os.sys.exit(1)


class DicomRoiCollector(BaseCollector):
    """ROI Collector for DICOM files."""

    type_ = "dicom"


class NiftiRoiCollector(BaseCollector):
    """ROI collector for NIfTI files"""

    type_ = "nifti"
