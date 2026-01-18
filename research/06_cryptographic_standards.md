# Cryptographic Standards & Immutable Logging

## 1. Requirement
Automated capital allocation decisions must be tamper-evident. If the AI releases \$5M for a chip fabrication deposit, the "audit trail" explaining *why* (i.e., the originating government solicitation) cannot be alterable.

## 2. Signal Hashing
Every generated signal is hashed using **SHA-256**.
`Hash = SHA256(signal_id + timestamp + source_url + demand_probability)`

## 3. Digital Signatures
The Credit Agent (Human-in-the-Loop component) signs approved transactions using **ECDSA (secp256k1)**.
- **Private Key:** Stored in HSM (Hardware Security Module) - Architected for FIPS 140-2 Level 3 compliant hardware.
- **Public Key:** Embedded in the ERP Audit Log.

## 4. Key Management
- **Rotation:** API Keys for connectors rotate every 90 days.
- **Storage:** Environment variables injected at runtime (no hardcoding).

## 5. NIST Compliance
This architecture aligns with **NIST SP 800-171** requirements for protecting Controlled Unclassified Information (CUI) in non-federal systems.

<!-- Refined by GovSignal Automation -->
