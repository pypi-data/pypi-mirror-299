"""fw_utils.py module for dicom-seg-to-ohif."""

import logging
import os
import zipfile
from pathlib import Path
from typing import Optional, Tuple

from flywheel import Client
from fw_client import FWClient
from fw_file.dicom import DICOM, DICOMCollection
from fw_http_client.client import ClientError, NotFound

log = logging.getLogger(__name__)


def dynamic_search(
    fw_client: Client, work_dir: Path, dicom_seg_path: Path, session_id: str
) -> Path:
    """Searches the session container for a matching DICOM.

    Args:
        fw_client: Flywheel Client instance
        work_dir: Path to work directory
        dicom_seg_path: Path to input DICOM SEG
        session_id: Flywheel session id related to input DICOM SEG

    Returns:
        Path: Path to downloaded matching DICOM
    """
    log.info("Attempting to locate source DICOM...")
    dicom_seg_filename = dicom_seg_path.name
    sops_to_match = get_dicom_seg_referenced_sop(dicom_seg_path)
    dicom_file_paths, file_id_ref_dict = collect_potential_dicom_files(
        fw_client, work_dir, session_id, dicom_seg_filename
    )
    source_dicom = check_all_dicom_files(dicom_file_paths, sops_to_match)
    log.info(f"Identified {source_dicom.name} as source DICOM.")
    file_id = file_id_ref_dict[source_dicom]

    return source_dicom, file_id


def get_dicom_seg_referenced_sop(dicom_seg_path: Path) -> list:
    """Gets Referenced SOP Instance UID(s) from the DICOM SEG.

    Args:
        dicom_seg_path: Path to DICOM SEG

    Returns:
        list: All Referenced SOP Instance UIDs
    """

    dicom_seg = DICOM(dicom_seg_path, force=True)
    sops = []
    try:
        for rss in dicom_seg.ReferencedSeriesSequence:
            for ris in rss.ReferencedInstanceSequence:
                sops.append(ris.ReferencedSOPInstanceUID)
    except:  # noqa: E722
        log.info(
            "ReferencedSOPInstanceUID not found in ReferencedSeriesSequence. Trying SourceImageSequence."
        )
        try:
            for sis in dicom_seg.SourceImageSequence:
                sops.append(sis.ReferencedSOPInstanceUID)
        except:  # noqa: E722
            log.error(
                "Unable to parse Referenced SOP Instance UID from DICOM SEG, "
                "and therefore cannot dynamically identify source_dicom. "
                "source_dicom must be provided via gear input. Exiting."
            )
            os.sys.exit(1)

    return sops


def collect_potential_dicom_files(
    fw_client: Client, work_dir: Path, session_id: str, dicom_seg_filename: str
) -> Tuple[list, dict]:
    """Downloads all DICOM files in the session container for review.

    Args:
        fw_client: Flywheel Client
        work_dir: Path to work directory
        session_id: Flywheel session ID to search
        dicom_seg_filename: DICOM SEG name (to prevent re-download)

    Returns:
        list: Paths to all downloaded DICOM files
        dict: Dictionary to map files to file_id value, with paths as keys
    """
    dicom_search_dir = work_dir / "potential_dicoms"
    dicom_search_dir.mkdir(parents=True, exist_ok=True)
    dicom_file_paths = []
    file_id_ref_dict = {}

    session = fw_client.get_session(session_id)
    acquisitions = session.acquisitions.find()
    for acquisition in acquisitions:
        files = acquisition.get("files")
        for file in files:
            if file.get("type") == "dicom" and file.get("name") != dicom_seg_filename:
                filename = file.get("name")
                filepath = dicom_search_dir / filename
                acquisition.download_file(filename, dest_file=filepath)
                dicom_file_paths.append(filepath)
                file_id_ref_dict[filepath] = file.get("file_id")

    return dicom_file_paths, file_id_ref_dict


def check_all_dicom_files(dicom_file_paths: list, sops_to_match: list) -> Path:
    """Iterate through all possible DICOMs and check for SOP Instance UID match.

    If no DICOMs match, or more than one matches, instruct user to
    explicitly input source_dicom as gear input and exit.

    Args:
        dicom_file_paths: List of paths to downloaded DICOMs
        sops_to_match: UIDs from DICOM SEG to match

    Returns:
        Path: Path to source_dicom, if found
    """
    matching_files = []
    for dicom_file in dicom_file_paths:
        dicom_path = check_dicom_file(dicom_file, sops_to_match)
        if dicom_path:
            matching_files.append(dicom_path)

    if len(matching_files) == 1:
        # Only one possible source_dicom found in session,
        # this is what we want.
        source_dicom_path = matching_files[0]
        return source_dicom_path
    else:
        # No possible matching DICOMs, or too many. Raise error.
        log.error(
            "%s potential source_dicom files identified; "
            "gear cannot dynamically identify source_dicom. "
            "source_dicom must be provided via gear input. Exiting.",
            len(matching_files),
        )
        os.sys.exit(1)


def check_dicom_file(dicom_file: Path, sops_to_match: list) -> Optional[Path]:
    """Check individual DICOM file and return filepath if match.

    Args:
        dicom_file: Path to downloaded DICOM file being checked
        sops_to_match: DICOM SEG UIDs to use for check

    Returns:
        Path: If DICOM matches UIDs, path to DICOM file
    """
    if zipfile.is_zipfile(dicom_file):
        dcms = DICOMCollection.from_zip(dicom_file, force=True)
        sops = dcms.bulk_get("SOPInstanceUID")
        for sop in sops:
            if sop not in sops_to_match:
                return None
    else:
        dcm = DICOM(dicom_file, force=True)
        sop = dcm.SOPInstanceUID
        if sop != sops_to_match[0]:
            return None

    return dicom_file


def check_if_annotations_exist(fw: FWClient, task_id: str, behavior: str):
    """Retrieves all annotations related to task and follows configured behavior.

    Args:
        fw: FWClient instance, logged in with api-key
        task_id: 24 char BSON id corresponding with existing task
        behavior: What to do if existing annotations are retrieved
    """
    try:
        annotations = fw.get(f"/api/readertasks/{task_id}/annotations")
    except (ClientError, NotFound):
        log.error(
            f"Task with id {task_id} not found. Please check that this task exists "
            "or use config option `protocol_id` to create a new task_id. Exiting."
        )
        os.sys.exit(1)
    if annotations["count"] == 0:
        log.info("No existing annotations found, continuing.")
    elif behavior == "append":
        log.info(
            f"{annotations['count']} annotations found. New annotations will be appended."
        )
    elif behavior == "override":
        log.info(f"{annotations['count']} annotations found, deleting...")
        for annotation in annotations["results"]:
            try:
                fw.delete(f'/api/annotations/{annotation.get("_id")}')
            except (ClientError, NotFound):
                log.warning(
                    f"Annotation with id {annotation.get('_id')} connected to task_id but "
                    "could not be deleted. Exiting..."
                )
                os.sys.exit(1)
        log.info("Existing annotation deletion complete.")
    else:  # behavior == "exit"
        log.error(
            f"Task with id {task_id} already has associated annotations. Exiting."
        )
        os.sys.exit(1)
