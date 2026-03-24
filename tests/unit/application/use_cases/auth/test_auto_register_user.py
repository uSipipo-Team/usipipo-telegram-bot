"""Tests for AutoRegisterUser use case."""

import pytest
from unittest.mock import AsyncMock

from src.application.use_cases.auth.auto_register_user import (
    AutoRegisterUser,
    AutoRegisterUserResult,
)


@pytest.fixture
def mock_backend_api():
    """Mock de BackendApiPort."""
    return AsyncMock()


@pytest.fixture
def mock_token_storage():
    """Mock de TokenStoragePort."""
    return AsyncMock()


@pytest.mark.asyncio
async def test_auto_register_success(
    mock_backend_api: AsyncMock,
    mock_token_storage: AsyncMock,
):
    """Test de auto-registro exitoso."""
    # Arrange
    telegram_id = 1058749165
    tokens = {
        "access_token": "test_access",
        "refresh_token": "test_refresh",
        "expires_in": 1800,
        "user_id": "uuid-1234",
    }
    mock_backend_api.auto_register.return_value = tokens

    use_case = AutoRegisterUser(mock_backend_api, mock_token_storage)

    # Act
    result = await use_case.execute(telegram_id)

    # Assert
    assert isinstance(result, AutoRegisterUserResult)
    assert result.success is True
    assert "¡Bienvenido" in result.message
    assert result.user_id == "uuid-1234"

    # Verify backend was called
    mock_backend_api.auto_register.assert_called_once_with(telegram_id)

    # Verify tokens were stored
    mock_token_storage.store.assert_called_once_with(
        telegram_id,
        "test_access",
        "test_refresh",
        1800,
    )
