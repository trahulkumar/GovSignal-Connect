# Key Generation Protocol

## 1. System Keys
GovSignal uses asymmetric cryptography for signing internal messages.
- **Algorithm:** RSA-4096 or ECDSA P-384.

## 2. API Key Management
Connecting to 20+ sources requires robust secret management.
- **Vault:** HashiCorp Vault is the specified secret manager.
- **Injection:** Secrets are injected as environment variables `GOVSIGNAL_API_KEY_{SOURCE}`.

## 3. Protocol for New Keys
1.  DevOps generates key pair in offline machine.
2.  Public key is committed to `certs/known_hosts`.
3.  Private key is imported directly to Vault.
4.  Offline machine is wiped.
