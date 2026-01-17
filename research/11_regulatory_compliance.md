# Regulatory Compliance Framework

## 1. NIST SP 800-171 (DFARS)
Since GovSignal handles data relevant to defense supply chains, it must adhere to NIST 800-171 controls for CUI:
- **3.1 Access Control:** Role-Based Access Control (RBAC) enforces 'Need to Know'.
- **3.13 System and Communications Protection:** FIPS 140-2 validated encryption for data in transit (TLS 1.3).

## 2. CMMC Level 2
The architecture is designed to support Cybersecurity Maturity Model Certification (CMMC) Level 2 certification, required for DoD contractors.
- **Audit Logging:** Centralized, immutable logging.
- **Incident Response:** Automated alerting for anomaly detection.

## 3. Sarbanes-Oxley (SOX)
For public companies, automated capital allocation (ERP writes) is a "Material Financial Process".
- **Validation:** Every algorithm change is version-controlled and peer-reviewed.
- **Traceability:** Signals link back to original government source URL.
