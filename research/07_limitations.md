# Research Limitations & Constraints

## 1. Data Source constraints
- **Synthetic Validation Data:** The public repository utilizes sanitized, synthetic datasets to demonstrate logic flow without exposing proprietary or classified feed subscriptions (e.g., Bloomberg Terminal).
- **Production Requirement:** Live deployment requires active credentials for SAM.gov Data Bank (System for Award Management).

## 2. Architectural Scope
- **Reference Implementation:** The provided Python code is a synchronous, deterministic implementation designed for code auditability.
- **Production Scaling:** A deployed National-Scale system would utilize the asynchronous `Celery` / `Redis` architecture described in `10_scalability_report.md`.

## 3. Semantic Disambiguation Challenges
- **Keyword Ambiguity:** "Chip" can mean wood chips or silicon chips.
- **Current Mitigation:** "Negative Lookahead" Regex filters.
- **Future Mitigation:** Migration to Vector Embeddings (Phase 2) to capture semantic context.
