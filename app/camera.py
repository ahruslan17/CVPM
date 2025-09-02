import cv2
import os


def capture_frame(filename: str = "frame.jpg") -> str:
    """
    Делает кадр с веб-камеры, выбирая максимально возможное разрешение,
    и сохраняет его в корень проекта.
    """
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # ускорение на Windows

    if not cap.isOpened():
        raise RuntimeError("Не удалось открыть веб-камеру")

    # Список стандартных разрешений (ширина x высота)
    resolutions = [
        (3840, 2160),  # 4K
        (2560, 1440),  # QHD
        (1920, 1080),  # Full HD
        (1600, 900),
        (1280, 720),  # HD
        (1024, 576),
        (800, 600),
        (640, 480),
    ]

    selected_resolution = None
    for w, h in resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        ret, frame = cap.read()
        if not ret:
            continue
        h_actual, w_actual = frame.shape[:2]
        if w_actual == w and h_actual == h:
            selected_resolution = (w, h)
            break

    if selected_resolution:
        print(
            f"Выбрано разрешение камеры: {selected_resolution[0]}x{selected_resolution[1]}"
        )
    else:
        print("Не удалось установить стандартное разрешение, используем текущее.")

    # Пропускаем пару кадров для прогрева
    for _ in range(3):
        ret, frame = cap.read()

    cap.release()

    if not ret:
        raise RuntimeError("Не удалось получить кадр с веб-камеры")

    save_path = os.path.join(os.getcwd(), filename)
    cv2.imwrite(save_path, frame)

    return save_path


if __name__ == "__main__":
    path = capture_frame()
    print(f"Кадр сохранен: {path}")
