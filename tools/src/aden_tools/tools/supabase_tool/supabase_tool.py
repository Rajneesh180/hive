import logging
import os
from typing import TYPE_CHECKING, Any

from fastmcp import FastMCP
from supabase import Client, create_client

if TYPE_CHECKING:
    from aden_tools.credentials import CredentialStoreAdapter

logger = logging.getLogger(__name__)


def _get_supabase_client(credentials: "CredentialStoreAdapter | None") -> Client:
    """Initialize and return a Supabase client using credentials or env vars."""
    url, key = None, None
    if credentials is not None:
        try:
            url = credentials.get("SUPABASE_URL")
            key = credentials.get("SUPABASE_SERVICE_ROLE_KEY")
        except KeyError:
            pass

    if not url:
        url = os.getenv("SUPABASE_URL")
    if not key:
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

    if not url or not key:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required to use the Supabase tool"
        )

    return create_client(url, key)


def register_tools(
    mcp: FastMCP,
    credentials: "CredentialStoreAdapter | None" = None,
) -> None:
    """Register Supabase tools with the MCP server."""

    @mcp.tool()
    def supabase_db_query(
        table: str,
        action: str = "select",
        query_filter: dict[str, Any] | None = None,
        payload: dict[str, Any] | list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """
        Execute a database operation against a Supabase table.

        Args:
            table: The name of the table to query.
            action: The operation to perform ('select', 'insert', 'update', 'delete').
            query_filter: Dictionary of column-value pairs to exact-match filter.
            payload: Data to insert or update.

        Returns:
            A dictionary containing the query 'data' or an 'error' message.
        """
        try:
            client = _get_supabase_client(credentials)
            builder = client.table(table)

            if action == "select":
                req = builder.select("*")
                if query_filter:
                    for k, v in query_filter.items():
                        req = req.eq(k, v)
                result = req.execute()
                return {"success": True, "data": result.data, "count": len(result.data)}

            elif action == "insert":
                if not payload:
                    return {"error": "payload is required for insert action"}
                result = builder.insert(payload).execute()
                return {"success": True, "data": result.data}

            elif action == "update":
                if not payload:
                    return {"error": "payload is required for update action"}
                if not query_filter:
                    return {"error": "query_filter is required for update action"}
                req = builder.update(payload)
                for k, v in query_filter.items():
                    req = req.eq(k, v)
                result = req.execute()
                return {"success": True, "data": result.data}

            elif action == "delete":
                if not query_filter:
                    return {"error": "query_filter is required for delete action"}
                req = builder.delete()
                for k, v in query_filter.items():
                    req = req.eq(k, v)
                result = req.execute()
                return {"success": True, "data": result.data}

            else:
                return {
                    "error": f"Unknown action: {action}. Use select, insert, update, or delete."
                }

        except Exception as e:
            logger.exception("Supabase DB Query failed")
            return {"error": f"Failed to execute DB query: {e}"}

    @mcp.tool()
    def supabase_auth_list_users() -> dict[str, Any]:
        """
        List all users registered in the Supabase Auth module.
        Requires Service Role Key.

        Returns:
            A dictionary containing the users 'data' or an 'error'.
        """
        try:
            client = _get_supabase_client(credentials)
            result = client.auth.admin.list_users()
            # The SDK returns a UserResponse object which has a users list
            users_list = []
            if hasattr(result, "users"):
                for u in result.users:
                    users_list.append(
                        {
                            "id": u.id,
                            "email": getattr(u, "email", None),
                            "created_at": getattr(u, "created_at", None),
                            "last_sign_in_at": getattr(u, "last_sign_in_at", None),
                        }
                    )
            return {"success": True, "data": users_list, "count": len(users_list)}
        except Exception as e:
            logger.exception("Supabase Auth List Users failed")
            return {"error": f"Failed to list auth users: {e}"}

    @mcp.tool()
    def supabase_storage_list_buckets() -> dict[str, Any]:
        """
        List all storage buckets in the Supabase project.

        Returns:
            A dictionary containing the buckets 'data' or an 'error'.
        """
        try:
            client = _get_supabase_client(credentials)
            buckets = client.storage.list_buckets()
            bucket_list = []
            for b in buckets:
                bucket_list.append(
                    {
                        "id": getattr(b, "id", None),
                        "name": getattr(b, "name", None),
                        "public": getattr(b, "public", None),
                        "created_at": getattr(b, "created_at", None),
                    }
                )
            return {"success": True, "data": bucket_list, "count": len(bucket_list)}
        except Exception as e:
            logger.exception("Supabase Storage List Buckets failed")
            return {"error": f"Failed to list storage buckets: {e}"}
