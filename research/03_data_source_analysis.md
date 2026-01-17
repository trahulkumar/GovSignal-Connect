# Data Source Analysis

## 1. Federal Sources
| Source | Type | Update Frequency | Data Format | Reliability |
|--------|------|------------------|-------------|-------------|
| **SAM.gov** | Contract Solicitations | Daily | API (JSON) | High |
| **Federal Register** | Policy/Notices | Daily | API (JSON/XML) | High |

## 2. State & Local Sources (Selected)
We monitor 20+ distinct non-federal sources to detect "grassroots" supply chain shifts before they appear in federal data.

| Region | Key Sources | Focus Area |
|--------|-------------|------------|
| **West** | CA GO-Biz, AZ Commerce, WA Commerce | Semiconductors, Aerospace, Cloud Infrastructure |
| **South** | TX TEF, FL Defense TF, NC Biotech, Huntsville | Defense Mfg, Bio-Pharma, Rocket Propulsion |
| **East** | NY ESD, Mass Life Sci, VEDP, PA DCED, Port Authority | Chip Fabs, Biologics, Cyber-physical, Logistics |
| **Midwest** | OH Development, MI MEDC, IN IEDC | "Silicon Heartland", Auto-Defense, Microelectronics |
| **Policy** | NGA, CSG | Interstate Compacts, Regulatory Alignment |

## 3. Data Ingestion Strategy
Connectors normalize disparate local formats (HTML scrapers, RSS feeds, Socrata APIs) into a unified `ConnectorResponse` schema.
