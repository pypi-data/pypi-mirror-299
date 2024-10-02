"""Creator.py module for creating OHIF annotations from SEG arrays."""

import logging
import os
import uuid
from typing import Optional

from fw_client import FWClient
from fw_http_client.client import ClientError, NotFound

from fw_gear_dicom_seg_to_ohif.fw_utils import check_if_annotations_exist
from fw_gear_dicom_seg_to_ohif.prepper import Prepper
from fw_gear_dicom_seg_to_ohif.seg_utils import Segment

log = logging.getLogger(__name__)


class Creator:
    """Creates OHIF annotations from DICOM SEG arrays."""

    def __init__(
        self,
        prepper: Prepper,
        task_id: Optional[str],
        protocol_id: Optional[str],
        source_dicom_file_id: str,
        annotation_description: Optional[str],
        if_annotations_exist: str,
        assignee: Optional[str],
        fw: FWClient,
    ):
        """Initializes Creator.

        Args:
            prepper: Prepper as previously initialized
            task_id: 24 char BSON id of existing task or None if new task
            protocol_id: Protocol to be used if creating a new task
            source_dicom_file_id: 24 char BSON id of Flywheel file
            annotation_description: Text to populate annotation description
            if_annotations_exist: Behavior if task_id is specified and annotations exist
            assignee: If creating a new task, the Flywheel user the task is to be assigned
            fw: FWClient instance, logged in with api-key
        """
        # Useful paths
        self.work_dir = prepper.work_dir

        # Loaded DICOM SEG and DICOM elements
        self.dicom_seg = prepper.dicom_seg
        self.segments = prepper.segments
        self.dicoms = prepper.dicoms

        # Config options
        self.task_id = task_id
        self.protocol_id = protocol_id
        self.annotation_description = annotation_description
        self.if_annotations_exist = if_annotations_exist
        self.assignee = assignee

        # API
        self.source_dicom_file_id = source_dicom_file_id
        self.fw = fw
        self.task = None
        self.num_created_annotations = 0

        if not task_id:
            self.create_new_task()
        self.check_task()

    def check_task(self):
        """Checks that task_id refers to a valid task and sets self.task."""
        try:
            self.task = self.fw.get(f"/api/readertasks/{self.task_id}")
            log.info(
                f"Task with task_id {self.task_id} will be used to store annotations."
            )
            check_if_annotations_exist(
                fw=self.fw, task_id=self.task_id, behavior=self.if_annotations_exist
            )

        except (ClientError, NotFound):
            log.error(
                f"task_id value {self.task_id} did not return a valid task. Please "
                "check for typos and/or utilize protocol_id to create a new task. Exiting."
            )
            os.sys.exit(1)

    def create_new_task(self):
        """If task_id is None, create a new task to store the annotations."""
        log.info(f"Creating new task with protocol_id {self.protocol_id}...")
        if not self.assignee:
            user = self.fw.auth_status
            self.assignee = user.user_id
        log.info(f"Assigning task to {self.assignee}...")
        task_info = {
            "assignee": self.assignee,
            "parent": {
                "id": self.source_dicom_file_id,
                "type": "file",
                "version": 0,
            },
            "status": "Todo",
            "viewer": "OHIF",
            "task_type": "R",
            "protocol_id": self.protocol_id,
        }
        try:
            self.task = self.fw.post("/api/readertasks", json=task_info)
            self.task_id = self.task._id
            log.info(f"Created new task with id {self.task_id}.")
        except:  # noqa: E722
            log.error(
                "Failed to create new task. Please check protocol_id and assignee "
                "for typos or utilize task_id to specify a pre-existing task."
            )
            os.sys.exit(1)

    def process_segments(self):
        """Iterates through all segments and calls create_annotation."""
        log.info("Processing segments...")
        for segment in self.segments:
            log.info(f"\tSegment: {segment.seg_label}, {segment.dim_index}")
            self.create_annotation(segment)

        log.info(
            "Segment processing completed. "
            f"{self.num_created_annotations} total annotations created."
        )

    def create_annotation(self, segment: Segment):
        """For each polygon in segment, assembles and posts annotation.

        Args:
            segment: Class object that stores segment attributes
        """
        user = self.fw.auth_status
        study_uid = self.dicoms.get("StudyInstanceUID")
        series_uid = self.dicoms.get("SeriesInstanceUID")
        path = f"{study_uid}$$${series_uid}$$${segment.ref_sop}$$${segment.ref_frame}"

        for poly in segment.polygons:
            # Note that x corresponds to idx 1 and y to 0
            y_min, y_max = poly[:, 0].min(), poly[:, 0].max()
            x_min, x_max = poly[:, 1].min(), poly[:, 1].max()

            points = []
            for idx in range(len(poly)):
                next_point_idx = idx + 1 if idx + 1 < len(poly) else 0
                next_point = poly[next_point_idx]
                points.append(
                    {
                        "y": poly[idx][0],
                        "x": poly[idx][1],
                        "highlight": True,
                        "active": True,
                        "lines": [
                            {
                                "y": next_point[0],
                                "x": next_point[1],
                            }
                        ],
                    }
                )

            annotation_info = {
                "file_id": self.source_dicom_file_id,
                "task_id": self.task_id,
                "data": {
                    "SeriesInstanceUID": series_uid,
                    "StudyInstanceUID": study_uid,
                    "SOPInstanceUID": segment.ref_sop,
                    "uuid": str(uuid.uuid4()),
                    "flywheelOrigin": user.origin,
                    "_id": str(uuid.uuid4()),
                    "imagePath": path,
                    "handles": {
                        "points": points,
                        "textBox": {
                            "x": 0,
                            "y": 0,
                            "boundingBox": None,
                        },
                    },
                    "polyBoundingBox": {
                        "left": x_min,
                        "top": y_min,
                        "width": x_max - x_min,
                        "height": y_max - y_min,
                    },
                    "frameIndex": segment.ref_frame,
                    "measurementNumber": self.num_created_annotations,
                    "lesionNamingNumber": segment.ref_seg,
                    "location": segment.seg_label,
                    "toolType": "FreehandRoi",
                    "readonly": False,
                    "description": self.annotation_description,
                    "color": segment.color,
                },
            }

            try:
                _ = self.fw.post("/api/annotations", json=annotation_info)
                self.num_created_annotations += 1
            except (NotFound, ClientError):
                log.error("OHIF annotation creation failed. Exiting.")
                os.sys.exit(1)
