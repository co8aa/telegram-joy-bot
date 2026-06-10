import os
import random
import logging
import threading
import time
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler

TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден!")

logging.basicConfig(level=logging.INFO)

JOYS = [
    "Разобрать ящик хаоса (любой один).",
    "Помыть одну раковину до идеала.",
    "Вымыть одну поверхность (стол / плиту).",
    "Разобрать детские вещи на \"маленькое / сейчас / убрать\".",
    "Пересортировать косметику или уход.",
    "Почистить телефон: фото / заметки / вкладки.",
    "Разложить одежду по стопкам.",
    "Быстро протереть пыль в одной зоне.",
    "Переставить что-то в комнате (микро-изменение пространства).",
    "Пересобрать холодильник/полку.",
    "Сделать простую еду (без рецепта — импровизация).",
    "Сделать напиток \"не как обычно\" (новая сборка).",
    "Выписать всё, что крутится в голове.",
    "Обновить список покупок.",
    "Удалить/архивировать лишнее из телефона.",
    "Очень холодная вода на руки/лицо.",
    "Переодеться полностью.",
    "Намазать тело кремом с массажем (не \"аромат\", а контакт).",
    "Напрячь тело → отпустить (3–5 раз).",
    "Включить ОЧЕНЬ любимую песню.",
    "Музыка, под которую хочется двигаться.",
    "Нарисовать круг и заштриховать его цветной ручкой — заполнить полностью, не вылезая.",
    "Обвести свою ладонь, а внутри написать слово «тут».",
    "Нарисовать домик — с трубой, дымом, забором. Как в 6 лет.",
    "Нарисовать себя в виде дерева (корни — ноги, ветки — руки).",
    "Вырезать снежинку из салфетки (даже летом).",
    "Сложить бумажного журавлика (оригами — вспомнить схему).",
    "Сделать гармошку из полоски бумаги (сложить туда-сюда).",
    "Сделать цепочку из бумажных колечек (склеить или скрепить степлером).",
    "Слепить что-то из полимерной глины",
    "Сделать «березку» у стены (ноги вверх, плечи на полу) — 10 секунд.",
    "Упереться руками в стену и давить 10 секунд.",
    "Съесть один маленький кусочек шоколада (если есть) — очень медленно, не жуя сразу.",
    "Прочитать одну страницу любой книги (не больше, не меньше) — вслух или про себя, неважно.",
    "Прочитать на немецком 1 страницу",
    "Выучить 10 новых слов на немецком",
    "Выучить 10 новых слов на английском",
    "Разобрать и выучить английскую песню",
    "Разобрать и выучить немецкую песню",
    "Поиграть на гитаре",
    "Поиграть на пианино",
    "Поиграть на барабанах",
    "Танцевать что угодно",
    "Выучить стих",
    "Сочинить стих",
    "Написать одну страницу моей книги",
    "Написать слово каллиграфическим почерком",
    "Создать новую атмосферную доску в пинтерест",
    "Найти новые обои на телефон",
    "Найти новую сумку для вязания",
    "Сохранить 1 интерьер, который хотелось бы иметь",
    "Составить капсулу из вещей которые хотелось бы купить",
    "Набрать в поиске «cozy corners» (уютные углы) — посмотреть 5 минут без цели.",
    "Найти иллюстрацию к любимой детской книге (вспомнить, как она выглядела).",
    "Научиться играть в шахматы (сделать первый ход в онлайн-партии или решить одну задачу на мат в 1 ход).",
    "Сделать одно упражнение на осанку (например, «лодочка» или планка на 10 секунд).",
    "Написать одно предложение для своей книги (даже если потом удалишь).",
    "Повторить один старый немецкий урок (Duolingo или любой другой).",
    "Нарисовать один небольшой натюрморт (чашку, яблоко, книгу).",
    "Сложить из бумаги простой кораблик.",
    "Поздравить мысленно себя с тем, что ты запустила этого бота.",
    "Найти новый рецепт и прочитать его (как сказку).",
    "Сделать три глубоких вдоха и выдоха, положив руку на сердце.",
    "Написать себе письмо из будущего (одно предложение).",
]

application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    await update.message.reply_text(
        "🌸 Привет! Я — твой бот-рандомайзер радостей.\n\n"
        "Отправь /random — и я выберу для тебя одно радостное действие.\n"
        "Отправь /list — чтобы увидеть, сколько радостей в списке.\n\n"
        "Ты справишься. Просто начни с одного пункта."
    )

async def random_joy(update: Update, context):
    joy = random.choice(JOYS)
    await update.message.reply_text(f"🎲 Твоя радость сегодня:\n\n✨ {joy}\n\nПопробуй прямо сейчас. Ты этого заслуживаешь.")

async def list_count(update: Update, context):
    await update.message.reply_text(f"📋 В твоём списке сейчас {len(JOYS)} радостей.\n\nЧтобы получить одну — напиши /random")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("random", random_joy))
application.add_handler(CommandHandler("list", list_count))

def run_bot():
    print(f"🤖 Бот запущен! В списке {len(JOYS)} радостей.")
    application.run_polling()

flask_app = Flask(__name__)

@flask_app.route("/")
def index():
    return "🤖 Бот для радостей работает!"

def keep_alive():
    url = "https://" + os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")
    while True:
        time.sleep(600)
        try:
            import requests
            requests.get(url)
            print("💓 Пинг себе")
        except Exception as e:
            print(f"Пинг ошибка: {e}")

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    ping_thread = threading.Thread(target=keep_alive)
    ping_thread.daemon = True
    ping_thread.start()
    
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Сервер на порту {port}")
    flask_app.run(host="0.0.0.0", port=port)import os
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
