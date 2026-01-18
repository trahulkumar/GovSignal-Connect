# Integration Standards: ERP Connectors

## 1. Design Philosophy: The "Air-Gapped" Write
To comply with **NIST 800-82 (ICS Security)**, the GovSignal agents **never** write directly to the production ledger. All signals are routed to a **Staging Interface Table** for human validation.

## 2. SAP S/4HANA (IDoc)
Signals are transformed into **SAP IDoc** format for asynchronous ingestion.

### Mapping Profile: `PREQCR1` (Purchase Requisition - Staged)
| Scout Field | IDoc Segment | Field Name | Transformation |
|-------------|--------------|------------|----------------|
| `signal_id` | `E1PREQCR1` | `BANFN` | Hashed UUID (Audit Key) |
| `timestamp` | `E1PREQCR1` | `BLDAT` | YYYYMMDD |
| `erp_action`| `E1BPMEPOHEADER`| `NOTE` | **"AI_SUGGESTED_BUY: PENDING_APPROVAL"** |

## 3. Oracle Cloud SCM (REST)
- **Endpoint:** `/fscmRestApi/resources/11.13.18.05/purchaseRequisitions`
- **Method:** `POST` (Draft Mode)
- **Payload Tag:** `{"ApprovalStatus": "INCOMPLETE"}` (Ensures Human-in-the-Loop)

## 4. Middleware (Zero Trust)
All traffic is routed through a Mutual TLS (mTLS) gateway (MuleSoft/Kong) to prevent unauthorized agent activity.
