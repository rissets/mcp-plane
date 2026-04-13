"""Tests for PlaneConfig and PlaneClient."""

from __future__ import annotations

import pytest

from utract_mcp.client import PlaneAPIError, PlaneClient
from utract_mcp.config import PlaneConfig


class TestPlaneConfig:
    def test_raises_without_api_key(self, monkeypatch):
        monkeypatch.delenv("PLANE_API_KEY", raising=False)
        monkeypatch.delenv("PLANE_WORKSPACE_SLUG", raising=False)
        with pytest.raises(ValueError, match="PLANE_API_KEY"):
            PlaneConfig()

    def test_raises_without_workspace_slug(self, monkeypatch):
        monkeypatch.setenv("PLANE_API_KEY", "test_key")
        monkeypatch.delenv("PLANE_WORKSPACE_SLUG", raising=False)
        with pytest.raises(ValueError, match="PLANE_WORKSPACE_SLUG"):
            PlaneConfig()

    def test_loads_from_env(self, monkeypatch):
        monkeypatch.setenv("PLANE_API_KEY", "env_key")
        monkeypatch.setenv("PLANE_WORKSPACE_SLUG", "env-slug")
        monkeypatch.setenv("PLANE_BASE_URL", "https://custom.plane.io")
        cfg = PlaneConfig()
        assert cfg.api_key == "env_key"
        assert cfg.workspace_slug == "env-slug"
        assert cfg.base_url == "https://custom.plane.io"

    def test_constructor_override(self):
        cfg = PlaneConfig(api_key="k", workspace_slug="s", base_url="https://x.io")
        assert cfg.api_key == "k"
        assert cfg.workspace_slug == "s"
        assert cfg.base_url == "https://x.io"


class TestPlaneAPIError:
    def test_str_representation(self):
        err = PlaneAPIError(404, "Not found")
        assert "404" in str(err)
        assert "Not found" in str(err)

    def test_attributes(self):
        err = PlaneAPIError(403, "Forbidden", {"detail": "no access"})
        assert err.status_code == 403
        assert err.message == "Forbidden"
        assert err.detail == {"detail": "no access"}
