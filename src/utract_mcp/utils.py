"""Shared response helpers for utract-mcp tools."""

from __future__ import annotations

import json
from typing import Any

from utract_mcp.client import PlaneAPIError


def ok(data: Any) -> str:
    """Serialize successful response to JSON string."""
    return json.dumps(data, indent=2, default=str)


def paginated(response: dict[str, Any]) -> str:
    """Serialize a paginated Plane API response."""
    return json.dumps(
        {
            "results": response.get("results", []),
            "total_results": response.get("total_results", len(response.get("results", []))),
            "total_pages": response.get("total_pages", 1),
            "count": response.get("count", len(response.get("results", []))),
            "next_cursor": response.get("next_cursor"),
            "prev_cursor": response.get("prev_cursor"),
            "next_page_results": response.get("next_page_results", False),
            "prev_page_results": response.get("prev_page_results", False),
        },
        indent=2,
        default=str,
    )


def handle_error(exc: Exception) -> str:
    """Convert an exception to a user-facing error string."""
    if isinstance(exc, PlaneAPIError):
        return f"Error {exc.status_code}: {exc.message}"
    return f"Error: {exc}"
