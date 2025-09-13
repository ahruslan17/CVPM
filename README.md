# Computer Vision Parking Monitoring

## ENGLISH
### Short pitch
Computer-vision pipeline that detects cars on a parking image, evaluates availability per user‑defined parking blocks, and returns results with annotations and a Telegram bot interface.

### Key features
- Start by running set_blocks.py: it grabs a fresh snapshot from the webcam and opens the interactive labeling UI; draw parking blocks (polygons) where availability will be checked. You specify the maximum number of cars (max_cars) for each block during labeling.
- YOLO-based car detection; per-block occupancy via polygon intersection logic (a car counts for a block if ≥ ~80% of its box area lies inside the polygon).
- Duplicate detection suppression by IoU and near-containment thresholds for stability.
- High-resolution webcam snapshot with best-available resolution auto-selection (DSHOW backend on Windows).
- Turnkey script to run detection and produce an annotated image + JSON outputs for downstream use (test_detection.py, renamed from main.py).
- Telegram bot: on command or button press, captures a new frame from the camera, runs analysis, and returns a text summary plus an annotated image; TOKEN is loaded from .env.

### Architecture and modules
- set_blocks.py — UI to draw polygons and save them to parking_blocks.json; on start it takes a webcam snapshot and then lets you label blocks. Controls on screen: LMB add point, RMB close polygon, mouse wheel zoom, “s” save.
- utils.py — Geometry helpers:
  - can_place_new_car: counts cars in a block by checking centroids against the polygon.
  - suppress_overlaps: removes duplicate boxes based on IoU and containment.
- detector.py — ParkingDetectorWithSpace:
  - Filters YOLO detections to cars; a car counts for a block if intersection_area / car_area ≥ 0.8; deduplicates boxes; availability if cars_count < max_cars; draws overlays and status text.
- test_detection.py — Batch runner to get the annotated result using your chosen model (renamed from main.py).
- camera.py — capture_frame selects the highest supported resolution from a preset list, warms up the camera, and saves frame.jpg.
- config.py — Centralized constants: camera index, frame size, optional ROI, model path, confidence threshold.
- bot.py — Telegram bot (python-telegram-bot v20+). In live mode, by a Telegram trigger (/start or button) it captures a current photo, processes it, and returns the result.

### Installation
- Requirements: Python 3.10+, a webcam (for live capture), GPU recommended for YOLO.
- Install dependencies (Ultralytics, OpenCV, Shapely, Telegram Bot API, etc.):
  - pip install -r requirements.txt
- YOLO weights:
  - Place a .pt model file and ensure the code points to it (e.g., your chosen weights in test_detection.py and/or in bot.py).

### Configuration
- Edit config.py to set camera parameters, ROI, model path, and confidence threshold.
- Ensure parking_blocks.json includes an id, polygon points, and max_cars per block (the detector expects max_cars).

### Quick start
1) Label the parking blocks (and create a fresh snapshot)
   - python set_blocks.py
   - The script takes a new photo from the webcam, opens the labeling UI, and lets you draw polygons. When closing a polygon, you’ll be prompted for max_cars for that block. Press “s” to save parking_blocks.json.
2) Run detection on a still frame
   - python test_detection.py
   - Produces parking_status.json and shows/saves an annotated image with colored blocks and counts.
3) Live mode via Telegram (optional)
   - Create a .env with your TOKEN, then:
     - python bot.py
   - Use /start or the “Show parking status” button to trigger capture + analysis and receive a text summary with an annotated image.

### Data formats
- parking_blocks.json: list of blocks with fields id, points (polygon vertices), and max_cars.
- parking_status.json: dict keyed by block_id with fields cars_count, can_add_car, max_cars (emitted by the detector).

### How it works
- Detection: YOLO finds cars; a car is assigned to a block if ≥80% of its bounding-box area lies inside the polygon. Duplicate boxes are suppressed using IoU and containment checks. A block is available if cars_count < max_cars.

### Notes
- camera.py uses CAP_DSHOW on Windows; on Linux/macOS you may need to change the capture backend.
- Align model paths across files consistently (config.py may use .pth; test_detection.py/bot.py typically use .pt).

### Tech stack
- Ultralytics YOLO, OpenCV, Shapely, Python Telegram Bot, FastAPI (in requirements for potential API), NumPy


## РУССКИЙ
### Краткое описание
Пайплайн компьютерного зрения, который детектирует автомобили на изображении парковки, вычисляет доступность по заданным пользователем полигонам и возвращает результаты с аннотациями и через интерфейс Telegram-бота.

### Ключевые возможности
- Старт с запуска set_blocks.py: скрипт делает свежий снимок с веб-камеры и открывает интерфейс разметки; выделите полигоны блоков, внутри которых будет проверяться доступность. Максимальное число машин (max_cars) задаётся при разметке каждого блока.
- Детекция машин на базе YOLO; занятость блочных полигонов по доле площади бокса внутри полигона (засчитываем, если ≥ ~80%).
- Подавление дублей детекций по IoU и почти полной вложенности для стабильности.
- Снимок с веб-камеры в максимально возможном разрешении с авто‑выбором (бэкенд DSHOW на Windows).
- Скрипт пакетного запуска для получения аннотированного результата и JSON (test_detection.py, новое имя вместо main.py).
- Telegram-бот: по триггеру из Telegram (команда /start или кнопка) делает актуальный снимок, обрабатывает и возвращает результат (текст + аннотированное изображение); TOKEN берётся из .env.

### Архитектура и модули
- set_blocks.py — интерфейс для рисования полигонов и сохранения в parking_blocks.json; при старте делает снимок с камеры и затем позволяет размечать блоки. Управление: ЛКМ — добавить точку, ПКМ — замкнуть полигон, колесо — зум, “s” — сохранить.
- utils.py — геометрические утилиты:
  - can_place_new_car: считает машины по центроидам, попавшим внутрь полигона.
  - suppress_overlaps: удаляет дубли по IoU и вложенности.
- detector.py — ParkingDetectorWithSpace:
  - Фильтрует YOLO‑детекции до класса «машина»; засчитывает авто блоку при intersection_area / car_area ≥ 0.8; убирает дубли; свободно, если cars_count < max_cars; рисует контуры и статус.
- test_detection.py — пакетный запуск для получения аннотированного результата выбранной моделью (переименован из main.py).
- camera.py — capture_frame выбирает максимально доступное разрешение, прогревает камеру и сохраняет frame.jpg.
- config.py — параметры камеры, ROI, путь к модели, порог уверенности.
- bot.py — Telegram‑бот (python‑telegram‑bot v20+). В live‑режиме по триггеру из Telegram делает снимок «здесь и сейчас», обрабатывает и возвращает результат.

### Установка
- Требования: Python 3.10+, веб‑камера (для live), желательно наличие GPU для YOLO.
- Установка зависимостей (Ultralytics, OpenCV, Shapely, Telegram Bot API и др.):
  - pip install -r requirements.txt
- Веса YOLO:
  - Поместите файл модели .pt и пропишите путь к нему (в test_detection.py и/или в bot.py).

### Настройка
- Отредактируйте config.py: параметры камеры, ROI, путь к модели, порог уверенности.
- Убедитесь, что в parking_blocks.json у каждого блока есть id, точки полигона и max_cars (детектор использует max_cars).

### Быстрый старт
1) Разметьте блоки парковки (и сделайте свежий снимок)
   - python set_blocks.py
   - Скрипт делает новый кадр с веб‑камеры, открывает UI разметки и позволяет рисовать полигоны. При замыкании полигона укажите max_cars. Нажмите “s” для сохранения parking_blocks.json.
2) Запустите детекцию на статичном кадре
   - python test_detection.py
   - Скрипт создаст parking_status.json и покажет/сохранит аннотированное изображение с раскрашенными блоками и счётчиками.
3) Live‑режим через Telegram (опционально)
   - Создайте .env с вашим TOKEN и запустите:
     - python bot.py
   - Используйте /start или кнопку «Показать статус парковки», чтобы сделать снимок + анализ и получить текстовый отчёт с аннотированным изображением.

### Форматы данных
- parking_blocks.json: список блоков с полями id, points (вершины полигона), max_cars.
- parking_status.json: словарь по block_id с полями cars_count, can_add_car, max_cars (формируется детектором).

### Как работает логика
- YOLO находит машины; авто засчитывается блоку, если ≥80% площади его бокса внутри полигона. Дубли подавляются по IoU и вложенности. Блок считается доступным, если cars_count < max_cars.

### Примечания
- camera.py использует CAP_DSHOW на Windows; на Linux/macOS при необходимости смените бэкенд захвата.
- Приведите пути к весам модели к единому виду (в config.py может быть .pth; в test_detection.py/bot.py обычно .pt).

### Технологии
- Ultralytics YOLO, OpenCV, Shapely, Python Telegram Bot, FastAPI (в requirements — для потенциального API), NumPy