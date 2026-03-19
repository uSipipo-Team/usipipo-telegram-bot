"""Telegram bot main module."""

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "¡Hola! 👋 Bienvenido al bot de uSipipo.\n\n"
        "Usa /help para ver los comandos disponibles."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await update.message.reply_text(
        "Comandos disponibles:\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar ayuda\n"
        "/status - Ver estado del servicio"
    )


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
