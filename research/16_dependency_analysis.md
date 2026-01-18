# Software Bill of Materials (SBOM) & Dependency Analysis

## 1. Core Architecture (The Agent System)
- **requests (v2.31):** HTTP client for connector polling. (External dependency).
- **PyYAML (v6.0):** Configuration parsing for ontology mapping.
- **pydantic (v2.0):** Data validation for JSON signal schemas (ensures strict typing).

## 2. Simulation & AI Stack (The "Readiness Protocol" Engine)
*Libraries used to generate the Monte Carlo validation data.*
- **numpy / pandas:** Stochastic modeling and inventory vectorization.
- **scipy:** Statistical distribution handling (Poisson/Normal demand curves).
- **matplotlib / seaborn:** Generation of validation graphs (`lead_time_comparison.png`).

## 3. Supply Chain Risk Management (SCRM)
- **Pinning:** All dependencies are pinned in `requirements.txt` with SHA-256 hashes to prevent "Dependency Confusion" attacks.
- **Base Image:** Builds utilize distroless container images (`gcr.io/distroless/python3`) to minimize attack surface (Aligns with CISA guidelines).
