"""Inline keyboards for Tickets feature."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class TicketsKeyboard:
    """Inline keyboards for ticket system."""

    @staticmethod
    def tickets_list(tickets: list) -> InlineKeyboardMarkup:
        """
        Keyboard for tickets list.

        Args:
            tickets: List of tickets to display

        Returns:
            InlineKeyboardMarkup: Keyboard with ticket buttons
        """
        keyboard = []

        for ticket in tickets[:10]:  # Limit to 10 tickets
            ticket_id = ticket.get("id", "")
            ticket_number = ticket.get("ticket_number", "#N/A")
            status = ticket.get("status", "UNKNOWN")

            # Status emoji
            status_emoji = {
                "OPEN": "🟢",
                "RESPONDED": "🟡",
                "RESOLVED": "🔵",
                "CLOSED": "🔴",
            }.get(status, "⚪")

            keyboard.append([
                InlineKeyboardButton(
                    f"{status_emoji} {ticket_number}",
                    callback_data=f"ticket_view:{ticket_id}",
                ),
            ])

        keyboard.append([
            InlineKeyboardButton("🔙 Volver", callback_data="tickets_back"),
        ])

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def ticket_detail(ticket_id: str) -> InlineKeyboardMarkup:
        """
        Keyboard for ticket detail view.

        Args:
            ticket_id: ID of the ticket

        Returns:
            InlineKeyboardMarkup: Keyboard with ticket actions
        """
        keyboard = [
            [
                InlineKeyboardButton("💬 Ver Mensajes", callback_data=f"ticket_messages:{ticket_id}"),
            ],
            [
                InlineKeyboardButton("📩 Enviar Mensaje", callback_data=f"ticket_send:{ticket_id}"),
            ],
            [
                InlineKeyboardButton("✅ Cerrar Ticket", callback_data=f"ticket_close:{ticket_id}"),
            ],
            [
                InlineKeyboardButton("🔙 Volver", callback_data="tickets_back"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def categories() -> InlineKeyboardMarkup:
        """
        Keyboard for category selection.

        Returns:
            InlineKeyboardMarkup: Keyboard with category buttons
        """
        keyboard = [
            [
                InlineKeyboardButton("🖥️ Técnico", callback_data="ticket_cat:technical"),
            ],
            [
                InlineKeyboardButton("💳 Pagos", callback_data="ticket_cat:billing"),
            ],
            [
                InlineKeyboardButton("📦 Servicios", callback_data="ticket_cat:services"),
            ],
            [
                InlineKeyboardButton("❓ General", callback_data="ticket_cat:general"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def ticket_actions(ticket_id: str) -> InlineKeyboardMarkup:
        """
        Keyboard for ticket actions.

        Args:
            ticket_id: ID of the ticket

        Returns:
            InlineKeyboardMarkup: Keyboard with action buttons
        """
        keyboard = [
            [
                InlineKeyboardButton("📩 Enviar Mensaje", callback_data=f"ticket_send:{ticket_id}"),
            ],
            [
                InlineKeyboardButton("✅ Cerrar Ticket", callback_data=f"ticket_close:{ticket_id}"),
            ],
            [
                InlineKeyboardButton("🔙 Volver", callback_data="tickets_back"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def back_to_tickets() -> InlineKeyboardMarkup:
        """
        Back to tickets list.

        Returns:
            InlineKeyboardMarkup: Keyboard with back button
        """
        keyboard = [
            [
                InlineKeyboardButton("🔙 Volver a Tickets", callback_data="tickets_back"),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)
