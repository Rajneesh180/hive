# Supabase Tool

This tool allows the agent to interact with a Supabase project, providing capabilities for Database queries, Authentication management, and Storage inspection.

## Credentials

The tool requires two environment variables mapped in the CredentialStore:
- `SUPABASE_URL`: Your project API URL (e.g. `https://xyz.supabase.co`)
- `SUPABASE_SERVICE_ROLE_KEY`: The service role key for admin privileges.

## Provided Tools

### `supabase_db_query`
Execute a database query using PostgREST syntax against a specific table, or use RPC calls.
- **Args**: `table` (string), `action` ("select", "insert", "update", "delete"), `payload` (Optional dict for data).

### `supabase_auth_list_users`
List the users currently registered in the Supabase Auth module.
- **Args**: None

### `supabase_storage_list_buckets`
List available storage buckets in the project.
- **Args**: None
