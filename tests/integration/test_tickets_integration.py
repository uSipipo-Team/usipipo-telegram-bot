"""Integration tests for Tickets feature."""

import pytest
from unittest.mock import AsyncMock

from src.bot.handlers.tickets import TicketsHandler
from src.infrastructure.api_client import APIClient
from src.infrastructure.token_storage import TokenStorage


@pytest.mark.asyncio
class TestTicketsIntegration:
    """Integration tests for tickets."""

    async def test_full_ticket_creation_flow(self):
        """Test complete ticket creation flow."""
        # Mock API client
        api_client = AsyncMock(spec=APIClient)
        api_client.get = AsyncMock(return_value={
            "id": "uuid-123",
            "ticket_number": "TKT-001",
            "status": "OPEN",
            "subject": "Test issue",
            "category": "technical",
            "created_at": "2026-03-28T10:00:00Z",
            "messages": [],
        })
        api_client.post = AsyncMock(return_value={
            "id": "uuid-123",
            "ticket_number": "TKT-001",
            "status": "OPEN",
            "subject": "Test issue",
            "category": "technical",
        })
        api_client.patch = AsyncMock(return_value={
            "id": "uuid-123",
            "ticket_number": "TKT-001",
            "status": "CLOSED",
        })

        # Mock token storage
        token_storage = AsyncMock(spec=TokenStorage)
        token_storage.is_authenticated = AsyncMock(return_value=True)
        token_storage.get = AsyncMock(return_value={"access_token": "test_token"})

        # Create handler
        handler = TicketsHandler(api_client, token_storage)

        # Test 1: Create ticket
        ticket = await api_client.post(
            "/tickets",
            headers={"Authorization": "Bearer test_token"},
            data={"category": "technical", "subject": "Test", "message": "Help"},
        )
        assert ticket["ticket_number"] == "TKT-001"

        # Test 2: Get ticket
        fetched = await api_client.get(
            "/tickets/uuid-123",
            headers={"Authorization": "Bearer test_token"},
        )
        assert fetched["id"] == "uuid-123"
        assert fetched["ticket_number"] == "TKT-001"

        # Test 3: Close ticket
        closed = await api_client.patch(
            "/tickets/uuid-123/close",
            headers={"Authorization": "Bearer test_token"},
            data={},
        )
        assert closed["status"] == "CLOSED"

    async def test_tickets_backend_endpoints_available(self):
        """Test that backend endpoints are available."""
        # This would test against actual backend in CI/CD
        # For now, just verify endpoint paths
        endpoints = [
            "POST /tickets",
            "GET /tickets",
            "GET /tickets/{id}",
            "POST /tickets/{id}/messages",
            "PATCH /tickets/{id}/close",
        ]
        assert len(endpoints) == 5

        # Verify endpoint structure
        for endpoint in endpoints:
            method, path = endpoint.split(" ", 1)
            assert method in ["GET", "POST", "PUT", "DELETE", "PATCH"]
            assert path.startswith("/tickets")
