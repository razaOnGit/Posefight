import cv2
import numpy as np
from ultralytics import YOLO
from game.camera import Camera  # Use camera.py class

class PoseDetector:
    def __init__(self):
        self.model = YOLO('yolov8n-pose.pt')  # Load YOLOv8 pose model

    def detect_pose(self, frame):
        results = self.model(frame)
        return self._parse_results(results)

    def _parse_results(self, results):
        poses = {
            'punch_right': False,
            'punch_left': False,
            'kick_right': False,
            'kick_left': False,
            'jump': False,
            'crouch': False,
            'move_right': False,
            'move_left': False
        }

        for result in results:
            if result.keypoints is not None:
                # Get keypoints and confidences
                keypoints = result.keypoints.xy.cpu().numpy() if result.keypoints.xy is not None else []
                confidences = result.keypoints.conf.cpu().numpy() if result.keypoints.conf is not None else []

                if len(keypoints) > 0:
                    # Attack detection
                    if len(keypoints) > 10 and confidences[10] > 0.5:
                        poses['punch_right'] = True
                    if len(keypoints) > 9 and confidences[9] > 0.5:
                        poses['punch_left'] = True
                    if len(keypoints) > 16 and confidences[16] > 0.5:
                        poses['kick_right'] = True
                    if len(keypoints) > 15 and confidences[15] > 0.5:
                        poses['kick_left'] = True

                    # Crouch detection
                    if len(keypoints) > 11 and len(keypoints) > 5:
                        hip_y = keypoints[11, 1]  # Hip y-coordinate
                        shoulder_y = keypoints[5, 1]  # Shoulder y-coordinate
                        if hip_y > shoulder_y:
                            poses['crouch'] = True

                    # Jump detection (Fixed)
                    if len(keypoints) > 0:
                        nose_y = keypoints[0, 1]  # Nose y-coordinate
                        if isinstance(nose_y, np.ndarray) and nose_y.size > 0 and np.any(nose_y < 100):
                            poses['jump'] = True

                    # Movement detection
                    if len(keypoints) > 6:
                        left_shoulder_x = keypoints[5, 0]  # Left shoulder x-coordinate
                        right_shoulder_x = keypoints[6, 0]  # Right shoulder x-coordinate
                        if left_shoulder_x < right_shoulder_x - 50:
                            poses['move_left'] = True
                        elif right_shoulder_x < left_shoulder_x - 50:
                            poses['move_right'] = True

        return poses
