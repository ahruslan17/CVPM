import cv2
from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, CROP_REGION


class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        x1, y1, x2, y2 = CROP_REGION
        self.crop_region = (x1, y1, x2, y2)

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Не удалось получить кадр с камеры")
        x1, y1, x2, y2 = self.crop_region
        cropped_frame = frame[y1:y2, x1:x2]
        return cropped_frame

    def release(self):
        self.cap.release()


class ImageLoader:
    def __init__(self, path, crop_region=None):
        self.path = path
        self.crop_region = crop_region

    def get_frame(self):
        frame = cv2.imread(self.path)
        if frame is None:
            raise RuntimeError(f"Не удалось загрузить изображение {self.path}")
        if self.crop_region:
            x1, y1, x2, y2 = self.crop_region
            frame = frame[y1:y2, x1:x2]
        return frame
