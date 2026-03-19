"""Entry point for running the Telegram bot."""

import asyncio
import logging
import os

from telegram.ext import Application, CommandHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update, context):
    """Handle /start command."""
    await update.message.reply_text(
        "¡Hola! 👋 Bienvenido al bot de uSipipo.\n\n"
        "Usa /help para ver los comandos disponibles."
    )


async def help_command(update, context):
    """Handle /help command."""
    await update.message.reply_text(
        "Comandos disponibles:\n\n"
        "/start - Iniciar el bot\n"
        "/help - Mostrar ayuda\n"
        "/status - Ver estado del servicio"
    )


async def status(update, context):
    """Handle /status command."""
    await update.message.reply_text("✅ Todos los sistemas operativos")


async def main():
    """Run the Telegram bot."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN no configurado")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))

    logger.info("Bot iniciado...")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    asyncio.run(main())
