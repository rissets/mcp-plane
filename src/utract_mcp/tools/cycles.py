"""Sprint/cycle management tools for utract-mcp."""

from typing import Annotated, List, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_cycle_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register all cycle (sprint) MCP tools."""

    @mcp.tool(name="plane_list_cycles", annotations={"title": "List Cycles", "readOnlyHint": True})
    async def plane_list_cycles(
        project_id: Annotated[str, Field(description="Project UUID")],
    ) -> str:
        """List all cycles (sprints) in a project."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/cycles/")
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_create_cycle", annotations={"title": "Create Cycle", "readOnlyHint": False})
    async def plane_create_cycle(
        project_id: Annotated[str, Field(description="Project UUID")],
        name: Annotated[str, Field(description="Cycle name", min_length=1, max_length=255)],
        start_date: Annotated[Optional[str], Field(description="Start date YYYY-MM-DD")] = None,
        end_date: Annotated[Optional[str], Field(description="End date YYYY-MM-DD")] = None,
        description: Annotated[Optional[str], Field(description="Cycle description")] = None,
    ) -> str:
        """Create a new cycle (sprint) in a project."""
        try:
            body: dict = {"name": name}
            for key, val in {"start_date": start_date, "end_date": end_date, "description": description}.items():
                if val is not None:
                    body[key] = val
            data = await client.post(f"workspaces/{workspace_slug}/projects/{project_id}/cycles/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_get_cycle", annotations={"title": "Get Cycle", "readOnlyHint": True})
    async def plane_get_cycle(
        project_id: Annotated[str, Field(description="Project UUID")],
        cycle_id: Annotated[str, Field(description="Cycle UUID")],
    ) -> str:
        """Get details of a specific cycle."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/")
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_update_cycle", annotations={"title": "Update Cycle", "readOnlyHint": False})
    async def plane_update_cycle(
        project_id: Annotated[str, Field(description="Project UUID")],
        cycle_id: Annotated[str, Field(description="Cycle UUID")],
        name: Annotated[Optional[str], Field(description="New name")] = None,
        start_date: Annotated[Optional[str], Field(description="New start date")] = None,
        end_date: Annotated[Optional[str], Field(description="New end date")] = None,
        description: Annotated[Optional[str], Field(description="New description")] = None,
    ) -> str:
        """Update a cycle (partial update)."""
        try:
            body = {k: v for k, v in {"name": name, "start_date": start_date, "end_date": end_date, "description": description}.items() if v is not None}
            data = await client.patch(f"workspaces/{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_delete_cycle", annotations={"title": "Delete Cycle", "readOnlyHint": False, "destructiveHint": True})
    async def plane_delete_cycle(
        project_id: Annotated[str, Field(description="Project UUID")],
        cycle_id: Annotated[str, Field(description="Cycle UUID to delete")],
    ) -> str:
        """Permanently delete a cycle."""
        try:
            await client.delete(f"workspaces/{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/")
            return ok({"message": f"Cycle {cycle_id} deleted."})
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_add_issues_to_cycle", annotations={"title": "Add Issues to Cycle", "readOnlyHint": False})
    async def plane_add_issues_to_cycle(
        project_id: Annotated[str, Field(description="Project UUID")],
        cycle_id: Annotated[str, Field(description="Cycle UUID")],
        issue_ids: Annotated[List[str], Field(description="List of work item UUIDs to add")],
    ) -> str:
        """Add work items to a cycle."""
        try:
            data = await client.post(
                f"workspaces/{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/",
                data={"issues": issue_ids},
            )
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_remove_issue_from_cycle", annotations={"title": "Remove Issue from Cycle", "readOnlyHint": False})
    async def plane_remove_issue_from_cycle(
        project_id: Annotated[str, Field(description="Project UUID")],
        cycle_id: Annotated[str, Field(description="Cycle UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID to remove")],
    ) -> str:
        """Remove a work item from a cycle."""
        try:
            await client.delete(f"workspaces/{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/")
            return ok({"message": f"Issue {issue_id} removed from cycle {cycle_id}."})
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_list_cycle_issues", annotations={"title": "List Cycle Issues", "readOnlyHint": True})
    async def plane_list_cycle_issues(
        project_id: Annotated[str, Field(description="Project UUID")],
        cycle_id: Annotated[str, Field(description="Cycle UUID")],
    ) -> str:
        """List all work items in a cycle."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/")
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)
