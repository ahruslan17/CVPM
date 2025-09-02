from shapely import Point
from shapely.geometry import box, Polygon


def can_place_new_car(block_poly: Polygon, cars_boxes: list, max_cars: int):
    """
    Простая проверка наличия места для новой машины по количеству машин.

    :param block_poly: shapely Polygon — полигон блока
    :param cars_boxes: список прямоугольников машин [(x1,y1,x2,y2), ...]
    :param max_cars: максимальное количество машин, которое можно поставить в блоке
    :return: True, если место есть, False — если блок заполнен
    """
    # считаем машины внутри блока
    cars_in_block = 0
    for cb in cars_boxes:
        x1, y1, x2, y2 = cb
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        if block_poly.contains(Point(cx, cy)):
            cars_in_block += 1

    # если машин меньше максимума, можно поставить ещё
    return cars_in_block < max_cars


import shapely


def suppress_overlaps(boxes, iou_threshold=0.5, contain_threshold=0.9):
    """
    Убираем дубликаты по IoU и по вложенности
    boxes: список [(x1,y1,x2,y2), ...]
    """
    filtered = []
    while boxes:
        current = boxes.pop(0)
        current_box = box(*current)
        keep = True

        for other in filtered:
            other_box = box(*other)

            # IoU
            inter = current_box.intersection(other_box).area
            union = current_box.union(other_box).area
            iou = inter / union if union > 0 else 0

            # Вложенность: площадь пересечения ≈ площадь меньшего бокса
            smaller_area = min(current_box.area, other_box.area)
            if smaller_area == 0:
                continue
            contain = inter / smaller_area

            if iou > iou_threshold or contain > contain_threshold:
                keep = False
                break

        if keep:
            filtered.append(current)

    return filtered
