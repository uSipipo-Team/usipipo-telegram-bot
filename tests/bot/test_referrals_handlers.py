"""Tests for Referrals Handlers."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestReferralsHandlerInitialization:
    """Tests for ReferralsHandler initialization."""

    @pytest.mark.asyncio
    async def test_handler_initialization(self):
        """ReferralsHandler initializes correctly with api and tokens attributes."""
        with patch('src.bot.handlers.referrals.APIClient'), \
             patch('src.bot.handlers.referrals.TokenStorage'):
            from src.bot.handlers.referrals import ReferralsHandler

            mock_api = AsyncMock()
            mock_storage = AsyncMock()

            handler = ReferralsHandler(mock_api, mock_storage)

            assert handler.api == mock_api
            assert handler.tokens == mock_storage

    @pytest.mark.asyncio
    async def test_get_auth_headers(self):
        """_get_auth_headers returns correct headers with token."""
        from src.bot.handlers.referrals import ReferralsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()

        # Mock token storage to return a valid token
        expected_token = "test_access_token_123"
        mock_storage.get.return_value = {
            'access_token': expected_token,
            'refresh_token': 'test_refresh_token'
        }

        handler = ReferralsHandler(mock_api, mock_storage)

        headers = await handler._get_auth_headers(telegram_id=12345)

        assert headers == {"Authorization": f"Bearer {expected_token}"}
        mock_storage.get.assert_called_once_with(12345)

    @pytest.mark.asyncio
    async def test_get_auth_headers_not_authenticated(self):
        """_get_auth_headers raises PermissionError when no token exists."""
        from src.bot.handlers.referrals import ReferralsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()

        # Mock token storage to return None (not authenticated)
        mock_storage.get.return_value = None

        handler = ReferralsHandler(mock_api, mock_storage)

        with pytest.raises(PermissionError, match="User not authenticated"):
            await handler._get_auth_headers(telegram_id=99999)


class TestReferralsHandlerHelpers:
    """Tests for ReferralsHandler helper methods."""

    @pytest.mark.asyncio
    async def test_safe_answer_query_success(self):
        """_safe_answer_query answers query successfully."""
        from src.bot.handlers.referrals import ReferralsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = ReferralsHandler(mock_api, mock_storage)

        mock_query = AsyncMock()
        mock_query.answer = AsyncMock()

        await handler._safe_answer_query(mock_query)

        mock_query.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_safe_answer_query_error_logged(self):
        """_safe_answer_query logs errors but doesn't raise."""
        from src.bot.handlers.referrals import ReferralsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = ReferralsHandler(mock_api, mock_storage)

        mock_query = AsyncMock()
        mock_query.answer = AsyncMock(side_effect=Exception("Test error"))

        # Should not raise
        await handler._safe_answer_query(mock_query)

        mock_query.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_safe_edit_message_success(self):
        """_safe_edit_message edits message successfully."""
        from src.bot.handlers.referrals import ReferralsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = ReferralsHandler(mock_api, mock_storage)

        mock_query = AsyncMock()
        mock_query.edit_message_text = AsyncMock()

        test_text = "Test message"
        test_markup = MagicMock()

        await handler._safe_edit_message(
            query=mock_query,
            context=MagicMock(),
            text=test_text,
            reply_markup=test_markup,
        )

        mock_query.edit_message_text.assert_called_once_with(
            text=test_text,
            reply_markup=test_markup,
            parse_mode="Markdown",
        )

    @pytest.mark.asyncio
    async def test_safe_edit_message_fallback_on_error(self):
        """_safe_edit_message uses fallback when edit fails."""
        from src.bot.handlers.referrals import ReferralsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = ReferralsHandler(mock_api, mock_storage)

        mock_query = AsyncMock()
        mock_query.edit_message_text = AsyncMock(side_effect=Exception("Edit failed"))
        mock_query.message.reply_text = AsyncMock()

        test_text = "Test fallback message"
        test_markup = MagicMock()

        await handler._safe_edit_message(
            query=mock_query,
            context=MagicMock(),
            text=test_text,
            reply_markup=test_markup,
        )

        # Edit should have been attempted
        mock_query.edit_message_text.assert_called_once()
        # Fallback should have been used
        mock_query.message.reply_text.assert_called_once_with(
            text=test_text,
            reply_markup=test_markup,
            parse_mode="Markdown",
        )


class TestShowReferralsCommand:
    """Tests for show_referrals command."""

    @pytest.mark.asyncio
    async def test_show_referrals_not_authenticated(self):
        """Shows error when user not authenticated."""
        from src.bot.handlers.referrals import ReferralsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = ReferralsHandler(mock_api, mock_storage)

        # Mock user and message
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_update = MagicMock()
        mock_update.effective_user = mock_user
        mock_update.message = AsyncMock()
        mock_context = MagicMock()

        # Mock is_authenticated to return False
        mock_storage.is_authenticated = AsyncMock(return_value=False)

        await handler.show_referrals(mock_update, mock_context)

        # Should show NOT_AUTHENTICATED error
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "❌ Debes estar autenticado" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_show_referrals_success(self):
        """Displays stats with keyboard when authenticated."""
        from src.bot.handlers.referrals import ReferralsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = ReferralsHandler(mock_api, mock_storage)

        # Mock user and message
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_update = MagicMock()
        mock_update.effective_user = mock_user
        mock_update.message = AsyncMock()
        mock_context = MagicMock()

        # Mock is_authenticated to return True
        mock_storage.is_authenticated = AsyncMock(return_value=True)

        # Mock _get_auth_headers
        handler._get_auth_headers = AsyncMock(return_value={"Authorization": "Bearer test_token"})

        # Mock API response
        mock_api.api_client.get = AsyncMock(return_value={
            "referral_code": "ABC123",
            "total_referrals": 5,
            "referral_credits": 10,
        })

        await handler.show_referrals(mock_update, mock_context)

        # Should call API
        mock_api.api_client.get.assert_called_once_with(
            "/referrals/me",
            headers={"Authorization": "Bearer test_token"},
        )

        # Should send message with keyboard
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "🎯 *Tu Programa de Referidos*" in call_args[1]["text"]
        assert "ABC123" in call_args[1]["text"]
        assert call_args[1]["parse_mode"] == "Markdown"
        # Verify keyboard was included
        assert call_args[1]["reply_markup"] is not None
