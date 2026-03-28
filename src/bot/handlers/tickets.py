"""Handlers for Ticket system."""

import logging
from typing import Any

from telegram import Update
from telegram.ext import CallbackQueryHandler, CommandHandler, ContextTypes

from src.bot.keyboards.messages_tickets import TicketsMessages
from src.bot.keyboards.tickets import TicketsKeyboard
from src.infrastructure.api_client import APIClient
from src.infrastructure.token_storage import TokenStorage

logger = logging.getLogger(__name__)


class TicketsHandler:
    """Handler for ticket system."""

    def __init__(self, api_client: APIClient, token_storage: TokenStorage):
        self.api = api_client
        self.tokens = token_storage
        logger.info("🎫 TicketsHandler initialized")

    async def _get_auth_headers(self, telegram_id: int) -> dict[str, str]:
        """Get authentication headers for user."""
        tokens = await self.tokens.get(telegram_id)
        if not tokens:
            raise PermissionError("User not authenticated")
        return {"Authorization": f"Bearer {tokens['access_token']}"}

    async def _safe_answer_query(self, query: Any) -> None:
        """Answer callback query safely."""
        try:
            await query.answer()
        except Exception as e:
            logger.error(f"Error answering query: {e}")

    async def _safe_edit_message(
        self,
        query: Any,
        context: ContextTypes.DEFAULT_TYPE,
        text: str,
        reply_markup: Any = None,
        parse_mode: str = "Markdown",
    ) -> None:
        """Edit message safely."""
        try:
            await query.edit_message_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )
        except Exception as e:
            logger.error(f"Error editing message: {e}")
            await query.message.reply_text(
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
            )

    async def list_tickets(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all user tickets."""
        if update.effective_user is None:
            return

        telegram_id = update.effective_user.id
        logger.info(f"🎫 User {telegram_id} listing tickets")

        try:
            # Check authentication
            if not await self.tokens.is_authenticated(telegram_id):
                if update.message:
                    await update.message.reply_text(
                        TicketsMessages.Error.NOT_AUTHORIZED,
                        parse_mode="Markdown",
                    )
                return

            # Get tickets
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get(
                "/tickets",
                headers=headers,
            )

            # Empty list
            if not response:
                if update.message:
                    await update.message.reply_text(
                        TicketsMessages.Menu.NO_TICKETS,
                        parse_mode="Markdown",
                    )
                return

            # Format tickets list
            tickets_text = ""
            for ticket in response:
                status_emoji = {
                    "OPEN": "🟢",
                    "RESPONDED": "🟡",
                    "RESOLVED": "🔵",
                    "CLOSED": "🔴",
                }.get(ticket.get("status", ""), "⚪")

                tickets_text += (
                    f"{status_emoji} *{ticket.get('ticket_number')}* - {ticket.get('subject')}\n"
                    f"Estado: {ticket.get('status')}\n"
                    f"Creado: {ticket.get('created_at', 'N/A')[:10]}\n\n"
                )

            # Format message
            message = TicketsMessages.Menu.TICKETS_LIST.format(tickets=tickets_text)

            # Send with keyboard
            if update.message:
                await update.message.reply_text(
                    text=message,
                    reply_markup=TicketsKeyboard.tickets_list(response),
                    parse_mode="Markdown",
                )

        except Exception as e:
            logger.error(f"Error listing tickets: {e}")
            if update.message:
                await update.message.reply_text(
                    TicketsMessages.Error.SYSTEM_ERROR,
                    parse_mode="Markdown",
                )

    async def create_ticket(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start ticket creation flow."""
        if update.effective_user is None:
            return

        telegram_id = update.effective_user.id
        logger.info(f"🎫 User {telegram_id} creating ticket")

        try:
            # Check authentication
            if not await self.tokens.is_authenticated(telegram_id):
                if update.message:
                    await update.message.reply_text(
                        TicketsMessages.Error.NOT_AUTHORIZED,
                        parse_mode="Markdown",
                    )
                return

            # Show category selection
            if update.message:
                await update.message.reply_text(
                    text=TicketsMessages.Menu.CREATE_TICKET,
                    reply_markup=TicketsKeyboard.categories(),
                    parse_mode="Markdown",
                )

        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            if update.message:
                await update.message.reply_text(
                    TicketsMessages.Error.SYSTEM_ERROR,
                    parse_mode="Markdown",
                )

    async def select_category_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle category selection for ticket creation."""
        if update.effective_user is None or update.callback_query is None:
            return

        telegram_id = update.effective_user.id
        query = update.callback_query
        logger.info(f"🎫 User {telegram_id} selecting category")

        try:
            # Check authentication
            if not await self.tokens.is_authenticated(telegram_id):
                await self._safe_answer_query(query)
                await query.edit_message_text(
                    text=TicketsMessages.Error.NOT_AUTHORIZED,
                    parse_mode="Markdown",
                )
                return

            # Parse category from callback_data
            # Format: "ticket_cat:technical"
            category = query.data.split(":")[1]

            # Validate category
            valid_categories = ["technical", "billing", "services", "general"]
            if category not in valid_categories:
                await self._safe_answer_query(query)
                await query.edit_message_text(
                    text=TicketsMessages.Error.INVALID_CATEGORY,
                    parse_mode="Markdown",
                )
                return

            # Store category in user_data
            context.user_data["ticket_category"] = category

            # Prompt for subject (simplified: use default)
            # In full implementation: ConversationHandler for user input
            subject = f"Consulta de {category}"
            context.user_data["ticket_subject"] = subject

            # Create ticket
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.post(
                "/tickets",
                headers=headers,
                json={
                    "category": category,
                    "subject": subject,
                    "message": "Necesito ayuda con...",
                },
            )

            # Format success message
            message = TicketsMessages.Menu.TICKET_CREATED.format(
                ticket_number=response["ticket_number"],
                subject=subject,
            )

            await self._safe_edit_message(
                query=query,
                context=context,
                text=message,
                reply_markup=TicketsKeyboard.back_to_tickets(),
            )

        except Exception as e:
            logger.error(f"Error creating ticket: {e}")
            await self._safe_answer_query(query)
            await query.edit_message_text(
                text=TicketsMessages.Error.SYSTEM_ERROR,
                parse_mode="Markdown",
            )

    async def view_ticket_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle view ticket callback."""
        if update.effective_user is None or update.callback_query is None:
            return

        telegram_id = update.effective_user.id
        query = update.callback_query
        logger.info(f"🎫 User {telegram_id} viewing ticket")

        try:
            # Check authentication
            if not await self.tokens.is_authenticated(telegram_id):
                await self._safe_answer_query(query)
                await query.edit_message_text(
                    text=TicketsMessages.Error.NOT_AUTHORIZED,
                    parse_mode="Markdown",
                )
                return

            # Parse ticket_id from callback_data
            # Format: "ticket_view:uuid-123"
            ticket_id = query.data.split(":")[1]

            # Get ticket details
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.get(
                f"/tickets/{ticket_id}",
                headers=headers,
            )

            # Format message
            message = TicketsMessages.Menu.TICKET_DETAIL.format(
                ticket_number=response["ticket_number"],
                status=response["status"],
                subject=response["subject"],
                category=response["category"],
                created_at=response["created_at"][:10] if response.get("created_at") else "N/A",
                last_message="Sin mensajes aún",
            )

            await self._safe_edit_message(
                query=query,
                context=context,
                text=message,
                reply_markup=TicketsKeyboard.ticket_detail(ticket_id),
            )

        except Exception as e:
            logger.error(f"Error viewing ticket: {e}")
            await self._safe_answer_query(query)
            await query.edit_message_text(
                text=TicketsMessages.Error.SYSTEM_ERROR,
                parse_mode="Markdown",
            )

    async def close_ticket_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle close ticket callback."""
        if update.effective_user is None or update.callback_query is None:
            return

        telegram_id = update.effective_user.id
        query = update.callback_query
        logger.info(f"🎫 User {telegram_id} closing ticket")

        try:
            # Check authentication
            if not await self.tokens.is_authenticated(telegram_id):
                await self._safe_answer_query(query)
                await query.edit_message_text(
                    text=TicketsMessages.Error.NOT_AUTHORIZED,
                    parse_mode="Markdown",
                )
                return

            # Parse ticket_id from callback_data
            ticket_id = query.data.split(":")[1]

            # Close ticket
            headers = await self._get_auth_headers(telegram_id)
            response = await self.api.api_client.patch(
                f"/tickets/{ticket_id}/close",
                headers=headers,
                json={},
            )

            # Format success message
            message = TicketsMessages.Menu.TICKET_CLOSED.format(
                ticket_number=response["ticket_number"],
            )

            await self._safe_edit_message(
                query=query,
                context=context,
                text=message,
                reply_markup=TicketsKeyboard.back_to_tickets(),
            )

        except Exception as e:
            logger.error(f"Error closing ticket: {e}")
            await self._safe_answer_query(query)
            await query.edit_message_text(
                text=TicketsMessages.Error.SYSTEM_ERROR,
                parse_mode="Markdown",
            )


def get_tickets_handlers(api_client: APIClient, token_storage: TokenStorage):
    """Get tickets command handlers."""
    handler = TicketsHandler(api_client, token_storage)

    return [
        CommandHandler("nuevoticket", handler.create_ticket),
        CommandHandler("tickets", handler.list_tickets),
    ]


def get_tickets_callback_handlers(api_client: APIClient, token_storage: TokenStorage):
    """Get all tickets callback handlers."""
    handler = TicketsHandler(api_client, token_storage)

    return [
        CallbackQueryHandler(
            handler.view_ticket_callback,
            pattern=r"^ticket_view:[\w-]+$",
        ),
        CallbackQueryHandler(
            handler.select_category_callback,
            pattern=r"^ticket_cat:\w+$",
        ),
        CallbackQueryHandler(
            handler.close_ticket_callback,
            pattern=r"^ticket_close:[\w-]+$",
        ),
        CallbackQueryHandler(
            handler.list_tickets,
            pattern=r"^tickets_back$",
        ),
    ]
