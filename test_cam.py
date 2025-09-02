import cv2
import time


def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # для Windows вебкамер
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("Не удалось открыть камеру 0")
        return
    print("Нажми 'q' для выхода")
    while True:
        ok, frame = cap.read()
        if not ok:
            print("Кадр не получен")
            time.sleep(0.1)
            continue
        cv2.imshow("Preview (USB)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
