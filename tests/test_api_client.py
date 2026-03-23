import pytest
from src.infrastructure.api_client import APIClient


def test_api_client_initialization():
    client = APIClient(base_url="http://localhost:8001")
    assert client.base_url == "http://localhost:8001"
