import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web
import os

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === ТОКЕН И URL ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан")

RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}"
else:
    WEBHOOK_URL = "http://localhost:8000"

APP_HOST = "0.0.0.0"
APP_PORT = int(os.getenv("PORT", 10000))

# === БОТ И ДИСПЕТЧЕР ===
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# 🔑 КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: dp.bot = bot
dp.bot = bot

# === ОБРАБОТЧИКИ ===
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🚀 Бот работает!")

@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# === ВЕБ-СЕРВЕР ===
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
        logger.info("💤 Вебхук удалён")
    except Exception as e:
        logger.error(f"❌ Ошибка при завершении: {e}")

# === ОБРАБОТЧИК ВЕБХУКА ===
async def handle_webhook(request):
    try:
        update = await request.json()
        # Теперь dp.bot существует → feed_update работает
        await dp.feed_update(update)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"❌ Ошибка при обработке вебхука: {e}")
        return web.Response(status=500)

# === HEALTH CHECK ===
async def health_check(request):
    return web.Response(text="OK", content_type="text/plain")

# === ЗАПУСК ===
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app.router.add_post("/webhook", handle_webhook)
app.router.add_get("/", health_check)

if __name__ == "__main__":
    logger.info(f"🌍 Запуск на http://{APP_HOST}:{APP_PORT}")
    web.run_app(app, host=APP_HOST, port=APP_PORT)
