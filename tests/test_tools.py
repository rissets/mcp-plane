"""Tests for state, label, cycle, and module tools."""

import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from utract_mcp.client import PlaneClient
from utract_mcp.tools.cycles import register_cycle_tools
from utract_mcp.tools.labels import register_label_tools
from utract_mcp.tools.modules import register_module_tools
from utract_mcp.tools.states import register_state_tools


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


class TestStateTools:
    async def test_list_states(self):
        tool_map, mock_client = _make_tools(register_state_tools)
        mock_client.get.return_value = [{"id": "s1", "name": "Backlog"}]
        result = await tool_map["plane_list_states"].fn(project_id="proj-uuid")
        data = json.loads(result)
        assert data["results"][0]["id"] == "s1"

    async def test_create_state(self):
        tool_map, mock_client = _make_tools(register_state_tools)
        mock_client.post.return_value = {"id": "s1", "name": "Todo", "color": "#AAA"}
        result = await tool_map["plane_create_state"].fn(project_id="proj-uuid", name="Todo", color="#AAA")
        data = json.loads(result)
        assert data["name"] == "Todo"

    async def test_update_state(self):
        tool_map, mock_client = _make_tools(register_state_tools)
        mock_client.patch.return_value = {"id": "s1", "name": "Done", "color": "#0F0"}
        result = await tool_map["plane_update_state"].fn(project_id="proj-uuid", state_id="s1", name="Done")
        data = json.loads(result)
        assert data["name"] == "Done"

    async def test_delete_state(self):
        tool_map, mock_client = _make_tools(register_state_tools)
        mock_client.delete.return_value = None
        result = await tool_map["plane_delete_state"].fn(project_id="proj-uuid", state_id="s1")
        data = json.loads(result)
        assert "deleted" in data["message"].lower() or "s1" in data["message"]


class TestLabelTools:
    async def test_list_labels(self):
        tool_map, mock_client = _make_tools(register_label_tools)
        mock_client.get.return_value = [{"id": "l1", "name": "bug"}]
        result = await tool_map["plane_list_labels"].fn(project_id="proj-uuid")
        data = json.loads(result)
        assert data["results"][0]["id"] == "l1"

    async def test_create_label(self):
        tool_map, mock_client = _make_tools(register_label_tools)
        mock_client.post.return_value = {"id": "l1", "name": "bug", "color": "#F00"}
        result = await tool_map["plane_create_label"].fn(project_id="proj-uuid", name="bug", color="#F00")
        data = json.loads(result)
        assert data["name"] == "bug"

    async def test_delete_label(self):
        tool_map, mock_client = _make_tools(register_label_tools)
        mock_client.delete.return_value = None
        result = await tool_map["plane_delete_label"].fn(project_id="proj-uuid", label_id="l1")
        data = json.loads(result)
        assert "l1" in data["message"]


class TestCycleTools:
    async def test_list_cycles(self):
        tool_map, mock_client = _make_tools(register_cycle_tools)
        mock_client.get.return_value = [{"id": "c1", "name": "Sprint 1"}]
        result = await tool_map["plane_list_cycles"].fn(project_id="proj-uuid")
        data = json.loads(result)
        assert data["results"][0]["id"] == "c1"

    async def test_create_cycle(self):
        tool_map, mock_client = _make_tools(register_cycle_tools)
        mock_client.post.return_value = {"id": "c1", "name": "Sprint 1"}
        result = await tool_map["plane_create_cycle"].fn(project_id="proj-uuid", name="Sprint 1")
        data = json.loads(result)
        assert data["id"] == "c1"

    async def test_add_issues_to_cycle(self):
        tool_map, mock_client = _make_tools(register_cycle_tools)
        mock_client.post.return_value = [{"cycle": "c1", "issue": "i1"}]
        result = await tool_map["plane_add_issues_to_cycle"].fn(
            project_id="proj-uuid", cycle_id="c1", issue_ids=["i1", "i2"]
        )
        _, kwargs = mock_client.post.call_args
        assert kwargs["data"]["issues"] == ["i1", "i2"]

    async def test_remove_issue_from_cycle(self):
        tool_map, mock_client = _make_tools(register_cycle_tools)
        mock_client.delete.return_value = None
        result = await tool_map["plane_remove_issue_from_cycle"].fn(
            project_id="proj-uuid", cycle_id="c1", issue_id="i1"
        )
        data = json.loads(result)
        assert "i1" in data["message"]

    async def test_list_cycle_issues(self):
        tool_map, mock_client = _make_tools(register_cycle_tools)
        mock_client.get.return_value = [{"id": "i1", "name": "Task"}]
        result = await tool_map["plane_list_cycle_issues"].fn(project_id="proj-uuid", cycle_id="c1")
        data = json.loads(result)
        assert data["results"][0]["id"] == "i1"


class TestModuleTools:
    async def test_list_modules(self):
        tool_map, mock_client = _make_tools(register_module_tools)
        mock_client.get.return_value = [{"id": "m1", "name": "MVP"}]
        result = await tool_map["plane_list_modules"].fn(project_id="proj-uuid")
        data = json.loads(result)
        assert data["results"][0]["id"] == "m1"

    async def test_create_module(self):
        tool_map, mock_client = _make_tools(register_module_tools)
        mock_client.post.return_value = {"id": "m1", "name": "MVP"}
        result = await tool_map["plane_create_module"].fn(project_id="proj-uuid", name="MVP")
        data = json.loads(result)
        assert data["id"] == "m1"

    async def test_delete_module(self):
        tool_map, mock_client = _make_tools(register_module_tools)
        mock_client.delete.return_value = None
        result = await tool_map["plane_delete_module"].fn(project_id="proj-uuid", module_id="m1")
        data = json.loads(result)
        assert "m1" in data["message"]
