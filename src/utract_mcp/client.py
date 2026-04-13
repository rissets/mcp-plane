"""Plane / utrack API client with authentication and error handling."""

from __future__ import annotations

import json
from typing import Any

import httpx

from utract_mcp.config import PlaneConfig


class PlaneAPIError(Exception):
    """Raised when the Plane API returns an error."""

    def __init__(self, status_code: int, message: str, detail: Any = None) -> None:
        self.status_code = status_code
        self.message = message
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {message}")


class PlaneClient:
    """Async HTTP client for the Plane/utrack API."""

    def __init__(self, config: PlaneConfig) -> None:
        self._config = config
        self._base_url = config.base_url.rstrip("/")
        self._headers = {
            "X-API-Key": config.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _url(self, path: str) -> str:
        return f"{self._base_url}/api/v1/{path.lstrip('/')}"

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, data: dict[str, Any] | None = None) -> Any:
        return await self._request("POST", path, json=data)

    async def patch(self, path: str, data: dict[str, Any] | None = None) -> Any:
        return await self._request("PATCH", path, json=data)

    async def delete(self, path: str) -> Any:
        return await self._request("DELETE", path)

    async def _request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        url = self._url(path)
        async with httpx.AsyncClient(timeout=30.0) as http:
            try:
                response = await http.request(
                    method,
                    url,
                    headers=self._headers,
                    params={k: v for k, v in (params or {}).items() if v is not None},
                    json=json,
                )
                _handle_response_error(response)
                if response.status_code == 204:
                    return None
                return response.json()
            except PlaneAPIError:
                raise
            except httpx.TimeoutException:
                raise PlaneAPIError(408, "Request timed out. Try again later.")
            except httpx.RequestError as exc:
                raise PlaneAPIError(0, f"Network error: {exc}") from exc


def _handle_response_error(response: httpx.Response) -> None:
    if response.status_code < 400:
        return
    try:
        detail = response.json()
        message = detail.get("detail") or detail.get("error") or str(detail)
    except Exception:
        message = response.text or response.reason_phrase

    code = response.status_code
    if code == 401:
        raise PlaneAPIError(code, "Unauthorized. Check your API key.", message)
    if code == 403:
        raise PlaneAPIError(code, "Permission denied.", message)
    if code == 404:
        raise PlaneAPIError(code, "Resource not found. Verify the identifier.", message)
    if code == 429:
        raise PlaneAPIError(code, "Rate limit exceeded (60 req/min). Retry later.", message)
    raise PlaneAPIError(code, f"API error: {message}", message)
