# Key Generation Protocol

## 1. System Keys
GovSignal uses asymmetric cryptography for signing internal messages, complying with **CNSA Suite 2.0** (Commercial National Security Algorithm) recommendations.
- **Algorithm:** RSA-4096 or ECDSA P-384.

## 2. API Key Management
Connecting to 20+ sources requires robust secret management.
- **Vault:** HashiCorp Vault (Enterprise) is the specified secret manager.
- **Injection:** Secrets are injected as environment variables `GOVSIGNAL_API_KEY_{SOURCE}` at runtime (No hardcoding).

## 3. Protocol for New Keys (The "Ceremony")
To ensure root of trust:
1.  **Air-Gapped Generation:** DevOps generates key pairs on a non-networked device (FIPS 140-3 Level 3 HSM).
2.  **Public Key:** Committed to `certs/known_hosts`.
3.  **Private Key:** Imported directly to Vault via ephemeral token.
4.  **Destruction:** Air-gapped machine state is wiped.
