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

## 3. Auditability & Compliance
To meet requirements for **ITAR (International Traffic in Arms Regulations)** and **FDA (Food and Drug Administration)** validations, the system enforces strict audit trails:

-   **Decision Logging:** Every "Demand Probability" score is logged with its timestamp and source snippet.
-   **Immutable Records:** Actionable signals sent to the ERP (`release_capital_hold`) are hashed and stored to provide a tamper-evident record of *why* automated purchasing decisions were made.
-   **Human-in-the-Loop:** For signals with a confidence score between 0.5 and 0.8 (`flag_for_review`), the Credit Agent requires a human digital signature before releasing funds.
