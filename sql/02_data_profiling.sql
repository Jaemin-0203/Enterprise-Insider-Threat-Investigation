/*
========================================
sharepoint_activity
========================================
*/

SELECT *
FROM sharepoint_activity
LIMIT 20;

SELECT COUNT(*)
FROM sharepoint_activity;

SELECT DISTINCT operation
FROM sharepoint_activity
ORDER BY operation;

SELECT
    MIN(event_time_utc) AS first_event,
    MAX(event_time_utc) AS last_event
FROM sharepoint_activity;

/*
========================================
Graph Metadata
========================================
*/

SELECT *
FROM graph_metadata
LIMIT 10;

SELECT COUNT(*)
FROM graph_metadata;

SELECT DISTINCT sensitivitylabel
FROM graph_metadata
ORDER BY sensitivitylabel;

SELECT
    MIN(created_time_utc),
    MAX(created_time_utc)
FROM graph_metadata;

/*
========================================
Teams Activity
========================================
*/

SELECT *
FROM teams_activity
LIMIT 10;

SELECT COUNT(*)
FROM teams_activity;

SELECT DISTINCT channel_name
FROM teams_activity;

SELECT COUNT(DISTINCT user_email)
FROM teams_activity;

SELECT
    MIN(event_time_utc),
    MAX(event_time_utc)
FROM teams_activity;

/*
========================================
OneDrive Activity
========================================
*/

SELECT *
FROM onedrive_activity
LIMIT 10;

SELECT COUNT(*)
FROM onedrive_activity;

SELECT DISTINCT operation
FROM onedrive_activity;

SELECT
    MIN(event_time_utc),
    MAX(event_time_utc)
FROM onedrive_activity;