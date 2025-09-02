from ultralytics import YOLO
import cv2
import json
import numpy as np
from shapely.geometry import Point, Polygon
from shapely.geometry import box
from app.utils import suppress_overlaps


class ParkingDetectorWithSpace:
    def __init__(
        self,
        blocks_json="parking_blocks.json",
        model_path="yolov8l.pt",
        confidence=0.5,
    ):
        """
        :param blocks_json: файл с полигонами блоков парковки (каждый блок должен содержать поле "max_cars")
        :param model_path: путь к модели YOLOv8
        :param confidence: минимальная уверенность детекции
        """
        self.model = YOLO(model_path)
        self.confidence = confidence

        # загружаем блоки парковки
        with open(blocks_json, "r") as f:
            data = json.load(f)

        self.blocks = {}
        for b in data:
            block_id = b["id"]
            poly = Polygon(b["points"])
            max_cars = b.get("max_cars", 2)  # значение по умолчанию = 2
            self.blocks[block_id] = {"poly": poly, "max_cars": max_cars}

        # индекс класса "car" в COCO
        self.car_class_idx = 2  # COCO: car = 2

    def check_blocks(self, frame):
        """
        Детектируем машины и анализируем каждый блок на доступность места.
        Возвращаем словарь с информацией и аннотированный кадр.
        """
        results = self.model(frame, conf=self.confidence)
        detections = results[0].boxes

        block_status = {}
        for block_id, info in self.blocks.items():
            poly = info["poly"]
            poly = poly.buffer(0)
            max_cars = info["max_cars"]

            # собираем машины внутри блока
            cars_boxes_in_block = []

            for i in range(len(detections)):
                cls = int(detections.cls[i].item())
                if cls != self.car_class_idx:
                    continue

                x1, y1, x2, y2 = map(int, detections.xyxy[i].tolist())
                car_box = box(x1, y1, x2, y2)
                intersection_area = car_box.intersection(poly).area
                car_area = car_box.area

                if intersection_area / car_area >= 0.8:
                    cars_boxes_in_block.append((x1, y1, x2, y2))

            # убираем дубли
            cars_boxes_in_block = suppress_overlaps(
                cars_boxes_in_block, iou_threshold=0.6, contain_threshold=0.9
            )

            # проверяем, есть ли место для новой машины
            can_add = len(cars_boxes_in_block) < max_cars
            block_status[block_id] = {
                "cars_count": len(cars_boxes_in_block),
                "can_add_car": can_add,
                "max_cars": max_cars,
            }

            # рисуем блок и машины
            self._draw_block(frame, poly, cars_boxes_in_block, can_add, block_id)

        return block_status, frame

    def _draw_block(self, frame, poly, cars_boxes, can_add, block_id):
        # цвет блока: зеленый = есть место, красный = блок заполнен
        color = (0, 255, 0) if can_add else (0, 0, 255)
        pts = [(int(x), int(y)) for x, y in poly.exterior.coords]
        cv2.polylines(
            frame, [np.array(pts, np.int32)], isClosed=True, color=color, thickness=2
        )

        # рисуем машины внутри блока
        for idx, (x1, y1, x2, y2) in enumerate(cars_boxes, 1):
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(
                frame,
                f"Car {idx}",
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 0, 0),
                2,
            )

        # подпись блока
        cx, cy = pts[0]
        status_text = (
            f"Space available ({len(cars_boxes)}/{self.blocks[block_id]['max_cars']})"
            if can_add
            else "Block full"
        )
        cv2.putText(
            frame,
            f"{block_id}: {status_text}",
            (cx, cy - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2,
        )
