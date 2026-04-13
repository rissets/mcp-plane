"""Activity feed tools for utract-mcp."""

from typing import Annotated, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_activity_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register activity-related MCP tools."""

    @mcp.tool(name="plane_list_issue_activity", annotations={"title": "List Issue Activity", "readOnlyHint": True})
    async def plane_list_issue_activity(
        project_id: Annotated[str, Field(description="Project UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID")],
        per_page: Annotated[int, Field(description="Items per page", ge=1, le=100)] = 20,
        cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None,
    ) -> str:
        """List the activity/history log for a work item."""
        try:
            data = await client.get(
                f"workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/history/",
                params={"per_page": per_page, "cursor": cursor},
            )
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)
