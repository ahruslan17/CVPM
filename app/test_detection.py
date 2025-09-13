import cv2
from app.detector import ParkingDetectorWithSpace
import json

frame = cv2.imread("frame.jpg")
detector = ParkingDetectorWithSpace(
    blocks_json="parking_blocks.json", model_path="yolov9c.pt", confidence=0.1
)

status, annotated_frame = detector.check_blocks(frame)

# сохранить статус в JSON
with open("parking_status.json", "w", encoding="utf-8") as f:
    json.dump(status, f, indent=4, ensure_ascii=False)

# показать кадр с разметкой
cv2.imshow("Parking Analysis", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
