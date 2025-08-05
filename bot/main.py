import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === 1. ТОКЕН И URL ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в переменных окружения")

# Получаем имя хоста от Render
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}"
else:
    WEBHOOK_URL = "http://localhost:8000"

# Порт и хост
APP_HOST = "0.0.0.0"
APP_PORT = int(os.getenv("PORT", 10000))

# === 2. СОЗДАНИЕ БОТА И ДИСПЕТЧЕРА (КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ) ===
bot = Bot(token=BOT_TOKEN)

# Важно: создаём Dispatcher БЕЗ bot, но явно привязываем его через контекст
dp = Dispatcher()

# Явно привязываем бота к диспетчеру через контекст
dp["bot"] = bot  # Это позволяет aiogram корректно обрабатывать update

# === 3. ОБРАБОТЧИКИ ===
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🚀 Бот успешно запущен на Render.com!")

@dp.message()
async def echo(message: Message):
    await message.answer(f"Вы сказали: {message.text}")

# === 4. ВЕБ-СЕРВЕР ===
async def on_startup(app):
    webhook_url = f"{WEBHOOK_URL}/webhook"
    try:
        await bot.set_webhook(webhook_url)
        logger.info(f"✅ Вебхук установлен: {webhook_url}")
    except Exception as e:
        logger.error(f"❌ Ошибка при установке вебхука: {e}")

async def on_shutdown(app):
    try:
        await bot.delete_webhook()
        await bot.session.close()
        logger.info("💤 Вебхук удалён, сессия бота закрыта")
    except Exception as e:
        logger.error(f"❌ Ошибка при завершении: {e}")

# === 5. ОБРАБОТЧИК ВЕБХУКА (БЕЗ ОШИБОК) ===
async def handle_webhook(request):
    try:
        # Получаем обновление от Telegram
        update = await request.json()

        # Ключевой момент: передаём ТОЛЬКО update
        # dp уже знает о bot через dp["bot"] = bot
        await dp.feed_update(update)

        return web.Response(status=200)
    except Exception as e:
        logger.error(f"❌ Ошибка при обработке вебхука: {e}")
        return web.Response(status=500)

# === 6. HEALTH CHECK (чтобы не было 404) ===
async def health_check(request):
    return web.Response(text="OK", content_type="text/plain")

# === 7. ЗАПУСК ВЕБ-ПРИЛОЖЕНИЯ ===
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app.router.add_post("/webhook", handle_webhook)
app.router.add_get("/", health_check)  # Для проверки Render

# === 8. ЗАПУСК СЕРВЕРА ===
if __name__ == "__main__":
    logger.info(f"🌍 Запуск сервера на http://{APP_HOST}:{APP_PORT}")
    web.run_app(app, host=APP_HOST, port=APP_PORT)
