from .base import CredentialSpec

SUPABASE_CREDENTIALS = {
    "supabase": CredentialSpec(
        env_var="SUPABASE_URL",
        tools=[
            "supabase_db_query",
            "supabase_auth_list_users",
            "supabase_storage_list_buckets",
        ],
        required=True,
        help_url="https://supabase.com/dashboard/project/_/settings/api",
        description="Supabase Project API URL",
        credential_id="supabase",
        credential_key="SUPABASE_URL",
    ),
    "supabase_service": CredentialSpec(
        env_var="SUPABASE_SERVICE_ROLE_KEY",
        tools=[
            "supabase_db_query",
            "supabase_auth_list_users",
            "supabase_storage_list_buckets",
        ],
        required=True,
        help_url="https://supabase.com/dashboard/project/_/settings/api",
        description="Supabase Service Role Key (Admin Access)",
        credential_id="supabase",
        credential_key="SUPABASE_SERVICE_ROLE_KEY",
    ),
}
