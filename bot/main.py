import logging
from aiogram import Bot, Dispatcher, executor, types
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)  # Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = "/webhook"
WEBHOOK_ROUTE = WEBHOOK_URL + WEBHOOK_PATH

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Пример логирования входящего сообщения
@dp.message_handler()
async def echo(message: types.Message):
    logging.info(f"Received message: {message.text} from user {message.from_user.id}")
    await message.reply(message.text)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_ROUTE)

async def on_shutdown(dp):
    await bot.delete_webhook()


async def main():
    # Configure environment variables
    WEBHOOK_HOST = '0.0.0.0'
    WEBHOOK_PORT = os.environ.get('PORT', 8080)

    # Set commands
    await bot.set_my_commands([
        types.BotCommand("start", "Запуск бота")
    ])

    # Configure and start application
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBHOOK_HOST,
        port=WEBHOOK_PORT,
    )

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())


