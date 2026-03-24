"""Entry point for running the Telegram bot."""

import asyncio
import os

from telegram import Update
from telegram.ext import Application

from src.infrastructure.logger import get_logger

logger = get_logger("main")


async def run_bot(application: Application) -> None:
    """Run the Telegram bot with polling."""
    logger.info("Starting bot with polling...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)  # type: ignore[func-returns-value]


def main() -> None:
    """Main entry point."""
    token = os.getenv("TELEGRAM_TOKEN")

    if not token:
        logger.error("TELEGRAM_TOKEN not configured. Check .env file.")
        raise RuntimeError("TELEGRAM_TOKEN not configured")

    from src.main import create_application

    application = create_application(token)
    logger.info("Bot application created successfully")

    try:
        asyncio.run(run_bot(application))
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    finally:
        logger.info("Bot shutdown complete")


if __name__ == "__main__":
    main()
