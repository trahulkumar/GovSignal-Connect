# Contributor Guidelines

## 1. Governance Model
This project operates under a **Benevolent Dictator for Life (BDFL)** model, managed by the Principal Investigator (T. Kumar), to ensure alignment with national security standards.

## 2. Pull Request Policy
- **Tests:** All PRs must include unit tests covering >80% of new code.
- **Security:** Code must not bypass `crypto_utils.py` signing logic. All ERP-facing signals must remain traceable (NIST 800-171 compliance).
- **Commits:** Follow conventional commits format (`feat:`, `fix:`, `docs:`).

## 3. Code of Conduct
We adhere to the [Contributor Covenant v2.1](https://www.contributor-covenant.org/).
