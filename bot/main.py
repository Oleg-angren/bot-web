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

# Бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("🚀 Бот запущен!")

# Эхо
@dp.message()
async def echo(message: Message):
    await message.answer(f"Ты сказал: {message.text}")

# === Health Check (для отладки или UptimeRobot) ===
async def health_check(request):
    return web.Response(text="OK", content_type="text/plain")

# Функция для запуска HTTP-сервера
async def run_http_server():
    app = web.Application()
    app.router.add_get("/health", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)  # Используем другой порт
    await site.start()
    logger.info("HTTP health check сервер запущен на порту 8080")

# Основная функция
async def main():
    # Запускаем HTTP-сервер и бота параллельно
    await asyncio.gather(
        run_http_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())

