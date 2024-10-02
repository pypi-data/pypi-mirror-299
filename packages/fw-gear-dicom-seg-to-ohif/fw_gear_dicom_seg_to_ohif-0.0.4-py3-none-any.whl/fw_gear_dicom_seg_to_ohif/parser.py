"""Parser module to parse gear config.json."""

import logging
import os
from pathlib import Path
from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext
from fw_client import FWClient

from fw_gear_dicom_seg_to_ohif.fw_utils import dynamic_search

log = logging.getLogger(__name__)


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[bool, dict]:
    """Parses context's config.json file to be used by the gear.

    Args:
        gear_context: to provide configuration information

    Returns:
        debug: Debug configuration, default False
        gear_args: Arguments needed for the gear to run as configured, including
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

    """
    debug = gear_context.config.get("debug")
    gear_args = {
        "dicom_seg_path": Path(gear_context.get_input_path("dicom_seg")),
        "task_id": gear_context.config.get("task_id"),
        "protocol_id": gear_context.config.get("protocol_id"),
        "annotation_description": gear_context.config.get("annotation_description"),
        "if_annotations_exist": gear_context.config.get("if_annotations_exist"),
        "assignee": gear_context.config.get("assignee"),
        "work_dir": Path(gear_context.work_dir),
    }

    if gear_args["task_id"] and gear_args["protocol_id"]:
        log.info(
            "Both task_id and protocol_id inputted. Task referred to by task_id "
            "will be used to store annotations; protocol_id will be ignored."
        )
    elif not gear_args["task_id"] and not gear_args["protocol_id"]:
        log.error(
            "Either task_id or protocol_id must be inputted so that the OHIF "
            "annotations to be created have a target task container. Please "
            "input a valid task_id or protocol_id and re-run gear. Exiting."
        )
        os.sys.exit(1)

    source_dicom = gear_context.get_input_path("source_dicom")
    if source_dicom:
        gear_args["source_dicom_path"] = Path(
            gear_context.get_input_path("source_dicom")
        )
        source_dicom_file = gear_context.get_input("source_dicom")
        gear_args["source_dicom_file_id"] = source_dicom_file["object"]["file_id"]
    else:
        acquisition_id = gear_context.destination.get("id")
        session_id = gear_context.client.get_acquisition(acquisition_id).session
        source_dicom, source_dicom_file_id = dynamic_search(
            fw_client=gear_context.client,
            work_dir=gear_context.work_dir,
            dicom_seg_path=gear_args["dicom_seg_path"],
            session_id=session_id,
        )
        gear_args["source_dicom_path"] = Path(source_dicom)
        gear_args["source_dicom_file_id"] = source_dicom_file_id

    gear_args["fw"] = FWClient(
        api_key=gear_context.get_input("api-key")["key"],
        read_timeout=100,
        connect_timeout=100,
    )

    return debug, gear_args
