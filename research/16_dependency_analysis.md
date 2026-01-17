# Software Bill of Materials (SBOM) & Dependency Analysis

## 1. Core Dependencies
- **requests (v2.31):** HTTP client. Risk: Low. Standard library.
- **PyYAML (v6.0):** Configuration parsing. Risk: Medium (CVE-2020-14343 fixed in 5.4+).

## 2. Dev Dependencies
- **pytest:** Testing framework. Data-collection only.
- **black/flake8:** Linting.

## 3. Supply Chain Risk Management
All dependencies are pinned in `requirements.txt` with specific versions.
Images are built from trusted base images (`python:3.10-slim-bullseye`).
