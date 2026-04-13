"""Tests for work item (issue) tools."""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from utract_mcp.client import PlaneAPIError, PlaneClient
from utract_mcp.tools.issues import register_issue_tools


@pytest.fixture
def mock_client():
    client = MagicMock(spec=PlaneClient)
    client.get = AsyncMock()
    client.post = AsyncMock()
    client.patch = AsyncMock()
    client.delete = AsyncMock()
    return client


@pytest.fixture
def tools(mock_client):
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("test")
    register_issue_tools(mcp, mock_client, "test-workspace")
    tool_map = {t.name: t for t in mcp._tool_manager.list_tools()}
    return tool_map, mock_client


SAMPLE_ISSUE = {
    "id": "issue-uuid-1",
    "name": "Fix bug",
    "priority": "high",
    "state": "state-uuid",
    "sequence_id": 1,
    "project": "proj-uuid",
}


class TestListIssues:
    async def test_list_returns_results(self, tools):
        tool_map, mock_client = tools
        mock_client.get.return_value = [SAMPLE_ISSUE]
        tool = tool_map["plane_list_issues"]
        result = await tool.fn(project_id="proj-uuid", per_page=20)
        data = json.loads(result)
        assert data["results"][0]["id"] == "issue-uuid-1"

    async def test_list_with_priority_filter(self, tools):
        tool_map, mock_client = tools
        mock_client.get.return_value = [SAMPLE_ISSUE]
        tool = tool_map["plane_list_issues"]
        await tool.fn(project_id="proj-uuid", per_page=20, priority="high")
        _, kwargs = mock_client.get.call_args
        assert kwargs["params"]["priority"] == "high"


class TestCreateIssue:
    async def test_create_issue_minimal(self, tools):
        tool_map, mock_client = tools
        mock_client.post.return_value = SAMPLE_ISSUE
        tool = tool_map["plane_create_issue"]
        result = await tool.fn(project_id="proj-uuid", name="Fix bug")
        data = json.loads(result)
        assert data["id"] == "issue-uuid-1"

    async def test_create_issue_full(self, tools):
        tool_map, mock_client = tools
        mock_client.post.return_value = SAMPLE_ISSUE
        tool = tool_map["plane_create_issue"]
        await tool.fn(
            project_id="proj-uuid",
            name="Full issue",
            description_html="<p>desc</p>",
            priority="medium",
            state="state-uuid",
            assignees=["user-uuid"],
            labels=["label-uuid"],
            start_date="2025-01-01",
            target_date="2025-01-15",
            is_draft=False,
        )
        _, kwargs = mock_client.post.call_args
        body = kwargs["data"]
        assert body["name"] == "Full issue"
        assert body["priority"] == "medium"
        assert body["assignees"] == ["user-uuid"]


class TestGetIssue:
    async def test_get_issue(self, tools):
        tool_map, mock_client = tools
        mock_client.get.return_value = SAMPLE_ISSUE
        tool = tool_map["plane_get_issue"]
        result = await tool.fn(project_id="proj-uuid", issue_id="issue-uuid-1")
        data = json.loads(result)
        assert data["name"] == "Fix bug"


class TestGetIssueBySequence:
    async def test_get_by_sequence(self, tools):
        tool_map, mock_client = tools
        mock_client.get.return_value = SAMPLE_ISSUE
        tool = tool_map["plane_get_issue_by_sequence"]
        result = await tool.fn(project_id="proj-uuid", sequence_id=1)
        data = json.loads(result)
        assert data["sequence_id"] == 1


class TestUpdateIssue:
    async def test_update_issue(self, tools):
        tool_map, mock_client = tools
        updated = {**SAMPLE_ISSUE, "priority": "low"}
        mock_client.patch.return_value = updated
        tool = tool_map["plane_update_issue"]
        result = await tool.fn(project_id="proj-uuid", issue_id="issue-uuid-1", priority="low")
        data = json.loads(result)
        assert data["priority"] == "low"

    async def test_update_only_sends_non_null_fields(self, tools):
        tool_map, mock_client = tools
        mock_client.patch.return_value = SAMPLE_ISSUE
        tool = tool_map["plane_update_issue"]
        await tool.fn(project_id="proj-uuid", issue_id="issue-uuid-1", name="New name")
        _, kwargs = mock_client.patch.call_args
        body = kwargs["data"]
        assert "name" in body
        assert body["name"] == "New name"
        # None fields should not be sent
        assert "priority" not in body


class TestDeleteIssue:
    async def test_delete_issue(self, tools):
        tool_map, mock_client = tools
        mock_client.delete.return_value = None
        tool = tool_map["plane_delete_issue"]
        result = await tool.fn(project_id="proj-uuid", issue_id="issue-uuid-1")
        data = json.loads(result)
        assert "deleted" in data["message"].lower() or "issue-uuid-1" in data["message"]


class TestSearchIssues:
    async def test_search_issues(self, tools):
        tool_map, mock_client = tools
        mock_client.get.return_value = [SAMPLE_ISSUE]
        tool = tool_map["plane_search_issues"]
        result = await tool.fn(project_id="proj-uuid", query="bug")
        data = json.loads(result)
        assert data["results"][0]["id"] == "issue-uuid-1"

    async def test_search_passes_query_param(self, tools):
        tool_map, mock_client = tools
        mock_client.get.return_value = []
        tool = tool_map["plane_search_issues"]
        await tool.fn(project_id="proj-uuid", query="critical bug")
        _, kwargs = mock_client.get.call_args
        assert kwargs["params"]["search"] == "critical bug"
