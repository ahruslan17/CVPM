# bot.py
import logging
import cv2
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from app.detector import ParkingDetectorWithSpace
import os
from dotenv import load_dotenv
from app.camera import capture_frame

# --- Настройка логирования ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# --- Инициализация детектора ---
detector = ParkingDetectorWithSpace(
    blocks_json="parking_blocks.json", model_path="yolov9c.pt", confidence=0.1
)

# --- Клавиатура ---
keyboard = [["Показать статус парковки"]]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# --- Обработка команды /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать! Нажмите кнопку ниже для получения статуса парковки.",
        reply_markup=reply_markup,
    )


# --- Обработка статуса (кнопка или /status) ---
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id, "Анализирую парковку...")

    # Загружаем изображение парковки
    capture_frame("frame.jpg")
    frame = cv2.imread("frame.jpg")
    if frame is None:
        await context.bot.send_message(chat_id, "Не удалось загрузить изображение.")
        return

    # Анализируем блоки
    block_status, annotated_frame = detector.check_blocks(frame)

    # Формируем текст отчёта
    report = ""
    for block_id, info in block_status.items():
        status_text = "✅ место есть" if info["can_add_car"] else "❌ блок полон"
        report += f"{block_id}: {info['cars_count']}/{info.get('max_cars', '?')} машин, {status_text}\n"

    await context.bot.send_message(chat_id, report)

    # Сохраняем аннотированное изображение
    output_path = "annotated_frame.jpg"
    cv2.imwrite(output_path, annotated_frame)

    # Отправляем фото
    with open(output_path, "rb") as f:
        await context.bot.send_photo(chat_id=chat_id, photo=f)


# --- Обработка сообщений для нажатия кнопки ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Показать статус парковки":
        await status(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, используйте кнопку для получения статуса парковки.",
            reply_markup=reply_markup,
        )


if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.environ.get("TOKEN")
    if not TOKEN:
        raise ValueError(
            "TOKEN не найден в переменных окружения. Установите переменную TOKEN в .env."
        )

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling()
