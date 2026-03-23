"""Handlers para comandos básicos del bot."""

from telegram import Update
from telegram.ext import ContextTypes

from src.bot.keyboards.main import BasicMessages


class BasicHandler:
    """Handler para comandos básicos."""

    def __init__(self):
        print("BasicHandler initialized")

    async def start_handler(self, update: Update, _context: ContextTypes.DEFAULT_TYPE):
        """Muestra el mensaje de bienvenida."""
        if update.message is None:
            return
        await update.message.reply_text(text=BasicMessages.START_TEXT)

    async def help_handler(self, update: Update, _context: ContextTypes.DEFAULT_TYPE):
        """Muestra la lista de comandos disponibles."""
        if update.message is None:
            return
        await update.message.reply_text(text=BasicMessages.HELP_TEXT, parse_mode="Markdown")
