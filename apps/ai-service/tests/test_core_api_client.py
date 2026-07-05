import httpx
import pytest

from app.clients.core_api_client import CoreApiClient, CoreApiError


@pytest.mark.asyncio
async def test_get_health_returns_parsed_json(monkeypatch):
    async def mock_request(self, method, url, **kwargs):
        request = httpx.Request(method, url)
        return httpx.Response(200, json={"status": "ok", "service": "core-api"}, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "request", mock_request)

    client = CoreApiClient(base_url="http://core-api-test")
    result = await client.get_health()

    assert result["status"] == "ok"
    assert result["service"] == "core-api"


@pytest.mark.asyncio
async def test_error_status_raises_core_api_error(monkeypatch):
    async def mock_request(self, method, url, **kwargs):
        request = httpx.Request(method, url)
        return httpx.Response(500, json={"error": "internal"}, request=request)

    monkeypatch.setattr(httpx.AsyncClient, "request", mock_request)

    client = CoreApiClient(base_url="http://core-api-test")
    with pytest.raises(CoreApiError) as exc_info:
        await client.get_health()

    assert exc_info.value.status_code == 500


@pytest.mark.asyncio
async def test_unreachable_host_raises_core_api_error(monkeypatch):
    async def mock_request(self, method, url, **kwargs):
        raise httpx.ConnectError("connection refused")

    monkeypatch.setattr(httpx.AsyncClient, "request", mock_request)

    client = CoreApiClient(base_url="http://core-api-test")
    with pytest.raises(CoreApiError):
        await client.get_health()
