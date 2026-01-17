# Audit Process Specification

## 1. Overview
This document defines the procedure for auditing the autonomous decisions made by GovSignal-Connect.

## 2. Daily Log Review
- **Role:** Compliance Officer (Human)
- **Action:** Review the `flag_for_review` queue.
- **Metric:** Check False Positive Rate (FPR). < 5% is acceptable.

## 3. Weekly Hash Verification
- **Role:** Systems Administrator
- **Action:** Re-hash a random sample of 50 signals and compare with the stored SHA-256 hash.
- **Fail State:** Any mismatch triggers an immediate System Halt (Circuit Breaker).

## 4. Quarterly Model Review
- **Role:** Data Scientist
- **Action:** Assess if keywords need updating based on new terminology (e.g., "AI PC" vs "Laptop").

<!-- Refined by GovSignal Automation -->
