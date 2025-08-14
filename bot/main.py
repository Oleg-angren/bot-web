import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import BotCommand
from aiogram.webhook import WebAppInfo

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Настройка переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL вашего сервиса Render
WEBHOOK_PATH = "/webhook"
WEBHOOK_ROUTE = WEBHOOK_URL + WEBHOOK_PATH
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 8000))

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(bot: Bot):
    # Установка Webhook
    await bot.set_webhook(WEBHOOK_ROUTE, drop_pending_updates=True)

    # Установка команд бота
    commands = [
        BotCommand(command="start", description="Запуск бота"),
    ]
    await bot.set_my_commands(commands)
    logging.info("Бот запущен и готов к работе!")


async def on_shutdown(bot: Bot):
    logging.warning("Shutting down..")

    # Удаление webhook (опционально, но рекомендуется при остановке)
    await bot.delete_webhook(drop_pending_updates=True)

    logging.warning("Бот остановлен.")


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот, работающий на Render!")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Запуск dispatcher
    try:
        await dp.start_webhook(
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен!")


