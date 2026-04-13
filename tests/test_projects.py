"""Tests for project tools."""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from utract_mcp.client import PlaneAPIError, PlaneClient
from utract_mcp.tools.projects import register_project_tools


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
    register_project_tools(mcp, mock_client, "test-workspace")
    tool_map = {t.name: t for t in mcp._tool_manager.list_tools()}
    return tool_map, mock_client


SAMPLE_PROJECT = {
    "id": "proj-uuid-1",
    "name": "Test Project",
    "identifier": "TEST",
    "description": "",
    "network": 2,
    "total_members": 1,
}


class TestListProjects:
    async def test_list_returns_paginated(self, tools):
        tool_map, mock_client = tools
        mock_client.get.return_value = [SAMPLE_PROJECT]
        tool = tool_map["plane_list_projects"]
        result = await tool.fn(per_page=20, cursor=None)
        data = json.loads(result)
        assert "results" in data
        assert data["results"][0]["id"] == "proj-uuid-1"

    async def test_list_handles_api_error(self, tools):
        tool_map, mock_client = tools
        mock_client.get.side_effect = PlaneAPIError(401, "Unauthorized")
        tool = tool_map["plane_list_projects"]
        result = await tool.fn(per_page=20, cursor=None)
        assert "Error 401" in result


class TestCreateProject:
    async def test_create_project(self, tools):
        tool_map, mock_client = tools
        mock_client.post.return_value = SAMPLE_PROJECT
        tool = tool_map["plane_create_project"]
        result = await tool.fn(name="Test Project", identifier="TEST")
        data = json.loads(result)
        assert data["id"] == "proj-uuid-1"
        mock_client.post.assert_called_once()

    async def test_create_project_sends_correct_body(self, tools):
        tool_map, mock_client = tools
        mock_client.post.return_value = SAMPLE_PROJECT
        tool = tool_map["plane_create_project"]
        await tool.fn(name="My Proj", identifier="MP", description="desc", network=0)
        _, kwargs = mock_client.post.call_args
        assert kwargs["data"]["name"] == "My Proj"
        assert kwargs["data"]["identifier"] == "MP"
        assert kwargs["data"]["description"] == "desc"


class TestGetProject:
    async def test_get_project(self, tools):
        tool_map, mock_client = tools
        mock_client.get.return_value = SAMPLE_PROJECT
        tool = tool_map["plane_get_project"]
        result = await tool.fn(project_id="proj-uuid-1")
        data = json.loads(result)
        assert data["name"] == "Test Project"

    async def test_get_project_not_found(self, tools):
        tool_map, mock_client = tools
        mock_client.get.side_effect = PlaneAPIError(404, "Resource not found.")
        tool = tool_map["plane_get_project"]
        result = await tool.fn(project_id="bad-uuid")
        assert "Error 404" in result


class TestUpdateProject:
    async def test_update_project(self, tools):
        tool_map, mock_client = tools
        updated = {**SAMPLE_PROJECT, "name": "Updated Name"}
        mock_client.patch.return_value = updated
        tool = tool_map["plane_update_project"]
        result = await tool.fn(project_id="proj-uuid-1", name="Updated Name")
        data = json.loads(result)
        assert data["name"] == "Updated Name"


class TestArchiveProject:
    async def test_archive_project(self, tools):
        tool_map, mock_client = tools
        mock_client.post.return_value = None
        tool = tool_map["plane_archive_project"]
        result = await tool.fn(project_id="proj-uuid-1")
        assert "proj-uuid-1" in result or "archived" in result.lower()
