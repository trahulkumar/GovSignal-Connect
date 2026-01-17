# GovSignal Test Suite

This directory contains unit and integration tests for the GovSignal Scout agent.

## Running Tests

To run all tests and capture output:

```bash
python tests/run_all.py
```

## Test Structure

- `test_scoring.py`: Verifies NLP keyword density logic.
- `test_schema.py`: Verifies JSON output structure and action thresholds.
- `test_config.py`: Verifies configuration loading.
- `test_sam_connector.py` / `test_fr_connector.py`: Tests for federal sources.
- `test_local_*.py`: Tests for state/local connectors by region.
- `test_integration.py`: Runs a full simulated cycle.
