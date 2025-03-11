import cv2
from ultralytics import YOLO

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Mirror the frame horizontally for more intuitive controls
        frame = cv2.flip(frame, 1)
        return frame

    def release(self):
        if self.cap:
            self.cap.release()

class PoseDetector:
    def __init__(self):
        self.model = YOLO('yolov8-pose.pt')  # Load the YOLOv8 pose model

    def detect_pose(self, frame):
        results = self.model(frame)
        poses = self._parse_results(results)
        return poses

    def _parse_results(self, results):
        poses = {
            'punch_right': False,
            'punch_left': False,
            'kick_right': False,
            'kick_left': False,
            'jump': False,
            'crouch': False
        }

        # Parse the results to update the poses dictionary
        for result in results:
            for keypoint in result.keypoints:
                # Example logic to determine poses based on keypoints
                if keypoint.label == 'right_hand' and keypoint.confidence > 0.5:
                    poses['punch_right'] = True
                elif keypoint.label == 'left_hand' and keypoint.confidence > 0.5:
                    poses['punch_left'] = True
                elif keypoint.label == 'right_foot' and keypoint.confidence > 0.5:
                    poses['kick_right'] = True
                elif keypoint.label == 'left_foot' and keypoint.confidence > 0.5:
                    poses['kick_left'] = True
                elif keypoint.label == 'nose' and keypoint.y < 100:  # Example condition for jump
                    poses['jump'] = True
                elif keypoint.label == 'nose' and keypoint.y > 300:  # Example condition for crouch
                    poses['crouch'] = True

        return poses
