"""Tests para AuthHandler."""

import pytest
from unittest.mock import patch, AsyncMock


class TestAuthHandler:
    """Tests para AuthHandler."""

    @pytest.mark.asyncio
    async def test_auth_handler_initialization(self):
        """AuthHandler se inicializa correctamente."""
        with patch("src.bot.handlers.auth.APIClient"), patch("src.bot.handlers.auth.TokenStorage"):
            from src.bot.handlers.auth import AuthHandler

            mock_api = AsyncMock()
            mock_storage = AsyncMock()

            handler = AuthHandler(mock_api, mock_storage)

            assert handler.api == mock_api
            assert handler.tokens == mock_storage

    @pytest.mark.asyncio
    async def test_auth_messages_constants_exist(self):
        """AuthMessages constants están definidas."""
        from src.bot.keyboards.auth import AuthMessages

        assert hasattr(AuthMessages, "WELCOME_NEW_USER")
        assert hasattr(AuthMessages, "WELCOME_RETURNING_USER")
        assert hasattr(AuthMessages, "ME_AUTHENTICATED")
        assert hasattr(AuthMessages, "ME_NOT_AUTHENTICATED")
        assert hasattr(AuthMessages, "UNLINK_SUCCESS")

    @pytest.mark.asyncio
    async def test_welcome_messages_are_strings(self):
        """Los mensajes de bienvenida son strings."""
        from src.bot.keyboards.auth import AuthMessages

        assert isinstance(AuthMessages.WELCOME_NEW_USER, str)
        assert isinstance(AuthMessages.WELCOME_RETURNING_USER, str)
        assert "uSipipo" in AuthMessages.WELCOME_NEW_USER

    @pytest.mark.asyncio
    async def test_me_authenticated_message_has_placeholders(self):
        """El mensaje de perfil tiene placeholders."""
        from src.bot.keyboards.auth import AuthMessages

        assert "{user_id}" in AuthMessages.ME_AUTHENTICATED
        assert "{username}" in AuthMessages.ME_AUTHENTICATED
        assert "{plan_name}" in AuthMessages.ME_AUTHENTICATED

    @pytest.mark.asyncio
    async def test_config_settings_loaded(self):
        """Settings se cargan correctamente."""
        from src.infrastructure.config import settings

        assert settings.TELEGRAM_TOKEN is not None
        assert settings.BACKEND_URL is not None
        assert settings.REDIS_URL is not None

    @pytest.mark.asyncio
    async def test_redis_pool_class_exists(self):
        """RedisPool class existe."""
        from src.infrastructure.redis import RedisPool

        assert RedisPool is not None
        assert hasattr(RedisPool, "get_instance")
        assert hasattr(RedisPool, "get_client")
        assert hasattr(RedisPool, "health_check")

    @pytest.mark.asyncio
    async def test_token_storage_class_exists(self):
        """TokenStorage class existe."""
        from src.infrastructure.token_storage import TokenStorage

        assert TokenStorage is not None
        assert hasattr(TokenStorage, "store")
        assert hasattr(TokenStorage, "get")
        assert hasattr(TokenStorage, "delete")
        assert hasattr(TokenStorage, "is_authenticated")
        assert hasattr(TokenStorage, "needs_refresh")

    @pytest.mark.asyncio
    async def test_main_has_auth_commands(self):
        """main.py tiene los comandos de auth."""
        from src.main import me, unlink

        assert me is not None
        assert unlink is not None
