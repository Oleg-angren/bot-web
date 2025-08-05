import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv
import os

# Логирование
logging.basicConfig(level=logging.INFO)

# Загружаем токен
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен")

# Бот и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Обработчик /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🚀 Бот запущен! Работает на Render.com")

# Эхо
@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты сказал: {message.text}")

# Запуск
async def main():
    logging.info("Запуск бота...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
