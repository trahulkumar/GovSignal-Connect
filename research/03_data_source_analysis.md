# Data Source Analysis: The Intelligence Grid

## 1. Federal Sources (The "Official" Record)
| Source | Type | Update Frequency | Strategic Value |
|--------|------|------------------|-----------------|
| **SAM.gov** | Contract Opportunities | Real-Time (API) | **Confirmation:** Validates funding is released. |
| **Federal Register** | Policy Notices | Daily (06:00 EST) | **Early Warning:** Detects policy shifts 6-12 months before contracts. |

## 2. State & Local Sources (The "Grassroots" Signal)
We monitor 20+ non-federal sources to detect **"Pre-Solicitation"** indicators—infrastructure planning that precedes federal involvement.

| Region | Key Sources | Focus Area | Impact |
|--------|-------------|------------|--------|
| **West** | CA GO-Biz, WA Commerce | Semiconductors, Aerospace |  **Site Selection:** Predicts equipment demand 18 months out. |
| **South** | TX TEF, Huntsville (AL) | Defense Mfg, Propulsion | **Workforce Flows:** Tracking hiring surges at defense hubs. |
| **East** | NY ESD, Mass Life Sci | Chip Fabs, Biologics | **Grant Awards:** Tracks R&D capital before it hits procurement. |
| **Midwest** | OH, MI, IN (IEDC) | "Silicon Heartland" | **Re-shoring:** Monitors "Rust Belt" modernization projects. |

## 3. Data Ingestion Strategy
- **Normalization:** All disparate feeds (RSS, HTML, Socrata) are mapped to a unified `ConnectorResponse` schema.
- **Latency Target:** < 15 minutes from publication to ERP ingestion (vs. 48 hours for human analysts).
