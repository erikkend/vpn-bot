# app/scheduler/setup.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from app.scheduler.jobs import check_and_deactivate_vpn


def setup_scheduler() -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="UTC")

    # Запускать каждые 5 минут
    scheduler.add_job(
        check_and_deactivate_vpn,
        trigger=IntervalTrigger(minutes=1),
        id="deactivate_expired_vpn_configs",
        replace_existing=True
    )

    return scheduler
