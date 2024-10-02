"""Prepper.py module for loading in DICOM SEG and source DICOM."""

import logging
import os
import zipfile
from pathlib import Path

from fw_file.dicom import DICOM, DICOMCollection
from fw_file.dicom.utils import sniff_dcm
from pydicom import dcmread

from fw_gear_dicom_seg_to_ohif.seg_utils import create_segments

log = logging.getLogger(__name__)


class Prepper:
    """Prepares DICOM and DICOM SEG files for use."""

    def __init__(
        self,
        work_dir: Path,
        dicom_seg_path: Path,
        source_dicom_path: Path,
    ):
        """Initializes Prepper.

        Args:
            work_dir: Path to work directory
            dicom_seg_path: Path to DICOM SEG
            source_dicom_path: Path to source DICOM
        """
        if work_dir is None:
            work_dir = ""

        self.work_dir = Path(work_dir)
        self.source_dicom_path = source_dicom_path
        self.dicom_seg_path = dicom_seg_path

        self.dicom_seg = None
        self.segments = None

        self.dicoms = None

        self.load_dicoms()
        self.load_dicom_seg()

    def load_dicoms(self):
        """Unzips DICOM if archived, and loads."""
        if zipfile.is_zipfile(self.source_dicom_path):
            self.dicoms = DICOMCollection.from_zip(self.source_dicom_path, force=True)
        else:
            if not sniff_dcm(self.source_dicom_path):
                log.warning(
                    "Source DICOM is missing file signature, "
                    "attempting to read as a single DICOM"
                )
            self.dicoms = DICOM(self.source_dicom_path, force=True)

    def load_dicom_seg(self):
        """Loads in the DICOM SEG and creates Segment objects."""
        if zipfile.is_zipfile(self.dicom_seg_path):
            with zipfile.ZipFile(self.dicom_seg_path, "r") as archive:
                unzipped_dir = self.dicom_seg_path.parent / "unzipped"
                unzipped_dir.mkdir()
                archive.extractall(path=unzipped_dir)
                files = [f for f in unzipped_dir.iterdir() if f.is_file()]
                if len(files) != 1:
                    log.error(
                        f"DICOM-SEG input archive invalid, contains {len(files)} files. "
                        "This gear currently only handles one DICOM-SEG file at a time. "
                        "Exiting."
                    )
                    os.sys.exit(1)
                else:
                    self.dicom_seg_path = files[0]
        seg = dcmread(self.dicom_seg_path)
        self.dicom_seg = seg
        self.segments = create_segments(seg, source_dicom=self.dicoms)
