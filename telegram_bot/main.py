
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bet_bot.settings")
django.setup()

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from telegram_bot.handlers import start, bet
from telegram_bot.config import TELEGRAM_BOT_TOKEN

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(bet.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
