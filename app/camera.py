import cv2
import os


def capture_frame(filename: str = "frame.jpg") -> str:
    """
    Делает быстрый кадр с веб-камеры и сохраняет в корень проекта.
    """
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW ускоряет на Windows

    if not cap.isOpened():
        raise RuntimeError("Не удалось открыть веб-камеру")

    # Пропускаем несколько кадров для прогрева камеры
    for _ in range(5):
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
