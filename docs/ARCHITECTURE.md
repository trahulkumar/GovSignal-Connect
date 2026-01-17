# System Architecture

## 1. System Context Diagram
GovSignal-Connect operates as a Decentralized Multi-Agent System (MAS). The "Procurement Scout" is the primary external sensor, but it acts in concert with internal agents to execute the full "Smart Overlay" strategy.

```mermaid
graph TD
    subgraph "External Data Environment"
        SAM[SAM.gov]
        FR[Federal Register]
        CHIPS[CHIPS.gov Funding Portal]
    end

    subgraph "GovSignal-Connect (The Smart Overlay)"
        Scout[<b>The Scout</b><br/>(External Signal)]
        Inventory[<b>Inventory Agent</b><br/>(Stock Analysis)]
        Credit[<b>Credit Agent</b><br/>(Capital Release)]
    end

    subgraph "Enterprise Core"
        ERP[Legacy ERP<br/>SAP S/4HANA / Oracle]
        SCM[Supply Chain Planning]
    end

    SAM --> Scout
    FR --> Scout
    CHIPS --> Scout
    
    Scout -- "Standardized Demand Signal" --> Inventory
    Inventory -- "Stock Low Alert" --> Credit
    Inventory -- "Stock Healthy" --> Scout
    
    Credit -- "Authorization Token" --> ERP
    ERP -- "Purchase Order Created" --> SCM
```

## 2. Data Flow
The system follows a strict unidirectional data flow to ensure signal integrity:

1.  **Ingestion (The Scout):** The Scout continuously polls unstructured federal feeds. It filters noise using the `critical_asset_ontology`.
2.  **Normalization (External Signal):** Raw text is converted into a `Standard Signal` JSON payload. This isolates the legacy ERP from the chaos of unstructured government data.
3.  **Internal Logic (ERP):** The standardized signal is ingested by the ERP via REST or IDoc interfaces. The ERP handles the "Internal Logic" (e.g., checking specific warehouse bin levels, calculating lead times based on preferred vendors).

## 3. Governance & Compliance Architecture
This system is architected to satisfy **NIST SP 800-171 (Protecting Controlled Unclassified Information in Nonfederal Systems)**. It is not merely "compliant" but explicitly implements the following controls:

### 3.1 Audit & Accountability (AU-2, AU-3)
- **Immutable Ledger:** All automated decisions (`release_capital_hold`) are cryptographically hashed and stored in a Write-Once-Read-Many (WORM) log.
- **Traceability:** Every signal sent to the ERP includes the raw JSON source, timestamp, and the specific Keyword Density Score (KDA) that triggered it.

### 3.2 Access Control (AC-2, AC-3)
- **Role-Based Access Control (RBAC):** Determining who can adjust "Demand Probability" thresholds is strictly limited to authorized System Administrators.
- **Separation of Duties:** The `Scout` module (Ingestion) runs in a separate, isolated container from the `Credit` module (Execution) to prevent lateral privilege escalation.

### 3.3 System validation integrity (SI-7)
- **Software Integrity:** All agents sign their payloads. The ERP connector verifies the digital signature before accepting any capital release instruction to prevent "Man-in-the-Middle" signal spoofing.
