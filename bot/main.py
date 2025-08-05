import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import web
import os

# Логирование
logging.basicConfig(level=logging.INFO)

# Токен и URL
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_HOST = "0.0.0.0"  # Не меняй
APP_PORT = int(os.getenv("PORT", 10000))  # Render даст PORT
WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}.onrender.com"

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан")
if not WEBHOOK_URL:
    raise ValueError("RENDER_EXTERNAL_HOSTNAME не задан (убедитесь, что сервис задеплоен)")

# Бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🚀 Бот работает в веб-режиме на Render!")

# Эхо
@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# Запуск веб-сервера
async def on_startup(app):
    webhook_url = f"{WEBHOOK_URL}/webhook"
    await bot.set_webhook(webhook_url)
    logging.info(f"Webhook установлен: {webhook_url}")

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

# Обработчик вебхука
async def handle_webhook(request):
    update = await request.json()
    await dp.feed_update(bot, update)
    return web.Response()

# Создание веб-приложения
app = web.Application()
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)
app.router.add_post("/webhook", handle_webhook)

# Запуск
if __name__ == "__main__":
    web.run_app(app, host=APP_HOST, port=APP_PORT)
