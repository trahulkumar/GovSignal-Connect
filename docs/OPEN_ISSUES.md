# Open Issues

This document tracks active development tasks and known bugs for GovSignal-Connect.

## Issue #1: Enhance NLP logic for 'Vacuum Chamber' detection
**Label:** `enhancement`
**Status:** Open
**Description:**
The current Keyword Density Analysis (KDA) struggles with compound terms like "Vacuum Chamber" or "Clean Room", often treating them as separate tokens.
**Acceptance Criteria:**
- Update `_calculate_probability` to handle n-gram tokenization.
- Add "Vacuum Chamber" to the default `semiconductor` keyword set.

## Issue #2: Fix timeout bug in SAM.gov connector
**Label:** `bug`
**Status:** Open
**Description:**
The `SamGovConnector` currently defaults to a 30s timeout, which causes failures during peak API load times (approx 09:00 EST).
**Fix:**
- Increase default timeout to 60s.
- Implement exponential backoff retry logic.

## Issue #3: Add support for Oracle ERP Cloud API
**Label:** `roadmap`
**Status:** Planned (Q3 2026)
**Description:**
Expand integration beyond SAP IDoc to support Oracle Fusion Cloud SCM.
**Tasks:**
- Create `OracleConnector` class.
- Map `Signal` schema to Oracle `PurchaseRequest` payload.

## Issue #4: Implement real-time rate limiting
**Label:** `infrastructure`
**Status:** Open
**Description:**
Local connectors currently poll sequentially but lack explicit sleep intervals between requests to the *same* host (when iterating pages), risking IP bans.
