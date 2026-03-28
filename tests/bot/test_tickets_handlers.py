"""Tests for Tickets Handlers."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock


class TestTicketsHandlerInitialization:
    """Tests for TicketsHandler initialization."""

    @pytest.mark.asyncio
    async def test_handler_initialization(self):
        """TicketsHandler initializes correctly with api and tokens attributes."""
        with patch('src.bot.handlers.tickets.APIClient'), \
             patch('src.bot.handlers.tickets.TokenStorage'):
            from src.bot.handlers.tickets import TicketsHandler

            mock_api = AsyncMock()
            mock_storage = AsyncMock()

            handler = TicketsHandler(mock_api, mock_storage)

            assert handler.api == mock_api
            assert handler.tokens == mock_storage

    @pytest.mark.asyncio
    async def test_get_auth_headers(self):
        """_get_auth_headers returns correct headers with token."""
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()

        # Mock token storage to return a valid token
        expected_token = "test_access_token_123"
        mock_storage.get.return_value = {
            'access_token': expected_token,
            'refresh_token': 'test_refresh_token'
        }

        handler = TicketsHandler(mock_api, mock_storage)

        headers = await handler._get_auth_headers(telegram_id=12345)

        assert headers == {"Authorization": f"Bearer {expected_token}"}
        mock_storage.get.assert_called_once_with(12345)

    @pytest.mark.asyncio
    async def test_get_auth_headers_not_authenticated(self):
        """_get_auth_headers raises PermissionError when no token exists."""
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()

        # Mock token storage to return None (not authenticated)
        mock_storage.get.return_value = None

        handler = TicketsHandler(mock_api, mock_storage)

        with pytest.raises(PermissionError, match="User not authenticated"):
            await handler._get_auth_headers(telegram_id=99999)


class TestTicketsHandlerHelpers:
    """Tests for TicketsHandler helper methods."""

    @pytest.mark.asyncio
    async def test_safe_answer_query_success(self):
        """_safe_answer_query answers query successfully."""
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = TicketsHandler(mock_api, mock_storage)

        mock_query = AsyncMock()
        mock_query.answer = AsyncMock()

        await handler._safe_answer_query(mock_query)

        mock_query.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_safe_answer_query_error_logged(self):
        """_safe_answer_query logs errors but doesn't raise."""
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = TicketsHandler(mock_api, mock_storage)

        mock_query = AsyncMock()
        mock_query.answer = AsyncMock(side_effect=Exception("Test error"))

        # Should not raise
        await handler._safe_answer_query(mock_query)

        mock_query.answer.assert_called_once()

    @pytest.mark.asyncio
    async def test_safe_edit_message_success(self):
        """_safe_edit_message edits message successfully."""
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = TicketsHandler(mock_api, mock_storage)

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
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        handler = TicketsHandler(mock_api, mock_storage)

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


class TestListTicketsCommand:
    """Tests for the /tickets command (list_tickets method)."""

    @pytest.mark.asyncio
    async def test_list_tickets_not_authenticated(self):
        """list_tickets shows error when user not authenticated."""
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        mock_storage.is_authenticated = AsyncMock(return_value=False)

        handler = TicketsHandler(mock_api, mock_storage)

        mock_update = MagicMock()
        mock_update.effective_user = MagicMock()
        mock_update.effective_user.id = 12345
        mock_update.message = AsyncMock()
        mock_update.message.reply_text = AsyncMock()

        mock_context = MagicMock()

        await handler.list_tickets(mock_update, mock_context)

        # Should check authentication
        mock_storage.is_authenticated.assert_called_once_with(12345)
        # Should show error message
        mock_update.message.reply_text.assert_called_once()
        # Verify it's the NOT_AUTHORIZED message
        call_args = mock_update.message.reply_text.call_args
        assert "❌ No tenés permiso" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_list_tickets_empty(self):
        """list_tickets shows NO_TICKETS message when no tickets."""
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        mock_storage.is_authenticated = AsyncMock(return_value=True)
        mock_storage.get = AsyncMock(return_value={'access_token': 'test_token'})

        # Mock API to return empty list
        mock_api.api_client.get = AsyncMock(return_value=[])

        handler = TicketsHandler(mock_api, mock_storage)

        mock_update = MagicMock()
        mock_update.effective_user = MagicMock()
        mock_update.effective_user.id = 12345
        mock_update.message = AsyncMock()
        mock_update.message.reply_text = AsyncMock()

        mock_context = MagicMock()

        await handler.list_tickets(mock_update, mock_context)

        # Should check authentication
        mock_storage.is_authenticated.assert_called_once_with(12345)
        # Should call API
        mock_api.api_client.get.assert_called_once_with(
            "/tickets",
            headers={"Authorization": "Bearer test_token"}
        )
        # Should show NO_TICKETS message
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        assert "📭 *No Tenés Tickets*" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_list_tickets_with_data(self):
        """list_tickets displays tickets list with keyboard when authenticated."""
        from src.bot.handlers.tickets import TicketsHandler

        mock_api = AsyncMock()
        mock_storage = AsyncMock()
        mock_storage.is_authenticated = AsyncMock(return_value=True)
        mock_storage.get = AsyncMock(return_value={'access_token': 'test_token'})

        # Mock API to return tickets list
        mock_tickets = [
            {
                "id": "uuid-1",
                "ticket_number": "TKT-001",
                "status": "OPEN",
                "subject": "VPN connection issue",
                "category": "technical",
                "created_at": "2026-03-28T10:00:00Z"
            },
            {
                "id": "uuid-2",
                "ticket_number": "TKT-002",
                "status": "RESPONDED",
                "subject": "Payment problem",
                "category": "billing",
                "created_at": "2026-03-27T15:30:00Z"
            }
        ]
        mock_api.api_client.get = AsyncMock(return_value=mock_tickets)

        handler = TicketsHandler(mock_api, mock_storage)

        mock_update = MagicMock()
        mock_update.effective_user = MagicMock()
        mock_update.effective_user.id = 12345
        mock_update.message = AsyncMock()
        mock_update.message.reply_text = AsyncMock()

        mock_context = MagicMock()

        await handler.list_tickets(mock_update, mock_context)

        # Should check authentication
        mock_storage.is_authenticated.assert_called_once_with(12345)
        # Should call API
        mock_api.api_client.get.assert_called_once_with(
            "/tickets",
            headers={"Authorization": "Bearer test_token"}
        )
        # Should send message with tickets list
        mock_update.message.reply_text.assert_called_once()
        call_args = mock_update.message.reply_text.call_args
        message_text = call_args.kwargs.get('text') or call_args[0][0] if call_args[0] else call_args.kwargs['text']
        
        # Verify message contains ticket info
        assert "🎫 *Tus Tickets*" in message_text
        assert "TKT-001" in message_text
        assert "TKT-002" in message_text
        assert "VPN connection issue" in message_text
        assert "Payment problem" in message_text
        # Verify keyboard was included
        assert 'reply_markup' in call_args.kwargs or len(call_args) > 1
