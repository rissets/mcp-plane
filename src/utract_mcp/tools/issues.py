"""Work item (issue) tools for utract-mcp."""

from typing import Annotated, List, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_issue_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register all work-item (issue) MCP tools."""

    @mcp.tool(name="plane_list_issues", annotations={"title": "List Work Items", "readOnlyHint": True})
    async def plane_list_issues(
        project_id: Annotated[str, Field(description="Project UUID")],
        per_page: Annotated[int, Field(description="Items per page", ge=1, le=100)] = 20,
        cursor: Annotated[Optional[str], Field(description="Pagination cursor")] = None,
        priority: Annotated[Optional[str], Field(description="Filter by priority: urgent|high|medium|low|none")] = None,
    ) -> str:
        """List work items in a project with optional priority filter."""
        try:
            query_params: dict = {"per_page": per_page, "cursor": cursor}
            if priority:
                query_params["priority"] = priority
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/issues/", params=query_params)
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_create_issue", annotations={"title": "Create Work Item", "readOnlyHint": False})
    async def plane_create_issue(
        project_id: Annotated[str, Field(description="Project UUID")],
        name: Annotated[str, Field(description="Work item title", min_length=1, max_length=255)],
        description_html: Annotated[Optional[str], Field(description="HTML description")] = None,
        priority: Annotated[Optional[str], Field(description="Priority: urgent|high|medium|low|none")] = None,
        state: Annotated[Optional[str], Field(description="State UUID")] = None,
        assignees: Annotated[Optional[List[str]], Field(description="List of user UUIDs to assign")] = None,
        labels: Annotated[Optional[List[str]], Field(description="List of label UUIDs")] = None,
        start_date: Annotated[Optional[str], Field(description="Start date YYYY-MM-DD")] = None,
        target_date: Annotated[Optional[str], Field(description="Target date YYYY-MM-DD")] = None,
        parent: Annotated[Optional[str], Field(description="Parent work item UUID")] = None,
        is_draft: Annotated[Optional[bool], Field(description="Create as draft")] = None,
    ) -> str:
        """Create a new work item in a project."""
        try:
            body: dict = {"name": name}
            for key, val in {"description_html": description_html, "priority": priority, "state": state, "assignees": assignees, "labels": labels, "start_date": start_date, "target_date": target_date, "parent": parent, "is_draft": is_draft}.items():
                if val is not None:
                    body[key] = val
            data = await client.post(f"workspaces/{workspace_slug}/projects/{project_id}/issues/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_get_issue", annotations={"title": "Get Work Item", "readOnlyHint": True})
    async def plane_get_issue(
        project_id: Annotated[str, Field(description="Project UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID")],
    ) -> str:
        """Get details of a specific work item by UUID."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/")
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_get_issue_by_sequence", annotations={"title": "Get Work Item by Sequence ID", "readOnlyHint": True})
    async def plane_get_issue_by_sequence(
        project_id: Annotated[str, Field(description="Project UUID")],
        sequence_id: Annotated[int, Field(description="Work item sequence ID", ge=1)],
    ) -> str:
        """Get a work item using its human-readable sequence ID."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/issues/sequence-id/{sequence_id}/")
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_update_issue", annotations={"title": "Update Work Item", "readOnlyHint": False})
    async def plane_update_issue(
        project_id: Annotated[str, Field(description="Project UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID")],
        name: Annotated[Optional[str], Field(description="New title")] = None,
        description_html: Annotated[Optional[str], Field(description="New HTML description")] = None,
        priority: Annotated[Optional[str], Field(description="New priority")] = None,
        state: Annotated[Optional[str], Field(description="New state UUID")] = None,
        assignees: Annotated[Optional[List[str]], Field(description="New list of assignee UUIDs")] = None,
        labels: Annotated[Optional[List[str]], Field(description="New list of label UUIDs")] = None,
        start_date: Annotated[Optional[str], Field(description="New start date YYYY-MM-DD")] = None,
        target_date: Annotated[Optional[str], Field(description="New target date YYYY-MM-DD")] = None,
    ) -> str:
        """Update a work item properties (partial update)."""
        try:
            body = {k: v for k, v in {"name": name, "description_html": description_html, "priority": priority, "state": state, "assignees": assignees, "labels": labels, "start_date": start_date, "target_date": target_date}.items() if v is not None}
            data = await client.patch(f"workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_delete_issue", annotations={"title": "Delete Work Item", "readOnlyHint": False, "destructiveHint": True})
    async def plane_delete_issue(
        project_id: Annotated[str, Field(description="Project UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID to delete")],
    ) -> str:
        """Permanently delete a work item."""
        try:
            await client.delete(f"workspaces/{workspace_slug}/projects/{project_id}/issues/{issue_id}/")
            return ok({"message": f"Work item {issue_id} deleted."})
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_search_issues", annotations={"title": "Search Work Items", "readOnlyHint": True})
    async def plane_search_issues(
        project_id: Annotated[str, Field(description="Project UUID")],
        query: Annotated[str, Field(description="Search text", min_length=1)],
    ) -> str:
        """Search work items in a project by text."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/issues/", params={"search": query})
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)
