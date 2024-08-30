import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from config import DEBUG
from database.main import init_db
from utils.register_routers_from_package import register_routers_from_package

load_dotenv()

if DEBUG:
    API_TOKEN = os.getenv('TEST_BOT_TOKEN')
else:
    API_TOKEN = os.getenv('BOT_TOKEN')

storage = MemoryStorage()


async def main() -> None:
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    register_routers_from_package('handlers', dp)
    init_db()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())