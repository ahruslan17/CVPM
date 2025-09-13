# Computer Vision Parking Monitoring

ENGLISH

Short pitch
Computer-vision pipeline that detects cars on a parking image, evaluates availability per user‑defined parking blocks, and returns results with annotations and a Telegram bot interface.

Key features
- Interactive parking-block labeling on a reference frame: left-click to add points, right-click to close polygon, mouse wheel to zoom, press “s” to save to parking_blocks.json [1].
- YOLO-based car detection; per-block occupancy via polygon intersection logic (counts a car if ≥ ~80% of its box area is inside the block) [6][9].
- Duplicate detection suppression by IoU and near-containment thresholds for stability [2].
- High-resolution webcam snapshot with best-available resolution auto-selection (DSHOW backend on Windows) [4].
- Turnkey scripts to run detection and visualize colored blocks and labels; JSON outputs for downstream use [3][7].
- Telegram bot: on command/button, captures a new frame and runs analysis; uses TOKEN from .env [8].

Architecture and modules
- set_blocks.py — UI to draw polygons over an image and save them to parking_blocks.json. Controls are printed on screen (LMB add point, RMB close, wheel zoom, “s” save) [1].
- utils.py — Geometry helpers:
  - can_place_new_car: counts cars in a block by checking centroids against the polygon [2].
  - suppress_overlaps: removes duplicate boxes based on IoU and containment [2].
- detector.py — ParkingDetectorWithSpace:
  - Filters YOLO detections to cars; a car counts for a block if intersection_area / car_area ≥ 0.8; deduplicates boxes; availability if cars_count < max_cars; draws overlay and status text [6].
- main.py — Batch runner: loads frame.jpg, runs detector, saves parking_status.json, shows annotated window [7].
- visualize_parking.py — Reads parking_blocks.json and parking_status.json and draws colored polygons and block labels over a test image [3].
- camera.py — capture_frame selects the highest supported resolution from a preset list, warms up the camera, saves frame.jpg [4].
- config.py — Centralized constants: camera index, frame size, optional ROI, model path, confidence threshold [5].
- bot.py — Telegram bot (python-telegram-bot v20+). On /start or button press, captures a frame and analyzes blocks; TOKEN is loaded from .env [8][9].

Installation
- Requirements: Python 3.10+, a webcam for live capture (optional), GPU recommended for YOLO.
- Install dependencies (Ultralytics, OpenCV, Shapely, Telegram Bot API, etc.) [9]:
    pip install -r requirements.txt
- YOLO weights:
  - Place a .pt model file and ensure the code points to it (e.g., yolov9e.pt in main.py or yolov9c.pt in bot.py) [7][8].

Configuration
- Edit config.py to set camera parameters, ROI, model path, and confidence threshold [5].
- Ensure parking_blocks.json includes an id, polygon points, and max_cars per block (detector expects max_cars; visualization uses blocks data) [1][6].

Quick start
1) Capture a reference frame for labeling
    python app/camera.py
   The script auto-selects the highest working resolution and saves frame.jpg [4].
2) Label parking blocks on the frame
    python set_blocks.py
   Follow on-screen controls to create polygons; press “s” to save parking_blocks.json [1].
3) Run detection on a frame
    python main.py
   Produces parking_status.json and shows the annotated image [7].
4) Telegram bot (optional)
- Create a .env with TOKEN, then:
    python bot.py
- Use /start or the “Show parking status” button to run analysis [8].

Data formats
- parking_blocks.json: list of blocks with id and polygon points; include max_cars for capacity logic [1][6].
- parking_status.json: dict keyed by block_id with fields cars_count, can_add_car, max_cars (from detector) [6][7].

How it works
- Detection: YOLO finds cars; a car is assigned to a block if ≥80% of its box lies inside the polygon; duplicate boxes are suppressed with IoU/containment checks. A block is available if cars_count < max_cars [6][2].

Notes
- visualize_parking.py expects boolean-like status per block; the detector emits a detailed dict. Map can_add_car to your visualization logic if needed [3][6].
- camera.py uses CAP_DSHOW on Windows; adjust capture backend on Linux/macOS if required [4].
- Align model paths across files: config.py uses .pth, while main.py and bot.py use .pt. Choose one and update references consistently [5][7][8].

Tech stack
- Ultralytics YOLO, OpenCV, Shapely, Python Telegram Bot, FastAPI (present in requirements for potential API), NumPy [9].


РУССКИЙ

Краткое описание
Пайплайн компьютерного зрения для оценки доступности парковочных мест: детектирует автомобили на изображении, вычисляет занятость по пользовательским полигонам и возвращает результат с аннотациями и через Telegram-бота.

Ключевые возможности
- Интерактивная разметка блоков парковки: ЛКМ — добавить точку, ПКМ — замкнуть полигон, колесо мыши — зум, “s” — сохранить в parking_blocks.json [1].
- Детекция автомобилей на YOLO; учёт занятости по пересечению боксов с полигонами (машина засчитывается, если ≥ ~80% площади бокса внутри блока) [6][9].
- Подавление дублей детекций по IoU и почти полной вложенности [2].
- Снимок с веб-камеры в максимально возможном разрешении (DSHOW на Windows) [4].
- Скрипты для запуска детекции и визуализации раскрашенных полигонов; выводы в JSON [3][7].
- Telegram-бот: по команде/кнопке делает снимок и запускает анализ; токен берётся из .env [8].

Архитектура и модули
- set_blocks.py — инструмент рисования полигонов и сохранения в parking_blocks.json. Подсказки по управлению выводятся на экран (ЛКМ, ПКМ, колесо, “s”) [1].
- utils.py — геометрические утилиты:
  - can_place_new_car: считает машины по центроидам внутри полигона [2].
  - suppress_overlaps: удаляет дубли по IoU и вложенности [2].
- detector.py — ParkingDetectorWithSpace:
  - Фильтрует детекции до класса «машина»; засчитывает авто блоку при доле площади ≥ 0.8; убирает дубли; считает свободно, если cars_count < max_cars; рисует контуры и статус [6].
- main.py — пакетный запуск: читает frame.jpg, запускает детектор, сохраняет parking_status.json, показывает окно с аннотацией [7].
- visualize_parking.py — читает parking_blocks.json и parking_status.json, рисует полигоны и подписи статуса [3].
- camera.py — capture_frame выбирает максимально доступное разрешение, прогревает камеру, сохраняет frame.jpg [4].
- config.py — параметры камеры, ROI, путь к модели, порог уверенности [5].
- bot.py — Telegram-бот (python-telegram-bot v20+). По /start или кнопке снимает кадр и анализирует; TOKEN загружается из .env [8][9].

Установка
- Требования: Python 3.10+, веб-камера (для live), для YOLO желательно наличие GPU.
- Установка зависимостей [9]:
    pip install -r requirements.txt
- Веса YOLO:
  - Поместите .pt модель и укажите путь в коде (например, yolov9e.pt в main.py или yolov9c.pt в bot.py) [7][8].

Настройка
- Отредактируйте config.py: камера, размер кадра, при необходимости ROI, путь к модели, порог уверенности [5].
- Убедитесь, что parking_blocks.json содержит id, точки полигона и max_cars для каждого блока (детектор использует max_cars; визуализация читает блоки) [1][6].

Быстрый старт
1) Снимок эталонного кадра
    python app/camera.py
   Скрипт автоматически выбирает наивысшее рабочее разрешение и сохраняет frame.jpg [4].
2) Разметка парковочных блоков
    python set_blocks.py
   Следуйте подсказкам на экране; “s” — сохранить parking_blocks.json [1].
3) Запуск детекции на кадре
    python main.py
   Получите parking_status.json и окно с аннотацией [7].
4) Telegram-бот (опционально)
- Создайте .env с TOKEN и запустите:
    python bot.py
- Используйте /start или кнопку «Показать статус парковки» [8].

Форматы данных
- parking_blocks.json: список блоков с id и точками полигона; добавьте max_cars для логики вместимости [1][6].
- parking_status.json: словарь по block_id с полями cars_count, can_add_car, max_cars (из детектора) [6][7].

Как работает логика
- YOLO находит машины; авто засчитывается блоку, если ≥80% площади бокса лежит внутри полигона; дубли подавляются по IoU/вложенности; свободно, если cars_count < max_cars [6][2].

Примечания
- visualize_parking.py ожидает булев статус; детектор отдаёт словарь. Для раскраски можно использовать поле can_add_car [3][6].
- camera.py использует CAP_DSHOW (Windows); на Linux/macOS при необходимости смените бэкенд [4].
- Согласуйте пути к модели: в config.py — .pth, в main.py/bot.py — .pt. Выберите единый формат и обновите ссылки [5][7][8].

Технологии
- Ultralytics YOLO, OpenCV, Shapely, Python Telegram Bot, FastAPI (в requirements — потенциал API), NumPy [9].