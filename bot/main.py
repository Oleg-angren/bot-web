import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import BotCommand, WebAppInfo

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Инициализация бота
bot = Bot(token=BOT_TOKEN)

# Инициализация диспетчера
dp = Dispatcher()  # Не передаем bot здесь
dp.include_router(router) # Добавляем роутер в диспетчер

# Создание роутера
router = Router()

@router.message(commands=["start"])  # Используем router.message
async def start_command(message: types.Message):
    # Создаем кнопку для открытия Web App
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    web_app_button = types.KeyboardButton(
        text="Открыть Web App", web_app=WebAppInfo(url="https://www.google.com")  # Замените на URL вашего Web App
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

    # Регистрация бота в диспетчере
    dp.include_router(router)  # Регистрируем роутер в диспетчере

    # Запуск Long Polling
    try:
        await dp.start_polling(bot)  # Передаем bot здесь
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен!")




