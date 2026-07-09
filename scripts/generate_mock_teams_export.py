import csv
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

random.seed(42)

BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "raw_data"
RAW.mkdir(exist_ok=True)

CASE_ID = "DFIR-2026-001"
INTERNAL_DOMAIN = "contoso.example"

PROJECT_STRATEGY_ID = "driveitem-project-falcon-strategy-001"
FALCON_TARGETS_ID = "driveitem-falcon-acquisition-targets-002"

users = [
    "john.carter@contoso.example",
    "sarah.chen@contoso.example",
    "maria.gomez@contoso.example",
    "david.kim@contoso.example",
    "emily.choi@contoso.example",
    "alex.ross@contoso.example",
    "linda.park@contoso.example",
    "michael.lee@contoso.example",
]

normal_files = [
    ("Board_Meeting_Notes.docx", "driveitem-normal-001", "General Business", "sarah.chen@contoso.example"),
    ("Vendor_Pricing.xlsx", "driveitem-normal-002", "Internal", "emily.choi@contoso.example"),
    ("Executive_Bonus_Plan.docx", "driveitem-normal-003", "Internal", "maria.gomez@contoso.example"),
    ("Q3_Forecast.xlsx", "driveitem-normal-004", "Confidential", "sarah.chen@contoso.example"),
    ("Due_Diligence_Checklist.pdf", "driveitem-normal-005", "Internal", "john.carter@contoso.example"),
    ("Finance_Review.xlsx", "driveitem-normal-006", "Confidential", "maria.gomez@contoso.example"),
    ("Customer_List.xlsx", "driveitem-normal-007", "Internal", "john.carter@contoso.example"),
    ("Pricing_Model.xlsx", "driveitem-normal-008", "Confidential", "linda.park@contoso.example"),
    ("HR_Transition_Plan.docx", "driveitem-normal-009", "Internal", "emily.choi@contoso.example"),
    ("Integration_Timeline.docx", "driveitem-normal-010", "General Business", "david.kim@contoso.example"),
]

sensitive_files = [
    {
        "name": "Project_Falcon_Strategy.docx",
        "driveItemId": PROJECT_STRATEGY_ID,
        "sensitivityLabel": "Confidential - M&A",
        "createdBy": "john.carter@contoso.example",
        "createdDateTime": "2026-06-22T16:12:00Z",
        "siteId": "site-project-falcon",
        "driveId": "drive-project-falcon-docs",
    },
    {
        "name": "Falcon_Acquisition_Targets.xlsx",
        "driveItemId": FALCON_TARGETS_ID,
        "sensitivityLabel": "Highly Confidential - M&A",
        "createdBy": "john.carter@contoso.example",
        "createdDateTime": "2026-06-22T16:13:00Z",
        "siteId": "site-project-falcon",
        "driveId": "drive-project-falcon-docs",
    },
]

drive_items = []

for file_name, drive_id, label, creator in normal_files:
    drive_items.append({
        "driveItemId": drive_id,
        "name": file_name,
        "createdBy": creator,
        "createdDateTime": "2026-06-20T14:00:00Z",
        "sensitivityLabel": label,
        "webUrl": f"https://contoso.sharepoint.com/sites/CorporateDocs/{file_name}",
        "parentReference": {
            "siteId": "site-corporate-docs",
            "driveId": "drive-corporate-docs"
        }
    })

for item in sensitive_files:
    drive_items.append({
        "driveItemId": item["driveItemId"],
        "name": item["name"],
        "createdBy": item["createdBy"],
        "createdDateTime": item["createdDateTime"],
        "sensitivityLabel": item["sensitivityLabel"],
        "webUrl": f"https://contoso.sharepoint.com/sites/ProjectFalcon/{item['name']}",
        "parentReference": {
            "siteId": item["siteId"],
            "driveId": item["driveId"]
        }
    })

graph_metadata = {
    "case_id": CASE_ID,
    "export_source": "Microsoft Graph metadata export",
    "driveItems": drive_items
}

with open(RAW / "graph_metadata.json", "w", encoding="utf-8") as f:
    json.dump(graph_metadata, f, indent=2)


# ---------------- Teams Export JSON ----------------

messages = []
start = datetime(2026, 6, 22, 14, 0, tzinfo=timezone.utc)

normal_text = [
    "Can you review the latest version?",
    "Moving this to tomorrow morning.",
    "Please confirm before sharing.",
    "I uploaded the meeting notes.",
    "Let's keep this in the project channel.",
    "Can we align before the steering committee meeting?",
]

for i in range(750):
    dt = start + timedelta(minutes=random.randint(0, 240))
    sender = random.choice(users)
    file_item = random.choice(drive_items)
    attach_file = random.random() < 0.35

    attachments = []
    if attach_file:
        attachments.append({
            "attachment_id": f"att-normal-{i}",
            "file_name": file_item["name"],
            "driveItemId": file_item["driveItemId"],
            "provider": "SharePoint"
        })

    messages.append({
        "message_id": f"msg-normal-{i:04d}",
        "createdDateTime": dt.isoformat().replace("+00:00", "Z"),
        "createdDateTime_CDT": (dt - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S CDT"),
        "sender": sender,
        "team_id": "team-corp-dev",
        "channel_id": random.choice(["channel-finance", "channel-legal", "channel-ma-planning"]),
        "channel_name": random.choice(["Finance", "Legal Review", "Project Falcon / M&A Planning"]),
        "body": random.choice(normal_text),
        "attachments": attachments
    })

# Suspicious Teams messages correlated with workstation timeline
suspicious_messages = [
    (
        "2026-06-22T16:13:35Z",
        "john.carter@contoso.example",
        "Please review the Project Falcon strategy file before tomorrow.",
        sensitive_files[0]
    ),
    (
        "2026-06-22T16:15:05Z",
        "john.carter@contoso.example",
        "I am keeping a backup copy until my transition is complete.",
        None
    ),
    (
        "2026-06-22T16:16:30Z",
        "john.carter@contoso.example",
        "Delete this message after review.",
        sensitive_files[1]
    ),
]

for idx, (ts_text, sender, body, file_item) in enumerate(suspicious_messages, start=1):
    dt = datetime.fromisoformat(ts_text.replace("Z", "+00:00"))
    attachments = []

    if file_item:
        attachments.append({
            "attachment_id": f"att-suspicious-{idx}",
            "file_name": file_item["name"],
            "driveItemId": file_item["driveItemId"],
            "provider": "SharePoint"
        })

    messages.append({
        "message_id": f"msg-suspicious-{idx}",
        "createdDateTime": ts_text,
        "createdDateTime_CDT": (dt - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S CDT"),
        "sender": sender,
        "team_id": "team-project-falcon",
        "channel_id": "channel-ma-planning",
        "channel_name": "Project Falcon / M&A Planning",
        "body": body,
        "attachments": attachments
    })

messages = sorted(messages, key=lambda x: x["createdDateTime"])

teams_export = {
    "case_id": CASE_ID,
    "export_source": "Microsoft Graph / Teams chatMessage-style export",
    "tenant": {
        "tenant_id": "contoso-lab-tenant",
        "display_name": "Contoso Legal Hold Lab"
    },
    "messages": messages
}

with open(RAW / "teams_export.json", "w", encoding="utf-8") as f:
    json.dump(teams_export, f, indent=2)


# ---------------- SharePoint Audit Logs CSV ----------------

sharepoint_rows = []

operations = ["FileAccessed", "FilePreviewed", "FileModified", "FileDownloaded"]

for i in range(450):
    dt = start + timedelta(minutes=random.randint(0, 240))
    file_item = random.choice(drive_items)

    sharepoint_rows.append({
        "event_time_utc": dt.isoformat().replace("+00:00", "Z"),
        "event_time_cdt": (dt - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S CDT"),
        "user_email": random.choice(users),
        "operation": random.choice(operations),
        "file_name": file_item["name"],
        "driveItemId": file_item["driveItemId"],
        "site_url": "https://contoso.sharepoint.com/sites/ProjectFalcon"
        if "Falcon" in file_item["name"]
        else "https://contoso.sharepoint.com/sites/CorporateDocs",
        "client_ip": f"172.16.{random.randint(1, 250)}.{random.randint(1, 250)}",
        "recipient_email": "",
        "recipient_type": "",
        "sharing_scope": "",
        "permission_role": ""
    })

# Suspicious SharePoint activity after workstation activity
suspicious_sharepoint = [
    {
        "ts": "2026-06-22T16:14:02Z",
        "user": "john.carter@contoso.example",
        "operation": "FileAccessed",
        "file": sensitive_files[0],
        "recipient": "",
        "recipient_type": "",
        "sharing_scope": "",
        "permission_role": "",
    },
    {
        "ts": "2026-06-22T16:14:18Z",
        "user": "john.carter@contoso.example",
        "operation": "FileDownloaded",
        "file": sensitive_files[1],
        "recipient": "",
        "recipient_type": "",
        "sharing_scope": "",
        "permission_role": "",
    },
    {
        "ts": "2026-06-22T16:15:22Z",
        "user": "john.carter@contoso.example",
        "operation": "SharingSet",
        "file": sensitive_files[0],
        "recipient": "sarah.chen@contoso.example",
        "recipient_type": "User",
        "sharing_scope": "SpecificPeople",
        "permission_role": "View",
    },
    {
        "ts": "2026-06-22T16:16:07Z",
        "user": "john.carter@contoso.example",
        "operation": "SharingSet",
        "file": sensitive_files[1],
        "recipient": "john.carter.personal@gmail.com",
        "recipient_type": "ExternalUser",
        "sharing_scope": "SpecificPeople",
        "permission_role": "View",
    },
    {
        "ts": "2026-06-22T16:17:12Z",
        "user": "john.carter@contoso.example",
        "operation": "SharingSet",
        "file": sensitive_files[1],
        "recipient": "unknown.external@outlook.com",
        "recipient_type": "ExternalUser",
        "sharing_scope": "Anyone",
        "permission_role": "View",
    },
]

for event in suspicious_sharepoint:
    dt = datetime.fromisoformat(event["ts"].replace("Z", "+00:00"))
    sharepoint_rows.append({
        "event_time_utc": event["ts"],
        "event_time_cdt": (dt - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S CDT"),
        "user_email": event["user"],
        "operation": event["operation"],
        "file_name": event["file"]["name"],
        "driveItemId": event["file"]["driveItemId"],
        "site_url": "https://contoso.sharepoint.com/sites/ProjectFalcon",
        "client_ip": "172.16.4.22",
        "recipient_email": event["recipient"],
        "recipient_type": event["recipient_type"],
        "sharing_scope": event["sharing_scope"],
        "permission_role": event["permission_role"]
    })

sharepoint_rows = sorted(sharepoint_rows, key=lambda x: x["event_time_utc"])

with open(RAW / "sharepoint_audit_logs.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "event_time_utc",
        "event_time_cdt",
        "user_email",
        "operation",
        "file_name",
        "driveItemId",
        "site_url",
        "client_ip",
        "recipient_email",
        "recipient_type",
        "sharing_scope",
        "permission_role"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(sharepoint_rows)


# ---------------- OneDrive Activity Logs CSV ----------------

onedrive_rows = []
onedrive_ops = ["SyncUploaded", "SyncDownloaded", "FileHydrated"]

for i in range(300):
    dt = start + timedelta(minutes=random.randint(0, 240))
    file_item = random.choice(drive_items)

    onedrive_rows.append({
        "event_time_utc": dt.isoformat().replace("+00:00", "Z"),
        "event_time_cdt": (dt - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S CDT"),
        "user_email": random.choice(users),
        "operation": random.choice(onedrive_ops),
        "file_name": file_item["name"],
        "driveItemId": file_item["driveItemId"],
        "sync_client": "OneDrive Sync Client",
        "device_name": random.choice(["Employee-PC01", "Employee-PC02", "Finance-Laptop01"])
    })

suspicious_onedrive = [
    {
        "ts": "2026-06-22T16:18:44Z",
        "user": "john.carter@contoso.example",
        "operation": "SyncDownloaded",
        "file": sensitive_files[1],
        "device_name": "Employee-PC01",
    }
]

for event in suspicious_onedrive:
    dt = datetime.fromisoformat(event["ts"].replace("Z", "+00:00"))
    onedrive_rows.append({
        "event_time_utc": event["ts"],
        "event_time_cdt": (dt - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S CDT"),
        "user_email": event["user"],
        "operation": event["operation"],
        "file_name": event["file"]["name"],
        "driveItemId": event["file"]["driveItemId"],
        "sync_client": "OneDrive Sync Client",
        "device_name": event["device_name"]
    })

onedrive_rows = sorted(onedrive_rows, key=lambda x: x["event_time_utc"])

with open(RAW / "onedrive_activity_logs.csv", "w", newline="", encoding="utf-8") as f:
    fieldnames = [
        "event_time_utc",
        "event_time_cdt",
        "user_email",
        "operation",
        "file_name",
        "driveItemId",
        "sync_client",
        "device_name"
    ]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(onedrive_rows)


print("Created updated Microsoft 365 raw evidence:")
print(f"- raw_data/teams_export.json ({len(messages)} Teams messages)")
print(f"- raw_data/sharepoint_audit_logs.csv ({len(sharepoint_rows)} SharePoint events)")
print(f"- raw_data/onedrive_activity_logs.csv ({len(onedrive_rows)} OneDrive events)")
print(f"- raw_data/graph_metadata.json ({len(drive_items)} DriveItems)")