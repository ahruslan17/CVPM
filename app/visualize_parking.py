import cv2
import json
import numpy as np
from shapely.geometry import Polygon

# загружаем блоки
with open("parking_blocks.json", "r", encoding="utf-8") as f:
    data = json.load(f)
blocks = {b["id"]: Polygon(b["points"]) for b in data}

# загружаем статус блоков
with open("parking_status.json", "r", encoding="utf-8") as f:
    status = json.load(f)

# загружаем изображение
frame = cv2.imread("test_parking.jpg")
if frame is None:
    raise FileNotFoundError("Не удалось загрузить изображение")

# визуализация
for block_id, poly in blocks.items():
    pts = [(int(x), int(y)) for x, y in poly.exterior.coords]
    occupied = not status.get(block_id, True)
    color = (0, 0, 255) if occupied else (0, 255, 0)
    cv2.polylines(
        frame, [np.array(pts, np.int32)], isClosed=True, color=color, thickness=2
    )

    # подпись блока
    cx, cy = pts[0]
    text = f"{block_id}: {'False' if occupied else 'True'}"
    cv2.putText(frame, text, (cx, cy - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

# показать
cv2.imshow("Parking Visualization", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
