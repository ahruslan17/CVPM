# Настройки камеры и модели
CAMERA_INDEX = 0
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
CROP_REGION = (100, 200, 1180, 680)  # x1, y1, x2, y2: область парковки на кадре

MODEL_PATH = "models/parking_spot_model.pth"  # путь к предобученной модели
CONFIDENCE_THRESHOLD = 0.2  # минимальная уверенность модели
