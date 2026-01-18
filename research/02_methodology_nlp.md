# Methodology: NLP-Driven Demand Probability Scoring

## 1. Abstract
We employ a deterministic Keyword Density Analysis (KDA) algorithm to quantify the "Demand Probability" of a given government solicitation relevant to a tracked asset class.

## 2. Scoring Algorithm
The scoring function $f(t, K)$ takes an input text $t$ and a set of target keywords $K$ to produce a probability $P \in [0.1, 0.95]$.

$$ P = \min(0.95, \text{BaseScore} + \sum_{k \in K} \mathbb{I}(k \in t) \times \text{Weight}) $$

Where:
- $\text{BaseScore} = 0.4$
- $\text{Weight} = 0.2$
- $\mathbb{I}(condition)$ is an indicator function (1 if true, 0 if false).

## 3. Justification for Deterministic XAI (Explainable AI)
While LLMs offer superior semantic generation, they lack the **interpretability** required for automated financial controls (SOX Section 404). This deterministic KDA model serves as a "Compliance Baseline," ensuring that every capital release trigger is mathematically traceable to a specific government solicitation text, eliminating "hallucination" risk in financial workflows.
