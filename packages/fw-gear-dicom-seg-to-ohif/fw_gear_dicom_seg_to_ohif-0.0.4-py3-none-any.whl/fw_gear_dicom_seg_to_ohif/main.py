"""Main module."""

import logging

from fw_gear_dicom_seg_to_ohif.creator import Creator
from fw_gear_dicom_seg_to_ohif.prepper import Prepper

log = logging.getLogger(__name__)


def run(gear_args: dict) -> int:
    """Initializes the needed components and runs.

    Args:
        gear_args: Arguments needed for the gear to run as configured:
            * dicom_seg_path: Path to dicom_seg file
            * source_dicom_path: Path to source_dicom file
            * source_dicom_file_id: 24 char BSON id of source_dicom on Flywheel instance
            * task_id: 24 char BSON id or None if new task to be created
            * protocol_id: Protocol to be used if creating a new task, else None
            * annotation_description: Text to populate annotation description
            * if_annotations_exist: Behavior if task_id is specified and annotations exist
            * assignee: If creating a new task, the Flywheel user the task is to be assigned
            * work_dir: Path to work directory
            * fw: FWClient instance, logged in with api-key

    Returns:
        int: Exit code, 0 if success
    """
    prep = Prepper(
        work_dir=gear_args["work_dir"],
        dicom_seg_path=gear_args["dicom_seg_path"],
        source_dicom_path=gear_args["source_dicom_path"],
    )

    create = Creator(
        prepper=prep,
        task_id=gear_args["task_id"],
        protocol_id=gear_args["protocol_id"],
        source_dicom_file_id=gear_args["source_dicom_file_id"],
        annotation_description=gear_args["annotation_description"],
        if_annotations_exist=gear_args["if_annotations_exist"],
        assignee=gear_args["assignee"],
        fw=gear_args["fw"],
    )

    create.process_segments()

    return 0
