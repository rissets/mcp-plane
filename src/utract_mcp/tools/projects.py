"""Project management tools for utract-mcp."""

from typing import Annotated, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_project_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register all project-related MCP tools."""

    @mcp.tool(name="plane_list_projects", annotations={"title": "List Projects", "readOnlyHint": True})
    async def plane_list_projects(
        per_page: Annotated[int, Field(description="Items per page (max 100)", ge=1, le=100)] = 20,
        cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None,
    ) -> str:
        """List all projects in the workspace."""
        try:
            data = await client.get(
                f"workspaces/{workspace_slug}/projects/",
                params={"per_page": per_page, "cursor": cursor},
            )
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_create_project", annotations={"title": "Create Project", "readOnlyHint": False})
    async def plane_create_project(
        name: Annotated[str, Field(description="Project name", min_length=1, max_length=255)],
        identifier: Annotated[str, Field(description="Short unique identifier e.g. PROJ", min_length=1, max_length=12)],
        description: Annotated[Optional[str], Field(description="Project description")] = None,
        network: Annotated[Optional[int], Field(description="Visibility: 0=Secret 2=Public", ge=0, le=2)] = 2,
    ) -> str:
        """Create a new project in the workspace."""
        try:
            body: dict = {"name": name, "identifier": identifier}
            if description is not None:
                body["description"] = description
            if network is not None:
                body["network"] = network
            data = await client.post(f"workspaces/{workspace_slug}/projects/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_get_project", annotations={"title": "Get Project", "readOnlyHint": True})
    async def plane_get_project(
        project_id: Annotated[str, Field(description="Project UUID")],
    ) -> str:
        """Get details of a specific project."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/")
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_update_project", annotations={"title": "Update Project", "readOnlyHint": False})
    async def plane_update_project(
        project_id: Annotated[str, Field(description="Project UUID")],
        name: Annotated[Optional[str], Field(description="New project name")] = None,
        description: Annotated[Optional[str], Field(description="New description")] = None,
        network: Annotated[Optional[int], Field(description="0=Secret 2=Public", ge=0, le=2)] = None,
    ) -> str:
        """Update a project's properties (partial update)."""
        try:
            body = {k: v for k, v in {"name": name, "description": description, "network": network}.items() if v is not None}
            data = await client.patch(f"workspaces/{workspace_slug}/projects/{project_id}/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_archive_project", annotations={"title": "Archive Project", "readOnlyHint": False})
    async def plane_archive_project(
        project_id: Annotated[str, Field(description="Project UUID to archive")],
    ) -> str:
        """Archive a project (soft delete)."""
        try:
            data = await client.post(f"workspaces/{workspace_slug}/projects/{project_id}/archive/", data={})
            return ok(data if data else {"message": f"Project {project_id} archived."})
        except Exception as exc:
            return handle_error(exc)
