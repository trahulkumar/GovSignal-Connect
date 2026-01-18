"""
Simulation: Hybrid Policy Evaluation
====================================

Goal:
-----
Evaluate a "Hybrid" policy that combines traditional Inventory Management (ROP) with Signal-based Logic.
Compares Pure Legacy, Pure Readiness, and Hybrid approaches.

Key Metrics:
------------
- Total Cost Distribution (Boxplot)

Policies:
---------
1. Legacy: 12mo Lead Time, ROP Trigger only.
2. Readiness: 3mo Lead Time, Signal Trigger only.
3. Hybrid: 3mo Lead Time, uses BOTH a lower ROP (Safety Net) and High Signal (Surge Response).
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

# Hybrid Policy Simulation
# Policy C: ROP + Signal Surge
NUM_ITERATIONS = 500
MONTHS = 36

class SupplyChainSim:
    def __init__(self, policy, lead_time):
        self.policy = policy
        self.lead_time = lead_time
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
            self.cost += 50000
            self.inventory = 0
        self.cost += self.inventory * 500
        
        trigger = False
        
        # Base ROP Logic (All policies use ROP logic as baseline? Or compare Pure vs Hybrid?)
        # Let's compare:
        # A: Pure Legacy (12mo, ROP)
        # B: Pure Readiness (3mo, Signal)
        # C: Hybrid (readiness lead time 3mo, but uses ROP AND Signal)
        
        inventory_pos = self.inventory + sum(o[1] for o in self.pipeline)
        
        if self.policy == "Legacy":
            # 12mo lead time, ROP=80
            if inventory_pos < 80: trigger = True
            
        elif self.policy == "Readiness":
             # 3mo lead time, Signal only
             if signal > 0.75: trigger = True
             
        elif self.policy == "Hybrid":
            # 3mo lead time
            # 1. ROP Safety Net (Lower ROP since we are fast? Or same?)
            if inventory_pos < 40: trigger = True # Lower ROP
            # 2. Surge Signal
            if signal > 0.8: trigger = True # Stricter signal

        if trigger: self.pipeline.append([month + self.lead_time, 60])

if __name__ == "__main__":
    c_a, c_b, c_c = [], [], []
    for _ in range(NUM_ITERATIONS):
        demands = np.random.poisson(5, MONTHS)
        signals = np.random.uniform(0,1, MONTHS)
        
        s_a = SupplyChainSim("Legacy", 12)
        s_b = SupplyChainSim("Readiness", 3)
        s_c = SupplyChainSim("Hybrid", 3)
        
        for m in range(MONTHS):
            s_a.step(m, demands[m], signals[m])
            s_b.step(m, demands[m], signals[m])
            s_c.step(m, demands[m], signals[m])
            
        c_a.append(s_a.cost)
        c_b.append(s_b.cost)
        c_c.append(s_c.cost)
        
    plt.figure()
    plt.boxplot([c_a, c_b, c_c], labels=['Legacy', 'Pure Readiness', 'Hybrid'])
    plt.title('Hybrid Policy Performance')
    plt.ylabel('Cost')
    plt.savefig(os.path.join(OUTPUT_DIR, "hybrid_policy_results.png"))
