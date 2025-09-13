import cv2
import json
import numpy as np

polygons = []  # список всех блоков
current_polygon = []  # текущий полигон
block_id = 1

# параметры прокрутки
offset_x, offset_y = 0, 0
scale = 1.0
mouse_start = None


def draw_polygon(event, x, y, flags, param):
    global current_polygon, polygons, block_id
    global offset_x, offset_y, scale

    # координаты с учётом смещения и масштаба
    x_real = int((x - offset_x) / scale)
    y_real = int((y - offset_y) / scale)

    img_copy = img.copy()

    # рисуем все сохраненные полигоны
    for poly in polygons:
        pts = np.array(poly["points"], np.int32)
        pts_scaled = ((pts * scale) + [offset_x, offset_y]).astype(int)
        cv2.polylines(
            img_copy, [pts_scaled], isClosed=True, color=(0, 255, 0), thickness=2
        )
        cx, cy = pts_scaled[0]
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
        pts = np.array(current_polygon + [(x_real, y_real)], np.int32)
        pts_scaled = ((pts * scale) + [offset_x, offset_y]).astype(int)
        cv2.polylines(
            img_copy, [pts_scaled], isClosed=False, color=(0, 0, 255), thickness=2
        )

    cv2.imshow("Polygon Labeling", img_copy)

    if event == cv2.EVENT_LBUTTONDOWN:
        current_polygon.append((x_real, y_real))

    elif event == cv2.EVENT_RBUTTONDOWN and len(current_polygon) >= 3:
        current_polygon.append(current_polygon[0])
        try:
            max_cars = int(input(f"Введите макс. количество машин для {block_id}: "))
        except ValueError:
            max_cars = 2
        polygons.append(
            {
                "id": f"Block_{block_id}",
                "points": current_polygon.copy(),
                "max_cars": max_cars,
            }
        )
        block_id += 1
        current_polygon.clear()


def mouse_wheel(event, x, y, flags, param):
    global scale, offset_x, offset_y
    if flags > 0:  # прокрутка вверх
        scale *= 1.1
    else:  # прокрутка вниз
        scale /= 1.1


# загрузка изображения
img = cv2.imread("frame.jpg")
cv2.namedWindow("Polygon Labeling", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("Polygon Labeling", draw_polygon)

print(
    "Левой кнопкой добавляйте точки полигона. Правой кнопкой завершайте блок (замкнётся автоматически)."
)
print("Используйте колесо мыши для масштабирования.")
print("Нажмите 's' для сохранения и выхода.")

while True:
    key = cv2.waitKey(20) & 0xFF
    if key == ord("s"):
        break

cv2.destroyAllWindows()

with open("parking_blocks.json", "w") as f:
    json.dump(polygons, f, indent=4)

print("Блоки сохранены в parking_blocks.json")
