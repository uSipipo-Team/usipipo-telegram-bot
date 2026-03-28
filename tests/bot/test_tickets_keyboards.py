"""Tests for Tickets Keyboards."""

import pytest
from telegram import InlineKeyboardMarkup


class TestTicketsKeyboards:
    """Tests for TicketsKeyboard class."""

    @pytest.mark.asyncio
    async def test_tickets_list_keyboard_exists_and_has_buttons(self):
        """tickets_list() keyboard exists and has buttons."""
        from src.bot.keyboards.tickets import TicketsKeyboard

        # Create sample tickets data
        sample_tickets = [
            {"id": "1", "ticket_number": "#001", "status": "OPEN"},
            {"id": "2", "ticket_number": "#002", "status": "RESPONDED"},
            {"id": "3", "ticket_number": "#003", "status": "CLOSED"},
        ]

        keyboard = TicketsKeyboard.tickets_list(sample_tickets)

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0

        # Check for ticket buttons with callback_data
        buttons = keyboard.inline_keyboard
        assert any("ticket_view:1" in btn.callback_data for row in buttons for btn in row)
        assert any("ticket_view:2" in btn.callback_data for row in buttons for btn in row)
        assert any("ticket_view:3" in btn.callback_data for row in buttons for btn in row)

        # Check for back button
        assert any("tickets_back" in btn.callback_data for row in buttons for btn in row)

    @pytest.mark.asyncio
    async def test_ticket_detail_keyboard_exists(self):
        """ticket_detail() keyboard exists."""
        from src.bot.keyboards.tickets import TicketsKeyboard

        keyboard = TicketsKeyboard.ticket_detail(ticket_id="123")

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0

        # Check for expected buttons
        buttons = keyboard.inline_keyboard
        assert any("ticket_messages:123" in btn.callback_data for row in buttons for btn in row)
        assert any("ticket_send:123" in btn.callback_data for row in buttons for btn in row)
        assert any("ticket_close:123" in btn.callback_data for row in buttons for btn in row)
        assert any("tickets_back" in btn.callback_data for row in buttons for btn in row)

    @pytest.mark.asyncio
    async def test_categories_keyboard_exists_and_has_4_categories(self):
        """categories() keyboard exists and has 4 categories."""
        from src.bot.keyboards.tickets import TicketsKeyboard

        keyboard = TicketsKeyboard.categories()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 4  # 4 categories

        # Check for all 4 categories
        buttons = keyboard.inline_keyboard
        callbacks = [btn.callback_data for row in buttons for btn in row]

        assert "ticket_cat:technical" in callbacks
        assert "ticket_cat:billing" in callbacks
        assert "ticket_cat:services" in callbacks
        assert "ticket_cat:general" in callbacks

    @pytest.mark.asyncio
    async def test_ticket_actions_keyboard_exists(self):
        """ticket_actions() keyboard exists."""
        from src.bot.keyboards.tickets import TicketsKeyboard

        keyboard = TicketsKeyboard.ticket_actions(ticket_id="456")

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0

        # Check for expected buttons
        buttons = keyboard.inline_keyboard
        assert any("ticket_send:456" in btn.callback_data for row in buttons for btn in row)
        assert any("ticket_close:456" in btn.callback_data for row in buttons for btn in row)
        assert any("tickets_back" in btn.callback_data for row in buttons for btn in row)

    @pytest.mark.asyncio
    async def test_back_to_tickets_keyboard_exists(self):
        """back_to_tickets() keyboard exists."""
        from src.bot.keyboards.tickets import TicketsKeyboard

        keyboard = TicketsKeyboard.back_to_tickets()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0

        # Check for back button
        buttons = keyboard.inline_keyboard
        assert any("tickets_back" in btn.callback_data for row in buttons for btn in row)
