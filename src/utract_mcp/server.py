"""utract-mcp server entry point."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from utract_mcp.client import PlaneClient
from utract_mcp.config import PlaneConfig
from utract_mcp.tools.activity import register_activity_tools
from utract_mcp.tools.comments import register_comment_tools
from utract_mcp.tools.cycles import register_cycle_tools
from utract_mcp.tools.issues import register_issue_tools
from utract_mcp.tools.labels import register_label_tools
from utract_mcp.tools.members import register_member_tools
from utract_mcp.tools.modules import register_module_tools
from utract_mcp.tools.projects import register_project_tools
from utract_mcp.tools.states import register_state_tools


def create_server(config: PlaneConfig | None = None) -> FastMCP:
    """Create and configure the FastMCP server with all tool groups.

    Args:
        config: Optional :class:`PlaneConfig`. If not provided, configuration is
            loaded from environment variables ``PLANE_API_KEY``,
            ``PLANE_WORKSPACE_SLUG``, and optionally ``PLANE_BASE_URL``.

    Returns:
        A configured :class:`~mcp.server.fastmcp.FastMCP` instance.
    """
    if config is None:
        config = PlaneConfig()

    client = PlaneClient(config)
    slug = config.workspace_slug

    mcp = FastMCP(
        "plane_mcp",
        instructions=(
            "MCP server for the Plane / utrack project-management platform. "
            f"Connected workspace: {slug}. "
            "Available tools cover projects, work items, states, labels, "
            "cycles, modules, members, comments, and activity logs."
        ),
    )

    register_project_tools(mcp, client, slug)
    register_issue_tools(mcp, client, slug)
    register_state_tools(mcp, client, slug)
    register_label_tools(mcp, client, slug)
    register_cycle_tools(mcp, client, slug)
    register_module_tools(mcp, client, slug)
    register_member_tools(mcp, client, slug)
    register_comment_tools(mcp, client, slug)
    register_activity_tools(mcp, client, slug)

    return mcp


def main() -> None:
    """CLI entry point – runs the server via stdio transport (default for uvx)."""
    server = create_server()
    server.run()


if __name__ == "__main__":
    main()
