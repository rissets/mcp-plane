"""Comment tools for utract-mcp."""

from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_comment_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register comment-related MCP tools."""

    @mcp.tool(name="plane_list_issue_comments", annotations={"title": "List Issue Comments", "readOnlyHint": True})
    async def plane_list_issue_comments(
        project_id: Annotated[str, Field(description="Project UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID")],
    ) -> str:
        """List all comments on a work item."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/")
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_create_issue_comment", annotations={"title": "Create Issue Comment", "readOnlyHint": False})
    async def plane_create_issue_comment(
        project_id: Annotated[str, Field(description="Project UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID")],
        comment_html: Annotated[str, Field(description="Comment body in HTML", min_length=1)],
    ) -> str:
        """Add a comment to a work item."""
        try:
            data = await client.post(
                f"workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/",
                data={"comment_html": comment_html},
            )
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_update_issue_comment", annotations={"title": "Update Issue Comment", "readOnlyHint": False})
    async def plane_update_issue_comment(
        project_id: Annotated[str, Field(description="Project UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID")],
        comment_id: Annotated[str, Field(description="Comment UUID")],
        comment_html: Annotated[str, Field(description="New comment HTML body", min_length=1)],
    ) -> str:
        """Update a comment body."""
        try:
            data = await client.patch(
                f"workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/",
                data={"comment_html": comment_html},
            )
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_delete_issue_comment", annotations={"title": "Delete Issue Comment", "readOnlyHint": False, "destructiveHint": True})
    async def plane_delete_issue_comment(
        project_id: Annotated[str, Field(description="Project UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID")],
        comment_id: Annotated[str, Field(description="Comment UUID to delete")],
    ) -> str:
        """Delete a comment from a work item."""
        try:
            await client.delete(f"workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/")
            return ok({"message": f"Comment {comment_id} deleted."})
        except Exception as exc:
            return handle_error(exc)
