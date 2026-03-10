import asyncio
import logging
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from telegram import format_message, send_message
from weather import fetch_weather

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
LATITUDE = float(os.environ["LATITUDE"])
LONGITUDE = float(os.environ["LONGITUDE"])

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger(__name__)


def job() -> None:
    log.info("Running weather job")
    try:
        data = asyncio.run(fetch_weather(LATITUDE, LONGITUDE))
        message = format_message(data)
        asyncio.run(send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message))
        log.info("Weather message sent successfully")
    except Exception:
        log.exception("Weather job failed")


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Europe/Lisbon")
    scheduler.add_job(job, "cron", hour=6, minute=0)
    log.info("Scheduler started. Waiting for 06:00 Europe/Lisbon...")
    scheduler.start()
