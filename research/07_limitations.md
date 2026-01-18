# Research Limitations

## 1. Prototype Constraints
- **Mock Data:** The current implementation uses static mock responses for all connectors. Real-time integration requires paid API subscriptions (e.g., Bloomberg Terminal, paid SAM.gov tiers).
- **Simplified NLP:** The Keyword Density Algorithm (KDA) ignores semantic context (e.g., "NOT for semiconductors" vs "FOR semiconductors").

## 2. Scalability Limits
- **Single-Threaded Polling:** The `run()` loop is synchronous. Monitoring 10,000 sources would require asynchronous architecture (Celery/Redis).
- **Rate Limiting:** Production APIs often impose rate limits (e.g., 60 requests/min) which the current prototype does not handle aggressively.

## 3. Semantic Disambiguation Challenges
- **Keyword Ambiguity:** "Chip" can mean wood chips or silicon chips.
- **Current Mitigation:** Implementation of "Negative Lookahead" filters (e.g., exclude "wood", "potato" from "chip" queries).
- **Future Mitigation:** Migration to Vector Embeddings (Phase 2) to capture semantic context.

<!-- Refined by GovSignal Automation -->
