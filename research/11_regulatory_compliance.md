# Regulatory Compliance Framework

## 1. NIST SP 800-171 (DFARS)
Since GovSignal handles data relevant to defense supply chains, it adheres to NIST 800-171 Rev 3 controls for Controlled Unclassified Information (CUI):
- **3.1 Access Control:** Role-Based Access Control (RBAC) enforces 'Need to Know' via Zero-Trust principles.
- **3.13 System Protection:** Cryptographic modules align with **FIPS 140-3** standards for data in transit (TLS 1.3) and at rest (AES-256).

## 2. CMMC Level 2 (Defense Industrial Base)
The architecture supports Cybersecurity Maturity Model Certification (CMMC) Level 2, a prerequisite for future DoD contract bids.
- **Audit Logging:** Immutable decision logs ensure traceability of every "Capital Release" signal.
- **Incident Response:** Automated circuit breakers isolate compromised connectors within milliseconds.

## 3. Sarbanes-Oxley (SOX) Section 404
For public manufacturers, the "Readiness Protocol" acts as a Material Financial Process.
- **Algorithmic Accountability:** The system creates a deterministic audit trail linking every purchase requisition back to the originating federal solicitation URL.
- **Internal Control:** This prevents "Ghost Inventory" and ensures automated spending aligns with corporate governance.
