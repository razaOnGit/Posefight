import cv2

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
