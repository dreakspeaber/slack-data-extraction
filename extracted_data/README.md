# Database Extraction Results

This directory contains JSON files extracted from the SQL database dump `db_1758093955565_4jfjxb8pj.sql`.

## Summary

- **Total Tables**: 48
- **Total Rows**: 2,531
- **Extraction Date**: 2025-09-19T01:07:28.420898

## Files Generated

### Summary File
- `extraction_summary.json` - Complete overview of all tables and their metadata

### Individual Table Files
Each table has been extracted to its own JSON file with the following structure:

```json
{
  "table_name": "table_name",
  "columns": ["col1", "col2", ...],
  "row_count": 123,
  "extracted_at": "2025-09-19T01:07:28.413389",
  "data": [
    {
      "col1": "value1",
      "col2": "value2",
      ...
    },
    ...
  ]
}
```

### Table List
- slack_audit_reports (40 rows)
- slack_scheduled_messages (40 rows)
- slack_audit_anomaly_allow (40 rows)
- slack_audit_policies (40 rows)
- slack_api_calls (40 rows)
- slack_messages (600 rows)
- slack_workflow_trigger_types (40 rows)
- slack_shared_invites (40 rows)
- slack_emojis (40 rows)
- slack_audit_compliance (40 rows)
- slack_roles (40 rows)
- slack_user_groups (40 rows)
- slack_usergroup_teams (40 rows)
- slack_calls (40 rows)
- slack_functions (40 rows)
- slack_audit_logs (40 rows)
- slack_enterprises (8 rows)
- slack_apps (40 rows)
- slack_audit_anomaly_events (40 rows)
- slack_emoji_aliases (40 rows)
- slack_usergroup_channels (40 rows)
- slack_channels (80 rows)
- slack_barriers (40 rows)
- slack_invite_requests (40 rows)
- slack_emoji_categories (40 rows)
- slack_users (99 rows)
- slack_function_permissions (40 rows)
- slack_function_executions (40 rows)
- slack_function_grants (40 rows)
- slack_teams (24 rows)
- slack_app_scopes (40 rows)
- slack_app_icons (40 rows)
- slack_app_requests (40 rows)
- slack_approved_apps (40 rows)
- slack_restricted_apps (40 rows)
- slack_app_configs (40 rows)
- slack_channel_restrictions (40 rows)
- slack_invites (40 rows)
- slack_invite_request_channels (40 rows)
- slack_role_assignments (40 rows)
- slack_call_participants (40 rows)
- slack_user_sessions (40 rows)
- slack_user_unsupported_versions (40 rows)
- slack_workflows (40 rows)
- slack_workflow_trigger_type_permissions (40 rows)
- slack_invite_channels (40 rows)
- slack_workflow_collaborators (40 rows)
- slack_workflow_triggers (40 rows)

## Data Types Handled

The extraction script automatically handles:
- NULL values → `null`
- Boolean values (TRUE/FALSE) → `true`/`false`
- Quoted strings with proper unescaping
- JSON arrays and objects (e.g., `'[]'`, `'{}'`)
- Numeric values (integers and floats)
- Timestamps and dates

## Usage

You can now use these JSON files for:
- Data analysis and reporting
- Importing into other systems
- API development
- Data visualization
- Machine learning datasets

## Script Used

The extraction was performed using `extract_db_to_json.py` which:
1. Parses SQL INSERT statements
2. Extracts column names and values
3. Handles data type conversion
4. Saves each table to a separate JSON file
5. Generates metadata and summary information
