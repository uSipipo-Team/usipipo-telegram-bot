"""Tests for Tickets messages."""

import pytest
from bot.keyboards.messages_tickets import TicketsMessages


class TestTicketsMessagesMenu:
    """Test Menu category messages."""

    def test_menu_category_exists(self):
        """Verify Menu category exists and is accessible."""
        assert hasattr(TicketsMessages, "Menu")
        assert hasattr(TicketsMessages.Menu, "TICKETS_LIST")
        assert hasattr(TicketsMessages.Menu, "NO_TICKETS")
        assert hasattr(TicketsMessages.Menu, "TICKET_DETAIL")
        assert hasattr(TicketsMessages.Menu, "TICKET_MESSAGES_LIST")
        assert hasattr(TicketsMessages.Menu, "CREATE_TICKET")
        assert hasattr(TicketsMessages.Menu, "TICKET_CREATED")
        assert hasattr(TicketsMessages.Menu, "MESSAGE_SENT")
        assert hasattr(TicketsMessages.Menu, "TICKET_CLOSED")

    def test_tickets_list_has_correct_placeholders(self):
        """Verify TICKETS_LIST message has correct placeholders."""
        message = TicketsMessages.Menu.TICKETS_LIST
        assert "{tickets}" in message
        assert "🎫" in message
        assert "/nuevoticket" in message

    def test_ticket_detail_has_correct_placeholders(self):
        """Verify TICKET_DETAIL message has correct placeholders."""
        message = TicketsMessages.Menu.TICKET_DETAIL
        assert "{ticket_number}" in message
        assert "{status}" in message
        assert "{subject}" in message
        assert "{category}" in message
        assert "{created_at}" in message
        assert "{last_message}" in message

    def test_create_ticket_exists(self):
        """Verify CREATE_TICKET message exists and has content."""
        message = TicketsMessages.Menu.CREATE_TICKET
        assert "🎫" in message
        assert "Crear Nuevo Ticket" in message
        assert "Técnico" in message
        assert "Pagos" in message
        assert "Servicios" in message
        assert "General" in message


class TestTicketsMessagesError:
    """Test Error category messages."""

    def test_error_category_exists(self):
        """Verify Error category exists and has all required messages."""
        assert hasattr(TicketsMessages, "Error")
        assert hasattr(TicketsMessages.Error, "NOT_FOUND")
        assert hasattr(TicketsMessages.Error, "NOT_AUTHORIZED")
        assert hasattr(TicketsMessages.Error, "INVALID_CATEGORY")
        assert hasattr(TicketsMessages.Error, "SUBJECT_TOO_SHORT")
        assert hasattr(TicketsMessages.Error, "MESSAGE_TOO_SHORT")
        assert hasattr(TicketsMessages.Error, "SYSTEM_ERROR")

    def test_all_error_messages_exist(self):
        """Verify all error messages are non-empty strings."""
        errors = [
            TicketsMessages.Error.NOT_FOUND,
            TicketsMessages.Error.NOT_AUTHORIZED,
            TicketsMessages.Error.INVALID_CATEGORY,
            TicketsMessages.Error.SUBJECT_TOO_SHORT,
            TicketsMessages.Error.MESSAGE_TOO_SHORT,
            TicketsMessages.Error.SYSTEM_ERROR,
        ]
        for error in errors:
            assert isinstance(error, str)
            assert len(error) > 0
            assert "❌" in error
