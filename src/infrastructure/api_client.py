"""
Cliente HTTP para comunicación con el backend API.

Author: uSipipo Team
Version: 1.0.0
"""

import os
from typing import Any, Optional

import httpx

from src.infrastructure.logger import get_logger

logger = get_logger("api_client")

DEFAULT_BACKEND_URL = "https://usipipo.duckdns.org"
DEFAULT_API_PREFIX = "/api/v1"


class APIClient:
    """Cliente HTTP para el backend API de uSipipo."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_prefix: Optional[str] = None,
    ):
        self.base_url = (base_url or os.getenv("BACKEND_URL", DEFAULT_BACKEND_URL)).rstrip("/")
        self.api_prefix = api_prefix or os.getenv("API_PREFIX", DEFAULT_API_PREFIX)
        self._client: Optional[httpx.AsyncClient] = None
        logger.info(f"APIClient initialized: {self.base_url}{self.api_prefix}")

    async def _get_client(self) -> httpx.AsyncClient:
        """Retorna o crea el cliente HTTP async."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=f"{self.base_url}{self.api_prefix}",
                timeout=30.0,
                headers={"Content-Type": "application/json"},
            )
        return self._client

    async def get(self, endpoint: str, params: Optional[dict] = None) -> dict[str, Any]:
        """Realiza una petición GET al backend."""
        client = await self._get_client()
        logger.debug(f"GET {endpoint}")
        response = await client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, data: Optional[dict] = None) -> dict[str, Any]:
        """Realiza una petición POST al backend."""
        client = await self._get_client()
        logger.debug(f"POST {endpoint}")
        response = await client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def close(self) -> None:
        """Cierra el cliente HTTP."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            logger.info("APIClient closed")
