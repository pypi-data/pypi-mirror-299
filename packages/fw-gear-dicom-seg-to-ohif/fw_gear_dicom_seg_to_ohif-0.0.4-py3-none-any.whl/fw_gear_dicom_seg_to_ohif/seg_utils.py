"""seg-utils.py module for dicom-seg-to-ohif."""

import logging
import typing as t
from dataclasses import dataclass, field
from functools import lru_cache
from math import isclose

import numpy as np
from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor
from fw_file.dicom import DICOM, DICOMCollection
from pydicom import FileDataset
from skimage import measure

log = logging.getLogger(__name__)


@dataclass
class Segment:
    """Class object for storing needed segment attributes."""

    ref_sop: str
    ref_seg: int
    seg_label: str
    dim_index: np.array
    slice_data: np.array
    ref_frame: int = 0
    offset: t.Optional[t.Tuple[float, float]] = None
    color: str = None
    polygons: list = field(default_factory=list)

    def array2poly(self):
        """Utilizes measure to identify contours and approximate polygons."""
        contours_list = measure.find_contours(self.slice_data, level=0.5)
        polygons = []
        for contour in contours_list:
            polygon_points = measure.approximate_polygon(contour, tolerance=1)
            if self.offset:
                polygon_points = np.reshape(
                    [xy - self.offset for xy in polygon_points],
                    (len(polygon_points), 2),
                )
            polygons.append(polygon_points)

        self.polygons = polygons


def create_segments(ds: FileDataset, source_dicom: DICOMCollection | DICOM) -> list:
    """Parses segment information from a pydicom FileDataset.

    Args:
        ds: Pydicom-loaded FileDataset object corresponding to DICOM-SEG file
        source_dicom: DICOMCollection or DICOM object

    Returns:
        list: List of Segment objects created from dataset
    """
    seg_reference_dict = create_segment_sequences_dict(ds)
    slice_locations = None
    segments = []
    offset = None
    for idx, pffgs in enumerate(ds.PerFrameFunctionalGroupsSequence):
        try:
            # DerivationImageSequence may not exist, but it's helpful when it does!
            # The below assumes that there is only one DerivitationImageSequence and
            # SourceImageSequence, and does not handle multiple sequences at this time.
            source = pffgs.DerivationImageSequence[0].SourceImageSequence[0]
        except IndexError:
            source = None
        if source:
            ref_sop = source.ReferencedSOPInstanceUID
            try:
                ref_frame = source.ReferencedFrameNumber
            except:  # noqa: E722
                ref_frame = 0
        else:
            # If DerivationImageSequence doesn't exist, use ImagePositionPatient
            ipp = pffgs.PlanePositionSequence[0].ImagePositionPatient
            if isinstance(source_dicom, DICOMCollection):
                ref_sop = map_ipp_to_sop(source_dicom, ipp=ipp)
                ref_frame = 0
            else:  # type(source_dicom) == DICOM
                ref_sop = source_dicom.get("SOPInstanceUID")
                ref_frame = 0
                if source_dicom.get("NumberOfFrames"):
                    iop = (
                        source_dicom.SharedFunctionalGroupsSequence[0]
                        .PlaneOrientationSequence[0]
                        .ImageOrientationPatient
                    )
                    slice_dir = calculate_slice_direction(iop)
                    if not slice_locations:
                        slice_locations = get_slice_locations(source_dicom, slice_dir)
                    ref_frame, source_ipp = map_ipp_to_frame(
                        ipp, slice_dir, slice_locations
                    )
                    if ipp != source_ipp:
                        pixel_spacing = source_dicom.PixelSpacing
                        offset = (
                            (source_ipp[1] - ipp[1]) / pixel_spacing[0],
                            (source_ipp[0] - ipp[0]) / pixel_spacing[1],
                        )
        dim_index = pffgs.FrameContentSequence[0].DimensionIndexValues
        ref_seg = pffgs.SegmentIdentificationSequence[0].ReferencedSegmentNumber
        seg_label = seg_reference_dict[ref_seg].SegmentLabel

        try:
            cielab = seg_reference_dict[ref_seg].RecommendedDisplayCIELabValue
            color = us_cielab_to_rgb_str(cielab)
        except:  # noqa: E722
            color = None

        segment = Segment(
            ref_sop=ref_sop,
            ref_seg=ref_seg,
            seg_label=seg_label,
            dim_index=dim_index,
            slice_data=ds.pixel_array[idx, :, :],
            ref_frame=ref_frame,
            offset=offset,
            color=color,
        )
        segment.array2poly()
        segments.append(segment)

    return segments


def create_segment_sequences_dict(ds: FileDataset) -> dict:
    """Creates a reference dict of Segment Sequences info, mapped to SegmentNumber

    Args:
        ds: Pydicom-loaded FileDataset object corresponding to DICOM-SEG file

    Returns:
        dict: Dictionary of SegmentNumber, Segment key value pairs
    """
    segment_sequences = {}
    for seg_seq in ds.SegmentSequence:
        segment_sequences[seg_seq.SegmentNumber] = seg_seq
    return segment_sequences


@lru_cache(maxsize=1)
def get_ipps_and_sops(source_dicom: DICOMCollection) -> t.Tuple[list, list]:
    """Caches ImagePositionPatient and SOPInstanceUID tags for mapping.

    Args:
        source_dicom: DICOMCollection object to be utilized for mapping

    Returns:
        list: List of ImagePositionPatient as returned by fw-file's bulk_get
        list: List of SOPInstanceUID as returned by fw-file's bulk_get
    """
    ipps = source_dicom.bulk_get("ImagePositionPatient")
    sops = source_dicom.bulk_get("SOPInstanceUID")

    return ipps, sops


def map_ipp_to_sop(source_dicom: DICOMCollection, ipp: np.ndarray) -> str:
    """When given a valid ImagePositionPatient, returns the related SOPInstanceUID.

    Args:
        source_dicom: DICOMCollection object to be utilized for mapping
        ipp: ImagePositionPatient value to match with SOPInstanceUID

    Returns:
        str: SOPInstanceUID of DICOM corresponding with given ImagePositionPatient
    """
    ipps, sops = get_ipps_and_sops(source_dicom)

    sop = sops[ipps.index(ipp)]
    # TODO: Account for potential ipp offset (as with map_ipp_to_frame)?

    return sop


def calculate_slice_direction(iop: list) -> list:
    row_dir = np.array(iop[:3])
    col_dir = np.array(iop[3:])
    slice_dir = np.cross(row_dir, col_dir)
    return slice_dir


def get_slice_locations(
    source_dicom: DICOM, slice_dir: np.ndarray
) -> list[t.Tuple[float, list]]:
    """Caches slice locations and ImagePositionPatient values for mapping.

    Args:
        source_dicom: DICOM object to be used for mapping
        slice_dir: Slice direction calculated from ImageOrientationPatient

    Returns:
        list: List of slice location and corresponding ImagePositionPatient values
    """
    slice_locs = []
    for pffgs in source_dicom.PerFrameFunctionalGroupsSequence:
        ipp = pffgs.PlanePositionSequence[0].ImagePositionPatient
        slice_loc = np.dot(slice_dir, ipp)
        slice_locs.append((slice_loc, ipp))
    return slice_locs


def map_ipp_to_frame(
    ipp_to_find: np.ndarray, slice_dir: np.ndarray, slice_locations: list
) -> t.Tuple[int, str]:
    """When given a valid ImagePositionPatient, returns the related frame and ImagePositionPatient.

    Args:
        ipp_to_find: ImagePositionPatient to match (from seg)
        slice_dir: Slice Direction
        slice_locations: List of slice location and corresponding ImagePositionPatient values from source DICOM

    Returns:
        int: Frame
        str: ImagePositionPatient of frame (from source_dicom)
    """
    slice_loc_to_find = np.dot(slice_dir, ipp_to_find)

    for idx, (loc, ipp) in enumerate(slice_locations):
        if isclose(loc, slice_loc_to_find, rel_tol=1e-05):
            # Some of the provided test data has an xy offset and z rounded slightly differently
            # Therefore, this allows for a slight rounding difference and returns the source ipp
            # so that the offset can be calculated
            return idx + 1, ipp


def us_cielab_to_rgb_str(us_vals: list) -> str:
    """Converts CIELab (represented as PCS-Values) to rgba string for annotation creation.

    Args:
        us_vals: List of three unsigned shorts to be converted

    Returns:
        str: String representation of rgba value for OHIF annotation
    """
    # Units are specified in PCS-Values, and the value is encoded as CIELab.
    # Consist of three unsigned short values:
    # An L value linearly scaled to 16 bits, such that 0x0000 corresponds to an L of 0.0, and 0xFFFF corresponds to an L of 100.0.
    # An a* then a b* value, each linearly scaled to 16 bits and offset to an unsigned range, such that 0x0000 corresponds to
    # an a* or b* of -128.0, 0x8080 corresponds to an a* or b* of 0.0 and 0xFFFF corresponds to an a* or b* of 127.0
    cielab_l = us_vals[0] / 65535.0 * 100
    cielab_a = us_vals[1] / 65535.0 * 256 - 128
    cielab_b = us_vals[2] / 65535.0 * 256 - 128

    lab = LabColor(cielab_l, cielab_a, cielab_b)
    rgb = convert_color(lab, sRGBColor)
    # convert_color gives values 0-1
    red = int(rgb.rgb_r * 255)
    green = int(rgb.rgb_g * 255)
    blue = int(rgb.rgb_b * 255)

    color = f"rgba({red}, {green}, {blue}, 0.2)"

    return color
