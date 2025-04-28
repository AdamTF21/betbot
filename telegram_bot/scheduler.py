
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram_bot.services.check_matches import check_matches_and_notify

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        check_matches_and_notify,
        IntervalTrigger(seconds=60),
        name="Check matches and notify users",
        replace_existing=True,
    )
    scheduler.start()
