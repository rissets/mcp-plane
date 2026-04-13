"""Member tools for utract-mcp."""

from typing import Annotated, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_member_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register member-related MCP tools."""

    @mcp.tool(name="plane_list_project_members", annotations={"title": "List Project Members", "readOnlyHint": True})
    async def plane_list_project_members(
        project_id: Annotated[str, Field(description="Project UUID")],
    ) -> str:
        """List all members of a project."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/members/")
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_list_workspace_members", annotations={"title": "List Workspace Members", "readOnlyHint": True})
    async def plane_list_workspace_members(
        per_page: Annotated[int, Field(description="Items per page", ge=1, le=100)] = 20,
        cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None,
    ) -> str:
        """List all members of the workspace."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/members/", params={"per_page": per_page, "cursor": cursor})
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)
