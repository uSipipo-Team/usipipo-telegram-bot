"""Telegram bot main module."""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from src.bot.handlers.basic import BasicHandler
from src.infrastructure.error_handler import error_handler
from src.infrastructure.logger import get_logger

logger = get_logger("main")
handler = BasicHandler()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /start")
    await handler.start_handler(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /help")
    await handler.help_handler(update, context)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    user = update.effective_user
    logger.info(f"User {user.id if user else 'unknown'} executed /status")
    if update.message:
        await update.message.reply_text("✅ Todos los sistemas operativos")


def create_application(token: str) -> Application:
    """Create and configure the Telegram application."""
    logger.info("Initializing Telegram bot application...")
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_error_handler(error_handler)

    logger.info("Bot handlers registered successfully")
    return app
