"""Tests for member, comment, and activity tools."""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from utract_mcp.client import PlaneClient
from utract_mcp.tools.activity import register_activity_tools
from utract_mcp.tools.comments import register_comment_tools
from utract_mcp.tools.members import register_member_tools


def _make_mock_client():
    client = MagicMock(spec=PlaneClient)
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.patch = AsyncMock()
    client.delete = AsyncMock()
    return client


def _make_tools(register_fn):
    from mcp.server.fastmcp import FastMCP
    client = _make_mock_client()
    mcp = FastMCP("test")
    register_fn(mcp, client, "test-workspace")
    tool_map = {t.name: t for t in mcp._tool_manager.list_tools()}
    return tool_map, client


class TestMemberTools:
    async def test_list_project_members(self):
        tool_map, mock_client = _make_tools(register_member_tools)
        mock_client.get.return_value = [{"id": "u1", "display_name": "Alice"}]
        result = await tool_map["plane_list_project_members"].fn(project_id="proj-uuid")
        data = json.loads(result)
        assert data["results"][0]["id"] == "u1"

    async def test_list_workspace_members(self):
        tool_map, mock_client = _make_tools(register_member_tools)
        mock_client.get.return_value = [{"id": "u1"}, {"id": "u2"}]
        result = await tool_map["plane_list_workspace_members"].fn(per_page=20)
        data = json.loads(result)
        assert data["total_results"] == 2


class TestCommentTools:
    async def test_list_comments(self):
        tool_map, mock_client = _make_tools(register_comment_tools)
        mock_client.get.return_value = [{"id": "cmt1", "comment_html": "<p>hi</p>"}]
        result = await tool_map["plane_list_issue_comments"].fn(project_id="proj-uuid", issue_id="i1")
        data = json.loads(result)
        assert data["results"][0]["id"] == "cmt1"

    async def test_create_comment(self):
        tool_map, mock_client = _make_tools(register_comment_tools)
        mock_client.post.return_value = {"id": "cmt1", "comment_html": "<p>hello</p>"}
        result = await tool_map["plane_create_issue_comment"].fn(
            project_id="proj-uuid", issue_id="i1", comment_html="<p>hello</p>"
        )
        data = json.loads(result)
        assert data["id"] == "cmt1"

    async def test_update_comment(self):
        tool_map, mock_client = _make_tools(register_comment_tools)
        mock_client.patch.return_value = {"id": "cmt1", "comment_html": "<p>updated</p>"}
        result = await tool_map["plane_update_issue_comment"].fn(
            project_id="proj-uuid", issue_id="i1", comment_id="cmt1", comment_html="<p>updated</p>"
        )
        data = json.loads(result)
        assert data["comment_html"] == "<p>updated</p>"

    async def test_delete_comment(self):
        tool_map, mock_client = _make_tools(register_comment_tools)
        mock_client.delete.return_value = None
        result = await tool_map["plane_delete_issue_comment"].fn(
            project_id="proj-uuid", issue_id="i1", comment_id="cmt1"
        )
        data = json.loads(result)
        assert "cmt1" in data["message"]


class TestActivityTools:
    async def test_list_activity(self):
        tool_map, mock_client = _make_tools(register_activity_tools)
        mock_client.get.return_value = [{"id": "act1", "field": "state", "new_value": "Done"}]
        result = await tool_map["plane_list_issue_activity"].fn(project_id="proj-uuid", issue_id="i1")
        data = json.loads(result)
        assert data["results"][0]["id"] == "act1"
