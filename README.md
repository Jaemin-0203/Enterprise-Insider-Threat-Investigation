# Enterprise Insider Threat Investigation

> Advanced Digital Forensics & Cloud Investigation Project using **FTK Imager, Autopsy, Python, PostgreSQL, and Microsoft 365 Audit Logs** to investigate suspected insider data exfiltration.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![SQL](https://img.shields.io/badge/SQL-Investigation-orange)
![Digital Forensics](https://img.shields.io/badge/Digital-Forensics-darkgreen)
![Autopsy](https://img.shields.io/badge/Autopsy-Artifact%20Analysis-success)
![FTK Imager](https://img.shields.io/badge/FTK-Imager-lightgrey)
![Microsoft 365](https://img.shields.io/badge/Microsoft-365-blueviolet)

---

# Project Overview

This project simulates a real-world enterprise insider threat investigation involving both endpoint forensic artifacts and Microsoft 365 cloud collaboration evidence.

The investigation demonstrates how forensic evidence from multiple sources can be collected, normalized, analyzed, and correlated to reconstruct user activity and identify potential intellectual property exfiltration.

Rather than analyzing isolated artifacts, this project follows an end-to-end investigation workflow similar to those performed by digital forensic consultants and corporate incident response teams.

---

# Investigation Scenario

A departing employee was suspected of accessing confidential corporate documents before leaving the organization.

The investigation focused on determining whether the employee:

- Accessed sensitive project files
- Downloaded confidential documents
- Shared files through Microsoft Teams
- Synchronized data to OneDrive
- Shared information with external recipients
- Attempted to conceal evidence

---

# Investigation Objectives

- Identify suspicious user activity
- Correlate cloud audit logs across multiple Microsoft 365 services
- Normalize heterogeneous evidence into a common investigation dataset
- Reconstruct an investigative timeline
- Produce SQL-driven findings suitable for investigative reporting

---

# Evidence Sources

The investigation combines evidence from multiple Microsoft 365 data sources.

| Evidence Source | Description |
|----------------|-------------|
| Microsoft Teams Export | Team messages and shared attachments |
| SharePoint Audit Logs | File access and sharing events |
| OneDrive Activity Logs | Synchronization and download activity |
| Microsoft Graph Metadata | File metadata and sensitivity labels |

---

# Investigation Workflow

```
Raw Microsoft 365 Evidence
        │
        ▼
Python Evidence Normalization
        │
        ▼
Normalized CSV Evidence
        │
        ▼
PostgreSQL Database
        │
        ▼
SQL Investigation Queries
        │
        ▼
Investigation Findings & Reporting
```

---

# Project Structure

```
Enterprise-Insider-Threat-Investigation
│
├── raw_data/
│   ├── teams_export.json
│   ├── sharepoint_audit_logs.csv
│   ├── onedrive_activity_logs.csv
│   └── graph_metadata.json
│
├── processed_data/
│   ├── normalized_cloud_evidence.csv
│   ├── teams_activity.csv
│   ├── sharepoint_activity.csv
│   ├── onedrive_activity.csv
│   └── graph_metadata.csv
│
├── scripts/
│   ├── generate_mock_teams_export.py
│   └── normalize_cloud_evidence.py
│
├── sql/
│   ├── 01_create_investigation_tables.sql
│   ├── 02_import_data.sql
│   ├── 03_investigation_queries.sql
│   └── 04_reporting_views.sql
│
└── README.md
```

---

# Investigation Questions

The SQL investigation answers questions including:

- Which sensitive files did the suspect access?
- Which documents were downloaded?
- Were files shared externally?
- Which Microsoft Teams conversations contained confidential attachments?
- Which OneDrive synchronization events occurred?
- Can the suspect's activity be reconstructed into a chronological timeline?

---

# Technologies Used

### Digital Forensics

- FTK Imager
- Autopsy

### Programming

- Python
- CSV
- JSON

### Database

- PostgreSQL
- SQL

### Cloud Technologies

- Microsoft 365
- Microsoft Teams
- SharePoint
- OneDrive
- Microsoft Graph

---

# Skills Demonstrated

- Digital Forensic Investigation
- Cloud Evidence Processing
- Evidence Normalization
- SQL Investigation
- Timeline Reconstruction
- Insider Threat Investigation
- Microsoft 365 Audit Analysis
- Python Automation
- Investigative Reporting
- Data Correlation

---

# Future Improvements

- Microsoft Purview Audit Logs
- Exchange Online Investigation
- Azure AD Sign-in Analysis
- Automated Timeline Visualization
- Power BI Investigation Dashboard
- Chain of Custody Documentation

---

# Author

**Jaemin You**

Digital Forensics | Incident Investigation | SQL | Python | Microsoft 365
