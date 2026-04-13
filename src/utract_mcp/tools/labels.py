"""Label management tools for utract-mcp."""

from typing import Annotated, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_label_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register all label-related MCP tools."""

    @mcp.tool(name="plane_list_labels", annotations={"title": "List Labels", "readOnlyHint": True})
    async def plane_list_labels(
        project_id: Annotated[str, Field(description="Project UUID")],
    ) -> str:
        """List all labels in a project."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/labels/")
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_create_label", annotations={"title": "Create Label", "readOnlyHint": False})
    async def plane_create_label(
        project_id: Annotated[str, Field(description="Project UUID")],
        name: Annotated[str, Field(description="Label name", min_length=1, max_length=255)],
        color: Annotated[str, Field(description="Hex color code e.g. #FF0000")],
        description: Annotated[Optional[str], Field(description="Label description")] = None,
        parent: Annotated[Optional[str], Field(description="Parent label UUID")] = None,
    ) -> str:
        """Create a new label in a project."""
        try:
            body: dict = {"name": name, "color": color}
            for key, val in {"description": description, "parent": parent}.items():
                if val is not None:
                    body[key] = val
            data = await client.post(f"workspaces/{workspace_slug}/projects/{project_id}/labels/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_get_label", annotations={"title": "Get Label", "readOnlyHint": True})
    async def plane_get_label(
        project_id: Annotated[str, Field(description="Project UUID")],
        label_id: Annotated[str, Field(description="Label UUID")],
    ) -> str:
        """Get a label by UUID."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/labels/{label_id}/")
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_update_label", annotations={"title": "Update Label", "readOnlyHint": False})
    async def plane_update_label(
        project_id: Annotated[str, Field(description="Project UUID")],
        label_id: Annotated[str, Field(description="Label UUID")],
        name: Annotated[Optional[str], Field(description="New name")] = None,
        color: Annotated[Optional[str], Field(description="New hex color")] = None,
        description: Annotated[Optional[str], Field(description="New description")] = None,
    ) -> str:
        """Update a label (partial update)."""
        try:
            body = {k: v for k, v in {"name": name, "color": color, "description": description}.items() if v is not None}
            data = await client.patch(f"workspaces/{workspace_slug}/projects/{project_id}/labels/{label_id}/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_delete_label", annotations={"title": "Delete Label", "readOnlyHint": False, "destructiveHint": True})
    async def plane_delete_label(
        project_id: Annotated[str, Field(description="Project UUID")],
        label_id: Annotated[str, Field(description="Label UUID to delete")],
    ) -> str:
        """Permanently delete a label."""
        try:
            await client.delete(f"workspaces/{workspace_slug}/projects/{project_id}/labels/{label_id}/")
            return ok({"message": f"Label {label_id} deleted."})
        except Exception as exc:
            return handle_error(exc)
