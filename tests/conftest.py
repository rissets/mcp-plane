"""Shared pytest fixtures for utract-mcp tests."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from utract_mcp.client import PlaneClient
from utract_mcp.config import PlaneConfig
from utract_mcp.server import create_server


@pytest.fixture
def plane_config() -> PlaneConfig:
    config = MagicMock(spec=PlaneConfig)
    config.api_key = "plane_api_test_key"
    config.base_url = "https://api.plane.so"
    config.workspace_slug = "test-workspace"
    return config


@pytest.fixture
def mock_client(plane_config: PlaneConfig) -> PlaneClient:
    client = MagicMock(spec=PlaneClient)
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.patch = AsyncMock()
    client.delete = AsyncMock()
    return client


@pytest.fixture
def workspace_slug() -> str:
    return "test-workspace"


def make_paginated(results: list[Any]) -> dict:
    return {
        "results": results,
        "total_results": len(results),
        "total_pages": 1,
        "count": len(results),
        "next_cursor": None,
        "prev_cursor": None,
        "next_page_results": False,
        "prev_page_results": False,
    }
