import cv2
import json
import numpy as np
from camera import capture_frame

polygons = []  # список всех блоков
current_polygon = []  # текущий полигон
block_id = 1


def draw_polygon(event, x, y, flags, param):
    global current_polygon, polygons, block_id
    img_copy = img.copy()

    # рисуем все уже сохраненные полигоны
    for poly in polygons:
        pts = poly["points"]
        cv2.polylines(
            img_copy,
            [np.array(pts, np.int32)],
            isClosed=True,
            color=(0, 255, 0),
            thickness=2,
        )
        cx, cy = pts[0]
        cv2.putText(
            img_copy,
            f"{poly['id']} (max {poly['max_cars']})",
            (cx, cy - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

    # рисуем текущий полигон
    if len(current_polygon) > 0:
        pts = np.array(current_polygon + [(x, y)], np.int32)
        cv2.polylines(img_copy, [pts], isClosed=False, color=(0, 0, 255), thickness=2)

    cv2.imshow("Polygon Labeling", img_copy)

    # левая кнопка добавляет точку
    if event == cv2.EVENT_LBUTTONDOWN:
        current_polygon.append((x, y))

    # правая кнопка завершает полигон (автозамыкание)
    elif event == cv2.EVENT_RBUTTONDOWN and len(current_polygon) >= 3:
        # добавляем первую точку в конец для замыкания
        current_polygon.append(current_polygon[0])

        try:
            max_cars = int(input(f"Введите макс. количество машин для {block_id}: "))
        except ValueError:
            max_cars = 2  # значение по умолчанию

        polygons.append(
            {
                "id": f"Block_{block_id}",
                "points": current_polygon.copy(),
                "max_cars": max_cars,
            }
        )
        block_id += 1
        current_polygon.clear()


capture_frame("frame.jpg")
img = cv2.imread("frame.jpg")
cv2.namedWindow("Polygon Labeling")
cv2.setMouseCallback("Polygon Labeling", draw_polygon)

print(
    "Левой кнопкой добавляйте точки полигона. Правой кнопкой завершайте блок (замкнётся автоматически)."
)
print("Нажмите 's' для сохранения и выхода.")

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord("s"):  # сохранить и выйти
        break

cv2.destroyAllWindows()

# сохраняем блоки в JSON
with open("parking_blocks.json", "w") as f:
    json.dump(polygons, f, indent=4)

print("Блоки сохранены в parking_blocks.json")
