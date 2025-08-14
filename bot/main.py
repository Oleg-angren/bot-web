import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook

# Настройка переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_ROUTE = WEBHOOK_URL + WEBHOOK_PATH

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_ROUTE)
    # Установите Webhook при запуске


async def on_shutdown(dp):
    # Удалите Webhook при остановке (опционально)
    await bot.delete_webhook()


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот, работающий на Render!")


async def main():
    # Настройка команд бота
    await bot.set_my_commands([
        types.BotCommand("start", "Запуск бота")
    ])

    # Запуск Webhook
    WEBAPP_HOST = "0.0.0.0"  # Слушаем все входящие соединения
    WEBAPP_PORT = int(os.environ.get("PORT", 8000))

    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,  # Пропускаем старые обновления
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

if __name__ == '__main__':
    asyncio.run(main())

