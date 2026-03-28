"""Tests for Referrals Keyboards."""

import pytest
from telegram import InlineKeyboardMarkup


class TestReferralsKeyboards:
    """Tests for ReferralsKeyboard class."""

    @pytest.mark.asyncio
    async def test_menu_keyboard_exists_and_has_buttons(self):
        """menu() keyboard exists and has buttons."""
        from src.bot.keyboards.referrals import ReferralsKeyboard

        keyboard = ReferralsKeyboard.menu()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0

        # Check for referral_redeem button
        buttons = keyboard.inline_keyboard
        assert any("referral_redeem" in btn.callback_data
                   for row in buttons for btn in row)

        # Check for referral_apply button
        assert any("referral_apply" in btn.callback_data
                   for row in buttons for btn in row)

    @pytest.mark.asyncio
    async def test_redeem_confirmation_keyboard_exists(self):
        """redeem_confirmation() keyboard exists."""
        from src.bot.keyboards.referrals import ReferralsKeyboard

        keyboard = ReferralsKeyboard.redeem_confirmation(credits=100)

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0

        # Check for confirm button with credits
        buttons = keyboard.inline_keyboard
        assert any("referral_redeem_confirm:100" in btn.callback_data
                   for row in buttons for btn in row)

        # Check for cancel button
        assert any("referral_cancel" in btn.callback_data
                   for row in buttons for btn in row)

    @pytest.mark.asyncio
    async def test_apply_code_keyboard_exists(self):
        """apply_code() keyboard exists."""
        from src.bot.keyboards.referrals import ReferralsKeyboard

        keyboard = ReferralsKeyboard.apply_code()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0

        # Check for back button
        buttons = keyboard.inline_keyboard
        assert any("referral_back" in btn.callback_data
                   for row in buttons for btn in row)

    @pytest.mark.asyncio
    async def test_back_to_menu_keyboard_exists(self):
        """back_to_menu() keyboard exists."""
        from src.bot.keyboards.referrals import ReferralsKeyboard

        keyboard = ReferralsKeyboard.back_to_menu()

        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0

        # Check for back button
        buttons = keyboard.inline_keyboard
        assert any("referral_back" in btn.callback_data
                   for row in buttons for btn in row)

    @pytest.mark.asyncio
    async def test_callback_data_patterns_are_correct(self):
        """Callback data patterns are correct."""
        from src.bot.keyboards.referrals import ReferralsKeyboard

        # Test menu callback patterns
        menu_keyboard = ReferralsKeyboard.menu()
        menu_buttons = menu_keyboard.inline_keyboard
        menu_callbacks = [btn.callback_data for row in menu_buttons for btn in row]

        assert "referral_redeem" in menu_callbacks
        assert "referral_apply" in menu_callbacks

        # Test redeem_confirmation callback patterns
        confirm_keyboard = ReferralsKeyboard.redeem_confirmation(credits=50)
        confirm_buttons = confirm_keyboard.inline_keyboard
        confirm_callbacks = [btn.callback_data for row in confirm_buttons for btn in row]

        assert "referral_redeem_confirm:50" in confirm_callbacks
        assert "referral_cancel" in confirm_callbacks

        # Test apply_code callback patterns
        apply_keyboard = ReferralsKeyboard.apply_code()
        apply_buttons = apply_keyboard.inline_keyboard
        apply_callbacks = [btn.callback_data for row in apply_buttons for btn in row]

        assert "referral_back" in apply_callbacks

        # Test back_to_menu callback patterns
        back_keyboard = ReferralsKeyboard.back_to_menu()
        back_buttons = back_keyboard.inline_keyboard
        back_callbacks = [btn.callback_data for row in back_buttons for btn in row]

        assert "referral_back" in back_callbacks
