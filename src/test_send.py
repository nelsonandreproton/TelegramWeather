"""
One-shot test script: fetches weather data and sends a message to Telegram.
Run with: uv run python src/test_send.py
"""
import asyncio
import os

from dotenv import load_dotenv

from telegram import format_message, send_message
from weather import fetch_weather

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
LATITUDE = float(os.environ["LATITUDE"])
LONGITUDE = float(os.environ["LONGITUDE"])


async def main() -> None:
    print("Fetching weather data...")
    data = await fetch_weather(LATITUDE, LONGITUDE)
    message = format_message(data)
    print("\n--- Message preview ---")
    print(message)
    print("-----------------------\n")
    print("Sending to Telegram...")
    await send_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, message)
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
