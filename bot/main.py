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

# Токен
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан")

# URL
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}.onrender.com"
else:
    WEBHOOK_URL = "http://localhost:8000"

# Порт
PORT = int(os.getenv("PORT", 10000))

# Бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🚀 Бот работает в веб-режиме!")

# Эхо
@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# Обработчик вебхука
async def handle_webhook(request):
    try:
        update = await request.json()
        await dp.feed_update(update)
        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return web.Response(status=500)

# Health check
async def health_check(request):
    return web.Response(text="OK")

# Создание веб-приложения
app = web.Application()
app.router.add_post("/webhook", handle_webhook)
app.router.add_get("/", health_check)

# Запуск
async def on_startup(app):
    webhook_url = f"{WEBHOOK_URL}/webhook"
    await bot.set_webhook(webhook_url)
    logger.info(f"✅ Webhook установлен: {webhook_url}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Запуск сервера
if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=PORT)

