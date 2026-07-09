-- ==========================================
-- Enterprise Insider Threat Investigation
-- Create cloud evidence investigation tables
-- Database: df_cloud_investigation
-- ==========================================

/*
WARNING

Running this script recreates all investigation tables.

Existing data will be removed.

Re-import CSV files after execution.
*/

DROP TABLE IF EXISTS normalized_cloud_evidence;
DROP TABLE IF EXISTS teams_activity;
DROP TABLE IF EXISTS sharepoint_activity;
DROP TABLE IF EXISTS onedrive_activity;
DROP TABLE IF EXISTS graph_metadata;

CREATE TABLE graph_metadata (
    driveItemId TEXT PRIMARY KEY,
    file_name TEXT,
    created_by TEXT,
    created_time_utc TIMESTAMP,
    sensitivityLabel TEXT,
    web_url TEXT,
    siteId TEXT,
    driveId TEXT
);

CREATE TABLE teams_activity (
    message_id TEXT,
    event_time_utc TIMESTAMP,
    event_time_cdt TEXT,
    user_email TEXT,
    channel_name TEXT,
    message_body TEXT,
    file_name TEXT,
    driveItemId TEXT
);

CREATE TABLE sharepoint_activity (
    event_time_utc TIMESTAMP,
    event_time_cdt TEXT,
    user_email TEXT,
    operation TEXT,
    file_name TEXT,
    driveItemId TEXT,
    site_url TEXT,
    client_ip TEXT,
    recipient_email TEXT,
    recipient_domain TEXT,
    recipient_type TEXT,
    sharing_scope TEXT,
    permission_role TEXT,
    is_external TEXT
);

CREATE TABLE onedrive_activity (
    event_time_utc TIMESTAMP,
    event_time_cdt TEXT,
    user_email TEXT,
    operation TEXT,
    file_name TEXT,
    driveItemId TEXT,
    sync_client TEXT,
    device_name TEXT
);

DROP TABLE IF EXISTS normalized_cloud_evidence;

CREATE TABLE normalized_cloud_evidence (
    event_source TEXT,
    event_time_utc TIMESTAMP,
    event_time_cdt TEXT,
    user_email TEXT,
    operation TEXT,
    file_name TEXT,
    driveItemId TEXT,
    sensitivityLabel TEXT,
    siteId TEXT,
    driveId TEXT,
    message_id TEXT,
    recipient_email TEXT,
    recipient_domain TEXT,
    recipient_type TEXT,
    sharing_scope TEXT,
    permission_role TEXT,
    is_external TEXT,
    details TEXT
);

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;