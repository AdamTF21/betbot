import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bet_bot.settings")
django.setup()

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from telegram_bot.handlers import start, bet, balance, history, deposit, menu, search
from telegram_bot.config import TELEGRAM_BOT_TOKEN
from telegram_bot.scheduler import check_matches_and_notify


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(
        token=TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        bet.router,
        balance.router,
        history.router,
        deposit.router,
        menu.router,
        search.router,
    )

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_matches_and_notify, "interval", minutes=1)
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
