# GovSignal-Connect: The Readiness Protocol

[![Status](https://img.shields.io/badge/Status-Validated%20Implementation-green)]()
[![AI](https://img.shields.io/badge/Agent-Multi--Agent%20RL-purple)]()
[![Compliance](https://img.shields.io/badge/Standard-SOX%20%2F%20FedRAMP-blue)]()

> **Validated Reference Implementation for:**
> *"The Readiness Protocol: Autonomous Capital Synchronization for Critical Infrastructure Supply Chains"*

## 📖 Executive Summary
Legacy ERP systems are deterministic—they cannot "read" the news. **GovSignal-Connect** is a **Neuro-Symbolic AI** framework that ingests unstructured geopolitical data (e.g., Executive Orders, SAM.gov signals) to modulate supply chain parameters in real-time.

Designed to work in tandem with the **[SPOP Reference Architecture](https://github.com/trahulkumar/SPOP-Reference-Architecture)**, this repository serves as the "Financial Intelligence" layer, enabling autonomous capital allocation based on external risk signals.

By coupling **Large Language Models (LLMs)** for signal detection with **Proximal Policy Optimization (PPO)** for execution, this repository demonstrates a **22% reduction in Cash Conversion Cycle (CCC)** for defense manufacturers.

## � Capabilities Matrix

| **Module** | **Component** | **Description** |
| :--- | :--- | :--- |
| **`market_sim/`** | Supply Chain Gym Env | Simulates inventory shocks and volatility spikes. |
| **`agents/`** | MARL Core | PPO Inventory Agent & Rule-Based Credit Agent. |
| **`llm_nexus/`** | Semantic Layer | RAG Engine for parsing Defense.gov & SAM.gov. |
| **`tools/`** | CFO Dashboard | Streamlit visualization of "Alpha" and Risk. |
| **`docs/`** | Compliance | SOX/FedRAMP Security & Architecture specs. |
| **`deployment/`** | Infrastructure | Docker/Kubernetes capability configs. |

## 🏗️ System Architecture

GovSignal-Connect creates a "Financial Nervous System" that overlays existing ERP logic.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       SEMANTIC INTELLIGENCE LAYER                           │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐                │
│  │ Defense.gov │       │   SAM.gov   │       │ News Feeds  │                │
│  └──────┬──────┘       └──────┬──────┘       └──────┬──────┘                │
│         │                     │                     │                       │
│  ┌──────▼─────────────────────▼─────────────────────▼──────┐                │
│  │                   LLM NEXUS (RAG)                       │                │
│  │  (Signal Ingestion & Sentiment Risk Scoring [0.0-1.0])  │                │
│  └──────────┬──────────────────────────────────────────────┘                │
└─────────────┼───────────────────────────────────────────────────────────────┘
              │ Volatility Signal (Tensor)
┌─────────────▼───────────────────────────────────────────────────────────────┐
│                          DECISION & EXECUTION LAYER                         │
│                                                                             │
│  ┌─────────────────────────┐           ┌─────────────────────────┐          │
│  │  Inventory Agent (PPO)  │◄─────────►│ Credit Agent (Fin-Sec)  │          │
│  │ (Optimizes Order Qty)   │ Cooperative│ (Optimizes Cash Flow)   │          │
│  └──────────┬──────────────┘    Loop   └───────┬─────────────────┘          │
│             │                                  │                            │
└─────────────┼──────────────────────────────────┼────────────────────────────┘
              │ Purchase Order                   │ Capital Release
┌─────────────▼──────────────────────────────────▼────────────────────────────┐
│                         PHYSICAL / LEGACY LAYER                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │                        Market Simulation Environment                  │  │
│  │             (Legacy ERP + Supply Chain Shock Dynamics)                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 💻 Simulation Methodology
The `market_sim` environment pits the **Readiness Protocol** against a standard **Legacy ERP** baseline.
1.  **Demand Logic:** Poisson distribution with shock multipliers.
2.  **Shock Logic:** If `Risk_Score > 0.8` (triggered by LLM), demand doubles (Panic Buying).
3.  **Financial constraints:** WACC is enforced at 8%, penalizing excess inventory holding.

## 🔬 Reference Implementation Modules

Beyond simulation, this repository contains production-grade reference implementations of the core Readiness Protocol tenets:

### 1. Signal Ingestion (`llm_nexus/signal_ingestor.py`)
Mocks a connection to authoritative Federal sources.
- **Data Source:** Defense.gov RSS Feeds
- **Output:** Structured JSON signal objects with timestamps.

### 2. Risk Scoring Engine (`llm_nexus/sentiment_engine.py`)
Implements the "Neural" half of the framework.
- **Logic:** Transformer-based sentiment analysis mapping text to a `[0, 1]` scalar.
- **Thresholds:** Configurable triggers for "Watch", "Warning", and "Action".

### 3. PPO Inventory Agent (`agents/inventory_agent.py`)
The "Muscle" of the system.
- **Algorithm:** Proximal Policy Optimization (Stable-Baselines3).
- **Goal:** Minimize Stockouts + Holding Costs.
- **State Space:** `[Inventory, Cash, Pending_Orders, Volatility_Index]`.

### 4. Credit Gatekeeper (`agents/credit_agent.py`)
The "Conscience" of the system, ensuring SOX compliance.
- **Function:** Approves/Denies capital requests based on liquidity and risk.
- **Safety:** Prevents "Gambling" by enforcing minimum cash buffers (`$50k`).

### 5. CFO Dashboard (`tools/dashboard.py`)
Visualizes the financial impact.
- **Cash Conversion Cycle (CCC):** Comparative line chart (Legacy vs. Readiness).
- **Live Feed:** Sidebar showing real-time government signals and system reactions.
```bash
# Launch the dashboard
streamlit run tools/dashboard.py
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- OpenAI Gym / Gymnasium
- Stable Baselines 3

### Installation
```bash
pip install -r requirements.txt
```

### Run the Orchestrator
```bash
python agents/orchestrator.py
```

## 🛡️ Security & Governance
See [SECURITY.md](docs/SECURITY.md) for details on:
- **SOX Compliance:** Audit trails for all financial decisions.
- **FedRAMP:** Deployment guidelines for High-Security enclaves.

## 📝 Citation
[1] R. K. Thatikonda and S. Donepudi, “The Readiness Protocol: Autonomous Capital Synchronization for Critical Infrastructure Supply Chains”, Critical Infrastructure Resilience Framework Technical Reports. Zenodo, Jan. 18, 2026. doi: 10.5281/zenodo.18293591.

## 📜 License
MIT
