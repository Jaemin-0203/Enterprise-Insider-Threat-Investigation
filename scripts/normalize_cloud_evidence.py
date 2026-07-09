import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "raw_data"
PROCESSED = BASE / "processed_data"
PROCESSED.mkdir(exist_ok=True)

INTERNAL_DOMAIN = "contoso.example"


def clean_timestamp(value):
    return value.replace("Z", "") if value else ""


def get_domain(email):
    if not email or "@" not in email:
        return ""
    return email.split("@")[-1].lower()


def is_external_recipient(email):
    domain = get_domain(email)
    if not domain:
        return ""
    return str(domain != INTERNAL_DOMAIN).upper()


# =========================================================
# Extract: Load raw Microsoft 365 evidence
# =========================================================

with open(RAW / "graph_metadata.json", "r", encoding="utf-8") as f:
    graph = json.load(f)

with open(RAW / "teams_export.json", "r", encoding="utf-8") as f:
    teams = json.load(f)


# =========================================================
# Transform 1: Graph metadata -> graph_metadata.csv
# =========================================================

graph_rows = []

for item in graph["driveItems"]:
    graph_rows.append({
        "driveItemId": item["driveItemId"],
        "file_name": item["name"],
        "created_by": item["createdBy"],
        "created_time_utc": clean_timestamp(item["createdDateTime"]),
        "sensitivityLabel": item["sensitivityLabel"],
        "web_url": item["webUrl"],
        "siteId": item["parentReference"]["siteId"],
        "driveId": item["parentReference"]["driveId"],
    })

with open(PROCESSED / "graph_metadata.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=graph_rows[0].keys())
    writer.writeheader()
    writer.writerows(graph_rows)


# Build lookup table for enrichment
graph_lookup = {
    item["driveItemId"]: item
    for item in graph["driveItems"]
}


# =========================================================
# Transform 2: Teams export -> teams_activity.csv
# =========================================================

teams_rows = []
timeline_rows = []

for msg in teams["messages"]:
    attachments = msg.get("attachments", [])

    if attachments:
        for att in attachments:
            drive_item_id = att["driveItemId"]
            metadata = graph_lookup.get(drive_item_id, {})

            teams_row = {
                "message_id": msg["message_id"],
                "event_time_utc": clean_timestamp(msg["createdDateTime"]),
                "event_time_cdt": msg["createdDateTime_CDT"],
                "user_email": msg["sender"],
                "channel_name": msg["channel_name"],
                "message_body": msg["body"],
                "file_name": att["file_name"],
                "driveItemId": drive_item_id,
            }
            teams_rows.append(teams_row)

            timeline_rows.append({
                "event_source": "Teams",
                "event_time_utc": teams_row["event_time_utc"],
                "event_time_cdt": teams_row["event_time_cdt"],
                "user_email": teams_row["user_email"],
                "operation": "TeamsMessageAttachment",
                "file_name": teams_row["file_name"],
                "driveItemId": drive_item_id,
                "sensitivityLabel": metadata.get("sensitivityLabel", ""),
                "siteId": metadata.get("parentReference", {}).get("siteId", ""),
                "driveId": metadata.get("parentReference", {}).get("driveId", ""),
                "message_id": teams_row["message_id"],
                "recipient_email": "",
                "recipient_domain": "",
                "recipient_type": "",
                "sharing_scope": "",
                "permission_role": "",
                "is_external": "",
                "details": teams_row["message_body"],
            })

    else:
        teams_rows.append({
            "message_id": msg["message_id"],
            "event_time_utc": clean_timestamp(msg["createdDateTime"]),
            "event_time_cdt": msg["createdDateTime_CDT"],
            "user_email": msg["sender"],
            "channel_name": msg["channel_name"],
            "message_body": msg["body"],
            "file_name": "",
            "driveItemId": "",
        })

with open(PROCESSED / "teams_activity.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=teams_rows[0].keys())
    writer.writeheader()
    writer.writerows(teams_rows)


# =========================================================
# Transform 3: SharePoint audit logs -> sharepoint_activity.csv
# Add derived fields: recipient_domain, is_external
# =========================================================

with open(RAW / "sharepoint_audit_logs.csv", "r", encoding="utf-8") as src:
    reader = csv.DictReader(src)
    sharepoint_rows = []

    for row in reader:
        recipient_email = row.get("recipient_email", "")
        recipient_domain = get_domain(recipient_email)
        external_flag = is_external_recipient(recipient_email)

        clean_row = {
            "event_time_utc": clean_timestamp(row["event_time_utc"]),
            "event_time_cdt": row["event_time_cdt"],
            "user_email": row["user_email"],
            "operation": row["operation"],
            "file_name": row["file_name"],
            "driveItemId": row["driveItemId"],
            "site_url": row["site_url"],
            "client_ip": row["client_ip"],
            "recipient_email": recipient_email,
            "recipient_domain": recipient_domain,
            "recipient_type": row.get("recipient_type", ""),
            "sharing_scope": row.get("sharing_scope", ""),
            "permission_role": row.get("permission_role", ""),
            "is_external": external_flag,
        }

        sharepoint_rows.append(clean_row)

        metadata = graph_lookup.get(clean_row["driveItemId"], {})

        timeline_rows.append({
            "event_source": "SharePoint",
            "event_time_utc": clean_row["event_time_utc"],
            "event_time_cdt": clean_row["event_time_cdt"],
            "user_email": clean_row["user_email"],
            "operation": clean_row["operation"],
            "file_name": clean_row["file_name"],
            "driveItemId": clean_row["driveItemId"],
            "sensitivityLabel": metadata.get("sensitivityLabel", ""),
            "siteId": metadata.get("parentReference", {}).get("siteId", ""),
            "driveId": metadata.get("parentReference", {}).get("driveId", ""),
            "message_id": "",
            "recipient_email": clean_row["recipient_email"],
            "recipient_domain": clean_row["recipient_domain"],
            "recipient_type": clean_row["recipient_type"],
            "sharing_scope": clean_row["sharing_scope"],
            "permission_role": clean_row["permission_role"],
            "is_external": clean_row["is_external"],
            "details": f"site_url={clean_row['site_url']}; client_ip={clean_row['client_ip']}",
        })

with open(PROCESSED / "sharepoint_activity.csv", "w", newline="", encoding="utf-8") as dst:
    writer = csv.DictWriter(dst, fieldnames=sharepoint_rows[0].keys())
    writer.writeheader()
    writer.writerows(sharepoint_rows)


# =========================================================
# Transform 4: OneDrive activity logs -> onedrive_activity.csv
# =========================================================

with open(RAW / "onedrive_activity_logs.csv", "r", encoding="utf-8") as src:
    reader = csv.DictReader(src)
    onedrive_rows = []

    for row in reader:
        clean_row = {
            "event_time_utc": clean_timestamp(row["event_time_utc"]),
            "event_time_cdt": row["event_time_cdt"],
            "user_email": row["user_email"],
            "operation": row["operation"],
            "file_name": row["file_name"],
            "driveItemId": row["driveItemId"],
            "sync_client": row["sync_client"],
            "device_name": row["device_name"],
        }

        onedrive_rows.append(clean_row)

        metadata = graph_lookup.get(clean_row["driveItemId"], {})

        timeline_rows.append({
            "event_source": "OneDrive",
            "event_time_utc": clean_row["event_time_utc"],
            "event_time_cdt": clean_row["event_time_cdt"],
            "user_email": clean_row["user_email"],
            "operation": clean_row["operation"],
            "file_name": clean_row["file_name"],
            "driveItemId": clean_row["driveItemId"],
            "sensitivityLabel": metadata.get("sensitivityLabel", ""),
            "siteId": metadata.get("parentReference", {}).get("siteId", ""),
            "driveId": metadata.get("parentReference", {}).get("driveId", ""),
            "message_id": "",
            "recipient_email": "",
            "recipient_domain": "",
            "recipient_type": "",
            "sharing_scope": "",
            "permission_role": "",
            "is_external": "",
            "details": f"sync_client={clean_row['sync_client']}; device_name={clean_row['device_name']}",
        })

with open(PROCESSED / "onedrive_activity.csv", "w", newline="", encoding="utf-8") as dst:
    writer = csv.DictWriter(dst, fieldnames=onedrive_rows[0].keys())
    writer.writeheader()
    writer.writerows(onedrive_rows)


# =========================================================
# Load: Create master timeline CSV
# =========================================================

timeline_rows.sort(key=lambda x: x["event_time_utc"])

timeline_fieldnames = [
    "event_source",
    "event_time_utc",
    "event_time_cdt",
    "user_email",
    "operation",
    "file_name",
    "driveItemId",
    "sensitivityLabel",
    "siteId",
    "driveId",
    "message_id",
    "recipient_email",
    "recipient_domain",
    "recipient_type",
    "sharing_scope",
    "permission_role",
    "is_external",
    "details",
]

with open(PROCESSED / "normalized_cloud_evidence.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=timeline_fieldnames)
    writer.writeheader()
    writer.writerows(timeline_rows)


print("Created SQL-ready CSV files and master timeline:")
print(f"- processed_data/graph_metadata.csv ({len(graph_rows)} rows)")
print(f"- processed_data/teams_activity.csv ({len(teams_rows)} rows)")
print(f"- processed_data/sharepoint_activity.csv ({len(sharepoint_rows)} rows)")
print(f"- processed_data/onedrive_activity.csv ({len(onedrive_rows)} rows)")
print(f"- processed_data/normalized_cloud_evidence.csv ({len(timeline_rows)} timeline events)")