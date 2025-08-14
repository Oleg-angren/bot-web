import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand, WebAppInfo

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    # Создаем кнопку для открытия Web App
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_button = types.KeyboardButton(
        text="Открыть Web App", web_app=WebAppInfo(url="https://bot-web-7x1x.onrender.com")  # Замените на URL вашего Web App
    )
    markup.add(web_app_button)
    await message.reply("Нажмите кнопку, чтобы открыть Web App:", reply_markup=markup)


async def main():
    # Установка команд бота
    commands = [
        BotCommand(command="start", description="Запуск бота"),
    ]
    await bot.set_my_commands(commands)
    logging.info("Бот запущен!")

    # Запуск Long Polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен!")



