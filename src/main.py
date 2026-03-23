"""Telegram bot main module."""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from src.bot.handlers.basic import BasicHandler


handler = BasicHandler()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await handler.start_handler(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await handler.help_handler(update, context)


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command."""
    await update.message.reply_text("✅ Todos los sistemas operativos")


def create_application(token: str) -> Application:
    """Create and configure the Telegram application."""
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))

    return app
