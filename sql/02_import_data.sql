-- Verify imported table row counts

SELECT count(*) 
FROM graph_metadata;

SELECT count(*)
FROM sharepoint_activity;

SELECT count(*)
FROM onedrive_activity;

SELECT count(*)
FROM teams_activity;

SELECT count(*)
FROM normalized_cloud_evidence;

SELECT column_name, data_type, ordinal_position
FROM information_schema.columns
WHERE table_name = 'sharepoint_activity'
ORDER BY ordinal_position;