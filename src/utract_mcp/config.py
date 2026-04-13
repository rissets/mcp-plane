"""Configuration for utract-mcp, loaded from environment variables."""

from __future__ import annotations

import os


class PlaneConfig:
    """Runtime configuration for the Plane API connection."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        workspace_slug: str | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("PLANE_API_KEY", "")
        self.base_url = base_url or os.environ.get("PLANE_BASE_URL", "https://api.plane.so")
        self.workspace_slug = workspace_slug or os.environ.get("PLANE_WORKSPACE_SLUG", "")

        if not self.api_key:
            raise ValueError(
                "PLANE_API_KEY environment variable is required. "
                "Generate a Personal Access Token in Plane → Profile Settings → "
                "Personal Access Tokens."
            )
        if not self.workspace_slug:
            raise ValueError(
                "PLANE_WORKSPACE_SLUG environment variable is required. "
                "It is the slug shown in your Plane workspace URL, e.g. 'my-team'."
            )
