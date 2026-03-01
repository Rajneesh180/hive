import os
from unittest.mock import MagicMock, patch

import pytest
from fastmcp import FastMCP

from aden_tools.credentials import CredentialStoreAdapter
from aden_tools.tools.supabase_tool import register_tools


@pytest.fixture
def mcp():
    """Create a FastMCP instance with tools registered."""
    server = FastMCP("test")
    register_tools(server, credentials=None)
    return server


@pytest.fixture
def mock_supabase():
    with patch("aden_tools.tools.supabase_tool.supabase_tool._get_supabase_client") as mock_get:
        mock_client = MagicMock()
        mock_get.return_value = mock_client
        yield mock_client


def test_supabase_db_query_select(mcp, mock_supabase):
    """Test basic select query."""
    tool_fn = mcp._tool_manager._tools["supabase_db_query"].fn

    # Mock builder chain
    mock_table = MagicMock()
    mock_select = MagicMock()
    mock_execute = MagicMock()

    mock_supabase.table.return_value = mock_table
    mock_table.select.return_value = mock_select
    mock_select.execute.return_value = mock_execute
    mock_execute.data = [{"id": 1, "name": "Test"}]

    result = tool_fn(table="users", action="select")

    assert result["success"] is True
    assert result["count"] == 1
    assert result["data"][0]["name"] == "Test"
    mock_supabase.table.assert_called_with("users")


def test_supabase_auth_list(mcp, mock_supabase):
    """Test auth listing functionality."""
    tool_fn = mcp._tool_manager._tools["supabase_auth_list_users"].fn

    mock_user = MagicMock()
    mock_user.id = "user-123"
    mock_user.email = "test@example.com"

    mock_response = MagicMock()
    mock_response.users = [mock_user]

    mock_supabase.auth.admin.list_users.return_value = mock_response

    result = tool_fn()

    assert result["success"] is True
    assert result["count"] == 1
    assert result["data"][0]["email"] == "test@example.com"


def test_supabase_storage_list(mcp, mock_supabase):
    """Test storage listing functionality."""
    tool_fn = mcp._tool_manager._tools["supabase_storage_list_buckets"].fn

    mock_bucket = MagicMock()
    mock_bucket.id = "bucket-1"
    mock_bucket.name = "Public Assets"

    mock_supabase.storage.list_buckets.return_value = [mock_bucket]

    result = tool_fn()

    assert result["success"] is True
    assert result["count"] == 1
    assert result["data"][0]["name"] == "Public Assets"
