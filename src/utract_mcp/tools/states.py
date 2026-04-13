"""State management tools for utract-mcp."""

from typing import Annotated, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_state_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register all state-related MCP tools."""

    @mcp.tool(name="plane_list_states", annotations={"title": "List States", "readOnlyHint": True})
    async def plane_list_states(
        project_id: Annotated[str, Field(description="Project UUID")],
    ) -> str:
        """List all workflow states in a project."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/states/")
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_create_state", annotations={"title": "Create State", "readOnlyHint": False})
    async def plane_create_state(
        project_id: Annotated[str, Field(description="Project UUID")],
        name: Annotated[str, Field(description="State name", min_length=1, max_length=255)],
        color: Annotated[str, Field(description="Hex color code e.g. #FF0000")],
        group: Annotated[Optional[str], Field(description="State group: backlog|unstarted|started|completed|cancelled")] = None,
        description: Annotated[Optional[str], Field(description="State description")] = None,
        sequence: Annotated[Optional[float], Field(description="Order within the group")] = None,
    ) -> str:
        """Create a new workflow state in a project."""
        try:
            body: dict = {"name": name, "color": color}
            for key, val in {"group": group, "description": description, "sequence": sequence}.items():
                if val is not None:
                    body[key] = val
            data = await client.post(f"workspaces/{workspace_slug}/projects/{project_id}/states/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_get_state", annotations={"title": "Get State", "readOnlyHint": True})
    async def plane_get_state(
        project_id: Annotated[str, Field(description="Project UUID")],
        state_id: Annotated[str, Field(description="State UUID")],
    ) -> str:
        """Get details of a specific state."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/states/{state_id}/")
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_update_state", annotations={"title": "Update State", "readOnlyHint": False})
    async def plane_update_state(
        project_id: Annotated[str, Field(description="Project UUID")],
        state_id: Annotated[str, Field(description="State UUID")],
        name: Annotated[Optional[str], Field(description="New name")] = None,
        color: Annotated[Optional[str], Field(description="New hex color")] = None,
        group: Annotated[Optional[str], Field(description="New group")] = None,
        description: Annotated[Optional[str], Field(description="New description")] = None,
    ) -> str:
        """Update a workflow state (partial update)."""
        try:
            body = {k: v for k, v in {"name": name, "color": color, "group": group, "description": description}.items() if v is not None}
            data = await client.patch(f"workspaces/{workspace_slug}/projects/{project_id}/states/{state_id}/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_delete_state", annotations={"title": "Delete State", "readOnlyHint": False, "destructiveHint": True})
    async def plane_delete_state(
        project_id: Annotated[str, Field(description="Project UUID")],
        state_id: Annotated[str, Field(description="State UUID to delete")],
    ) -> str:
        """Permanently delete a workflow state."""
        try:
            await client.delete(f"workspaces/{workspace_slug}/projects/{project_id}/states/{state_id}/")
            return ok({"message": f"State {state_id} deleted."})
        except Exception as exc:
            return handle_error(exc)
