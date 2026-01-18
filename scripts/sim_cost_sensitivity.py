"""
Simulation: Cost Sensitivity Analysis
=====================================

Goal:
-----
Analyze how varying the Stockout Penalty affects the economic viability of the Readiness Protocol vs. Legacy ERP.
Determines the "Break-even" point regarding criticality of the items (implied by penalty magnitude).

Key Metrics:
------------
- Average Total Cost vs. Stockout Penalty (Log Scale)
- Break-even Cost

Hypothesis:
-----------
As Stockout Penalty increases (items become more critical), the Readiness Protocol's value increases, justifying its costs.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set random seed
np.random.seed(42)

# Get project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cost Sensitivity Analysis
PENALTIES = [10000, 50000, 100000, 500000, 1000000]
NUM_ITERATIONS = 100
MONTHS = 36

class SupplyChainSim:
    def __init__(self, policy, lead_time, penalty):
        self.policy = policy
        self.lead_time = lead_time
        self.penalty = penalty
        self.inventory = 60
        self.pipeline = []
        self.cost = 0
        
    def step(self, month, demand, signal):
        # Arrive
        self.inventory += sum(o[1] for o in self.pipeline if o[0] == month)
        self.pipeline = [o for o in self.pipeline if o[0] > month]
        # Demand
        if self.inventory >= demand:
            self.inventory -= demand
        else:
            self.cost += self.penalty
            self.inventory = 0
        self.cost += self.inventory * 500
        
        trigger = False
        if "Legacy" in self.policy:
            if self.inventory + sum(o[1] for o in self.pipeline) < 80: trigger = True
        else:
            if signal > 0.75: trigger = True
        if trigger: self.pipeline.append([month + self.lead_time, 60])

if __name__ == "__main__":
    avg_costs_a = []
    avg_costs_b = []
    
    print("Running Cost Sensitivity...")
    for p in PENALTIES:
        c_a, c_b = [], []
        for _ in range(NUM_ITERATIONS):
            demands = np.random.poisson(5, MONTHS)
            signals = np.random.uniform(0, 1, MONTHS)
            
            s_a = SupplyChainSim("Legacy", 12, p)
            s_b = SupplyChainSim("Readiness", 3, p)
            for m in range(MONTHS):
                s_a.step(m, demands[m], signals[m])
                s_b.step(m, demands[m], signals[m])
            c_a.append(s_a.cost)
            c_b.append(s_b.cost)
        avg_costs_a.append(np.mean(c_a))
        avg_costs_b.append(np.mean(c_b))

    plt.figure()
    plt.plot(PENALTIES, avg_costs_a, label='Legacy (12mo)', marker='o')
    plt.plot(PENALTIES, avg_costs_b, label='Readiness (3mo)', marker='x')
    plt.xscale('log')
    plt.xlabel('Stockout Penalty ($)')
    plt.ylabel('Avg Total Cost')
    plt.title('Break-even Analysis')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, "cost_sensitivity.png"))
