"""Module management tools for utract-mcp."""

from typing import Annotated, List, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from utract_mcp.client import PlaneClient
from utract_mcp.utils import handle_error, ok, paginated


def register_module_tools(mcp: FastMCP, client: PlaneClient, workspace_slug: str) -> None:
    """Register all module-related MCP tools."""

    @mcp.tool(name="plane_list_modules", annotations={"title": "List Modules", "readOnlyHint": True})
    async def plane_list_modules(
        project_id: Annotated[str, Field(description="Project UUID")],
    ) -> str:
        """List all modules in a project."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/modules/")
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_create_module", annotations={"title": "Create Module", "readOnlyHint": False})
    async def plane_create_module(
        project_id: Annotated[str, Field(description="Project UUID")],
        name: Annotated[str, Field(description="Module name", min_length=1, max_length=255)],
        description: Annotated[Optional[str], Field(description="Module description")] = None,
        start_date: Annotated[Optional[str], Field(description="Start date YYYY-MM-DD")] = None,
        target_date: Annotated[Optional[str], Field(description="Target date YYYY-MM-DD")] = None,
        status: Annotated[Optional[str], Field(description="Status: backlog|in-progress|paused|completed|cancelled")] = None,
    ) -> str:
        """Create a new module in a project."""
        try:
            body: dict = {"name": name}
            for key, val in {"description": description, "start_date": start_date, "target_date": target_date, "status": status}.items():
                if val is not None:
                    body[key] = val
            data = await client.post(f"workspaces/{workspace_slug}/projects/{project_id}/modules/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_get_module", annotations={"title": "Get Module", "readOnlyHint": True})
    async def plane_get_module(
        project_id: Annotated[str, Field(description="Project UUID")],
        module_id: Annotated[str, Field(description="Module UUID")],
    ) -> str:
        """Get details of a specific module."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/modules/{module_id}/")
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_update_module", annotations={"title": "Update Module", "readOnlyHint": False})
    async def plane_update_module(
        project_id: Annotated[str, Field(description="Project UUID")],
        module_id: Annotated[str, Field(description="Module UUID")],
        name: Annotated[Optional[str], Field(description="New name")] = None,
        description: Annotated[Optional[str], Field(description="New description")] = None,
        start_date: Annotated[Optional[str], Field(description="New start date")] = None,
        target_date: Annotated[Optional[str], Field(description="New target date")] = None,
        status: Annotated[Optional[str], Field(description="New status")] = None,
    ) -> str:
        """Update a module (partial update)."""
        try:
            body = {k: v for k, v in {"name": name, "description": description, "start_date": start_date, "target_date": target_date, "status": status}.items() if v is not None}
            data = await client.patch(f"workspaces/{workspace_slug}/projects/{project_id}/modules/{module_id}/", data=body)
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_delete_module", annotations={"title": "Delete Module", "readOnlyHint": False, "destructiveHint": True})
    async def plane_delete_module(
        project_id: Annotated[str, Field(description="Project UUID")],
        module_id: Annotated[str, Field(description="Module UUID to delete")],
    ) -> str:
        """Permanently delete a module."""
        try:
            await client.delete(f"workspaces/{workspace_slug}/projects/{project_id}/modules/{module_id}/")
            return ok({"message": f"Module {module_id} deleted."})
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_add_issues_to_module", annotations={"title": "Add Issues to Module", "readOnlyHint": False})
    async def plane_add_issues_to_module(
        project_id: Annotated[str, Field(description="Project UUID")],
        module_id: Annotated[str, Field(description="Module UUID")],
        issue_ids: Annotated[List[str], Field(description="List of work item UUIDs to add")],
    ) -> str:
        """Add work items to a module."""
        try:
            data = await client.post(
                f"workspaces/{workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues/",
                data={"issues": issue_ids},
            )
            return ok(data)
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_remove_issue_from_module", annotations={"title": "Remove Issue from Module", "readOnlyHint": False})
    async def plane_remove_issue_from_module(
        project_id: Annotated[str, Field(description="Project UUID")],
        module_id: Annotated[str, Field(description="Module UUID")],
        issue_id: Annotated[str, Field(description="Work item UUID to remove")],
    ) -> str:
        """Remove a work item from a module."""
        try:
            await client.delete(f"workspaces/{workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues/{issue_id}/")
            return ok({"message": f"Issue {issue_id} removed from module {module_id}."})
        except Exception as exc:
            return handle_error(exc)

    @mcp.tool(name="plane_list_module_issues", annotations={"title": "List Module Issues", "readOnlyHint": True})
    async def plane_list_module_issues(
        project_id: Annotated[str, Field(description="Project UUID")],
        module_id: Annotated[str, Field(description="Module UUID")],
    ) -> str:
        """List all work items in a module."""
        try:
            data = await client.get(f"workspaces/{workspace_slug}/projects/{project_id}/modules/{module_id}/module-issues/")
            if isinstance(data, list):
                return ok({"results": data, "total_results": len(data), "count": len(data)})
            return paginated(data)
        except Exception as exc:
            return handle_error(exc)
