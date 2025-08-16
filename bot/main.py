import asyncio
import logging
import os
# lkjnjn
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Проверка наличия токена
if not BOT_TOKEN:
    logging.error("Необходимо установить переменную окружения BOT_TOKEN")
    exit()

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.reply("Привет! Я эхо-бот. Просто напиши мне что-нибудь, и я повторю это.")


# Обработчик всех остальных сообщений
@dp.message()
async def echo_message(message: types.Message):
    await message.reply(message.text)


async def main():
    # Запуск Long Polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен!")






