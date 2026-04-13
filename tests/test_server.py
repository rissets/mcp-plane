"""Tests for server creation and tool registration."""

from __future__ import annotations

import pytest
from unittest.mock import patch

from utract_mcp.config import PlaneConfig
from utract_mcp.server import create_server


class TestServerCreation:
    def test_create_server_returns_fastmcp(self):
        config = PlaneConfig(api_key="test-key", workspace_slug="test-ws")
        server = create_server(config)
        assert server is not None
        assert server.name == "plane_mcp"

    def test_all_tools_registered(self):
        config = PlaneConfig(api_key="test-key", workspace_slug="test-ws")
        server = create_server(config)
        tool_names = {t.name for t in server._tool_manager.list_tools()}

        expected_tools = {
            # projects
            "plane_list_projects",
            "plane_create_project",
            "plane_get_project",
            "plane_update_project",
            "plane_archive_project",
            # issues
            "plane_list_issues",
            "plane_create_issue",
            "plane_get_issue",
            "plane_get_issue_by_sequence",
            "plane_update_issue",
            "plane_delete_issue",
            "plane_search_issues",
            # states
            "plane_list_states",
            "plane_create_state",
            "plane_get_state",
            "plane_update_state",
            "plane_delete_state",
            # labels
            "plane_list_labels",
            "plane_create_label",
            "plane_get_label",
            "plane_update_label",
            "plane_delete_label",
            # cycles
            "plane_list_cycles",
            "plane_create_cycle",
            "plane_get_cycle",
            "plane_update_cycle",
            "plane_delete_cycle",
            "plane_add_issues_to_cycle",
            "plane_remove_issue_from_cycle",
            "plane_list_cycle_issues",
            # modules
            "plane_list_modules",
            "plane_create_module",
            "plane_get_module",
            "plane_update_module",
            "plane_delete_module",
            "plane_add_issues_to_module",
            "plane_remove_issue_from_module",
            "plane_list_module_issues",
            # members
            "plane_list_project_members",
            "plane_list_workspace_members",
            # comments
            "plane_list_issue_comments",
            "plane_create_issue_comment",
            "plane_update_issue_comment",
            "plane_delete_issue_comment",
            # activity
            "plane_list_issue_activity",
        }

        missing = expected_tools - tool_names
        assert not missing, f"Missing tools: {missing}"

    def test_tool_count(self):
        config = PlaneConfig(api_key="test-key", workspace_slug="test-ws")
        server = create_server(config)
        tools = server._tool_manager.list_tools()
        assert len(tools) >= 44  # at minimum all expected tools

    def test_create_server_without_config_uses_env(self, monkeypatch):
        monkeypatch.setenv("PLANE_API_KEY", "env-key")
        monkeypatch.setenv("PLANE_WORKSPACE_SLUG", "env-slug")
        server = create_server()
        assert server is not None
