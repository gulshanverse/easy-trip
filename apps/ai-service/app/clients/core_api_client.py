"""
Internal client for calling core-api from the AI layer.

Per ADR-001 (docs/06-architecture/adr/adr-001-ai-service-database-boundary.md),
ai-service must never hold direct database credentials. All data reads/writes
go through core-api's internal API, keeping core-api as the single writer
and owner of data integrity for the system of record.
"""
import os
from typing import Any

import httpx

CORE_API_URL = os.environ.get("CORE_API_URL", "http://localhost:3001")
DEFAULT_TIMEOUT_SECONDS = 5.0


class CoreApiError(Exception):
    """Raised when core-api returns an error or is unreachable."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class CoreApiClient:
    """
    Thin, typed wrapper around core-api's internal API.

    This is intentionally the *only* place in ai-service that is allowed to
    reach outside the process for data. Agents must go through this client
    (or a higher-level tool built on top of it), never construct their own
    HTTP calls or DB connections.
    """

    def __init__(self, base_url: str = CORE_API_URL, timeout: float = DEFAULT_TIMEOUT_SECONDS):
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = f"{self._base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.request(method, url, **kwargs)
        except httpx.RequestError as exc:
            raise CoreApiError(f"core-api unreachable: {exc}") from exc

        if response.status_code >= 400:
            raise CoreApiError(
                f"core-api returned {response.status_code} for {method} {path}",
                status_code=response.status_code,
            )
        return response.json()

    async def get_health(self) -> dict[str, Any]:
        """Example call used by the ai-service health check to verify connectivity."""
        return await self._request("GET", "/api/v1/health")

    # Future methods (added as core-api exposes them, per docs/06-architecture/api-design-guidelines.md):
    #   async def get_user_profile(self, user_id: str) -> dict: ...
    #   async def get_trip_budget(self, trip_id: str) -> dict: ...
    #   async def search_flights(self, ...) -> dict: ...
    # Agents call these methods; they never see a connection string or ORM.
