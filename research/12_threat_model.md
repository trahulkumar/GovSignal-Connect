# Threat Model: Adversarial Supply Chain Analysis

## 1. Data Poisoning
**Threat:** An adversary (e.g., foreign state actor) publishes fake solicitations on compromised local government sites to mislead western supply chains (e.g., inducing a fake demand spike).
**Mitigation:**
- **Source Reputation Scoring:** Signals from .gov/.mil domains have higher trust than others.
- **Cross-Verification:** A signal requires corroboration from at least two independent sources before triggering `release_capital_hold`.

## 2. Input Manipulation (Future Semantic Phase)
**Threat:** Malicious text in a PDF abstract tricks the semantic analysis engine into ignoring safety protocols.
**Mitigation:** Strict input sanitization and deterministic guardrails.

## 3. Denial of Service (DoS)
**Threat:** Flooding the system with noise to hide a real signal.
**Mitigation:** Adaptive thresholding and anomaly detection in signal volume.

<!-- Refined by GovSignal Automation -->
