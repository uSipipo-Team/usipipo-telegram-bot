from src.infrastructure.api_client import APIClient


def test_api_client_initialization():
    client = APIClient(base_url="https://api.example.com", api_key="secret")
    assert client.base_url == "https://api.example.com"
    assert client.api_key == "secret"
