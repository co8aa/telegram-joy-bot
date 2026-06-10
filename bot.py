import os
import random
import logging
import threading
import time
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler

# ========== НАСТРОЙКИ ==========
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден! Добавь переменную окружения в Render.")

logging.basicConfig(level=logging.INFO)

# ========== ТВОЙ ПОЛНЫЙ СПИСОК РАДОСТЕЙ ==========
# (Я оставлю его сокращенным для примера, но ты вставь свой полный список из 61 пункта)
JOYS = [
    "Разобрать ящик хаоса (любой один).",
    "Помыть одну раковину до идеала.",
    "Вымыть одну поверхность (стол / плиту).",
    "Научиться играть в шахматы.",
    "Сделать одно упражнение на осанку.",
    # ... и так далее, твой полный список ...
    "Написать себе письмо из будущего.",
]

# ========== СОЗДАЁМ БОТА ==========
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text(
        "🌸 Привет! Я — твой бот-рандомайзер радостей.\n\n"
        "Отправь /random — и я выберу для тебя одно радостное действие.\n"
        "Отправь /list — чтобы увидеть, сколько радостей в списке."
    )

async def random_joy(update: Update, context):
    joy = random.choice(JOYS)
    await update.message.reply_text(f"🎲 Твоя радость сегодня:\n\n✨ {joy}")

async def list_count(update: Update, context):
    await update.message.reply_text(f"📋 В твоём списке сейчас {len(JOYS)} радостей.")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("random", random_joy))
application.add_handler(CommandHandler("list", list_count))

# ========== ЗАПУСК БОТА ==========
def run_bot():
    print(f"🤖 Бот запущен! В списке {len(JOYS)} радостей.")
    application.run_polling()

# ========== НЕБОЛЬШОЙ ВЕБ-СЕРВЕР ДЛЯ RENDER ==========
flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "🤖 Бот для радостей работает!"

def keep_alive():
    """Функция, которая пингует бота каждые 10 минут, чтобы он не засыпал."""
    url = "https://" + os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")
    while True:
        time.sleep(600)  # Пауза 10 минут
        try:
            # Отправляем запрос к самому себе, чтобы Render не усыпил бота
            import requests
            requests.get(url)
            print("💓 Бот сказал себе 'живи'")
        except Exception as e:
            print(f"Ошибка при пинге: {e}")

# ========== ТОЧКА ВХОДА ==========
if __name__ == "__main__":
    # 1. Запускаем бота в фоновом потоке
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # 2. Запускаем поток с пингом, чтобы бот не засыпал
    ping_thread = threading.Thread(target=keep_alive)
    ping_thread.daemon = True
    ping_thread.start()
    
    # 3. Запускаем Flask, чтобы Render поверил, что он работает с портом
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Запуск Flask сервера на порту {port}...")
    flask_app.run(host="0.0.0.0", port=port)
