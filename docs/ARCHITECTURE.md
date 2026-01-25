# Architecture: The Readiness Protocol

## The Neuro-Symbolic Loop

GovSignal-Connect operates on a "Neuro-Symbolic" feedback loop that bridges the gap between unstructured geopolitical signals and deterministic ERP systems.

`External Signal -> LLM -> Risk Score -> RL Agent -> ERP Action`

### 1. Signal Ingestion (Neural)
- **Source**: RSS Feeds (Defense.gov), Federal Registers (SAM.gov).
- **Processing**: The `llm_nexus` module uses Transformer-based models to parse text and assign a `Risk_Score` (0.0 - 1.0).

### 2. State Augmentation
- The `Risk_Score` updates the `Market_Volatility_Index` in the `market_sim`.
- This creates a "State Tensor" that includes both Financial data (Cash, Inventory) and Geopolitical data (Volatility).

### 3. Agent Execution (Symbolic/RL)
- **Inventory Agent (PPO)**: Observes the augmented state and outputs `Order_Quantity`. PPO was chosen for its ability to handle continuous action spaces and stable convergence.
- **Credit Agent**: A rule-based (or DQN) gatekeeper that manages `Cash_on_Hand` ensuring compliance with WACC (Weighted Average Cost of Capital).

### 4. Action (Physical)
- The system executes purchase orders or capital releases, affecting the simulated supply chain environment.

## Design Choices
- **Why PPO?** Proximal Policy Optimization is robust for continuous control problems like inventory management where the action output is a float value (Quantity).
- **Why RAG?** Retrieval Augmented Generation allows traceability. Every decision to "Buy" can be traced back to a specific government citation or news event.
