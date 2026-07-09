/*
=========================================================
Investigation 1

Identify High Value Corporate Documents

Objective:
Identify files that contain confidential business
information that could be targeted for exfiltration.

=========================================================
*/

SELECT
    file_name,
    sensitivitylabel,
    created_by,
    created_time_utc
FROM graph_metadata
WHERE sensitivitylabel ILIKE '%Confidential%'
ORDER BY sensitivitylabel DESC,
         created_time_utc;

SELECT COUNT(*)
FROM sharepoint_activity;



/*
=========================================================
Phase 2

Identify User Access to Sensitive M&A Documents

Client Question:
Who accessed or downloaded those documents?

Objective:
Determine which employees accessed or downloaded
M&A-classified confidential documents.
=========================================================
*/

SELECT
    sp.event_time_utc,
    sp.user_email,
    sp.operation,
    sp.file_name,
    gm.sensitivitylabel,
    sp.client_ip
FROM sharepoint_activity sp
JOIN graph_metadata gm
    ON sp.driveItemId = gm.driveItemId
WHERE gm.sensitivitylabel IN (
        'Highly Confidential - M&A',
        'Confidential - M&A'
    )
  AND sp.operation IN (
        'FileAccessed',
        'FileDownloaded'
    )
ORDER BY sp.event_time_utc;

/*
=========================================================
Phase 3

Investigate Sharing Activity for Sensitive M&A Documents

Client Question:
Were the documents shared with other users?

Objective:
Identify SharePoint sharing events involving M&A-classified
confidential documents.
=========================================================
*/

SELECT
    sp.event_time_utc,
    sp.user_email,
    sp.operation,
    sp.file_name,
    gm.sensitivitylabel,
    sp.client_ip,
    sp.site_url
FROM sharepoint_activity sp
JOIN graph_metadata gm
    ON sp.driveItemId = gm.driveItemId
WHERE gm.sensitivitylabel IN (
        'Highly Confidential - M&A',
        'Confidential - M&A'
    )
  AND sp.operation = 'SharingSet'
ORDER BY sp.event_time_utc;

/*
=========================================================
Phase 4

Detect External Data Exfiltration

Client Question:
Were any sensitive documents shared outside the organization?

Objective:
Identify confidential or M&A-classified documents that were
shared with external recipients, including recipient email,
domain, permission role, and sharing scope.
=========================================================
*/

SELECT
    sp.event_time_utc,
    sp.user_email AS sharing_user,
    sp.operation,
    sp.file_name,
    gm.sensitivitylabel,
    sp.recipient_email,
    sp.recipient_domain,
    sp.recipient_type,
    sp.sharing_scope,
    sp.permission_role,
    sp.is_external,
    sp.client_ip
FROM sharepoint_activity sp
JOIN graph_metadata gm
    ON sp.driveItemId = gm.driveItemId
WHERE sp.operation = 'SharingSet'
  AND sp.is_external = 'TRUE'
  AND gm.sensitivitylabel ILIKE '%Confidential%'
ORDER BY sp.event_time_utc;

/*
=========================================================
Phase 5

Reconstruct Relevant Insider Activity Timeline

Client Question:
Can the suspect's key actions be reconstructed into a
focused investigative timeline?

Objective:
Identify the most relevant sequence of John Carter's
activity involving Project Falcon documents, including
access, download, Teams distribution, external sharing,
and OneDrive synchronization.
=========================================================
*/

SELECT
    event_time_utc,
    event_time_cdt,
    event_source,
    user_email AS actor,
    operation,
    file_name,
    sensitivityLabel AS classification,
    recipient_email,
    recipient_domain,
    sharing_scope,
    permission_role,
    is_external,
    details
FROM normalized_cloud_evidence
WHERE user_email = 'john.carter@contoso.example'
  AND file_name ILIKE '%Falcon%'
  AND operation IN (
        'FileAccessed',
        'FileDownloaded',
        'SharingSet',
        'TeamsMessageAttachment',
        'SyncDownloaded'
  )
ORDER BY event_time_utc;





