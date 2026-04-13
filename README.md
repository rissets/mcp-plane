# utract-mcp

MCP server for the [Plane](https://plane.so) / utrack project management platform.

Exposes 44+ tools covering projects, work items, states, labels, cycles, modules, members, comments, and activity logs — ready to use with any MCP-compatible client (Claude Desktop, VS Code Copilot, Cursor, MCP Inspector, etc.).

## Installation

```bash
# Using uvx (recommended – no install needed)
uvx utract-mcp

# Or install globally
pip install utract-mcp
utract-mcp
```

## Configuration

Set these environment variables before running:

| Variable | Required | Description |
|---|---|---|
| `PLANE_API_KEY` | ✅ | Personal Access Token from Plane → Profile Settings |
| `PLANE_WORKSPACE_SLUG` | ✅ | Workspace slug from your Plane URL (e.g. `my-team`) |
| `PLANE_BASE_URL` | ❌ | Base URL for self-hosted instances (default: `https://api.plane.so`) |

## VS Code / Claude Desktop config

Add to your MCP client config:

```json
{
  "mcpServers": {
    "utract": {
      "command": "uvx",
      "args": ["utract-mcp"],
      "env": {
        "PLANE_API_KEY": "plane_api_...",
        "PLANE_WORKSPACE_SLUG": "my-team",
        "PLANE_BASE_URL": "https://utrack.bht.co.id"
      }
    }
  }
}
```

## Available Tools

### Projects
- `plane_list_projects` – List all workspace projects
- `plane_create_project` – Create a new project
- `plane_get_project` – Get project details
- `plane_update_project` – Update project properties
- `plane_archive_project` – Archive a project

### Work Items (Issues)
- `plane_list_issues` – List work items (with priority filter)
- `plane_create_issue` – Create a work item
- `plane_get_issue` – Get work item by UUID
- `plane_get_issue_by_sequence` – Get by sequence ID (e.g. PROJ-42)
- `plane_update_issue` – Update work item fields
- `plane_delete_issue` – Delete a work item
- `plane_search_issues` – Full-text search work items

### States
- `plane_list_states`, `plane_create_state`, `plane_get_state`, `plane_update_state`, `plane_delete_state`

### Labels
- `plane_list_labels`, `plane_create_label`, `plane_get_label`, `plane_update_label`, `plane_delete_label`

### Cycles (Sprints)
- `plane_list_cycles`, `plane_create_cycle`, `plane_get_cycle`, `plane_update_cycle`, `plane_delete_cycle`
- `plane_add_issues_to_cycle`, `plane_remove_issue_from_cycle`, `plane_list_cycle_issues`

### Modules
- `plane_list_modules`, `plane_create_module`, `plane_get_module`, `plane_update_module`, `plane_delete_module`
- `plane_add_issues_to_module`, `plane_remove_issue_from_module`, `plane_list_module_issues`

### Members
- `plane_list_project_members` – Members of a specific project
- `plane_list_workspace_members` – All workspace members

### Comments & Activity
- `plane_list_issue_comments`, `plane_create_issue_comment`, `plane_update_issue_comment`, `plane_delete_issue_comment`
- `plane_list_issue_activity` – Audit log of all changes to a work item

## License

MIT
