"""
Simulation: Black Swan Event Analysis
=====================================

Goal:
-----
Compare the resilience of Legacy and Readiness policies during a "Black Swan" event (extreme unexpected demand spike).
Specifically models a 10x demand surge for 6 consecutive months.

Key Metrics:
------------
- Total Cost Impact (Holding + Stockout)
- Durability (Implicit in Stockout Costs)

Hypothesis:
-----------
The Readiness Protocol (3mo Lead Time, Signal-driven) should adapt faster to the surge than the Legacy Policy (12mo Lead Time).
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

NUM_ITERATIONS = 500
MONTHS = 36 # 3 years

def run():
    costs_a, costs_b = [], []
    print("Running Black Swan Simulation...")
    for _ in range(NUM_ITERATIONS):
        # Generate Demand with Spike
        demands = np.random.poisson(5, MONTHS)
        demands[12:18] = np.random.poisson(50, 6) # The Spike
        signals = np.random.uniform(0,1, MONTHS)
        
        # Policy A (Legacy, 12mo LT)
        sim_a = SupplyChainSim("Legacy", 12)
        # Policy B (Readiness, 3mo LT)
        sim_b = SupplyChainSim("Readiness", 3)
        
        for m in range(MONTHS):
            sim_a.step(m, demands[m], signals[m])
            sim_b.step(m, demands[m], signals[m])
            
        costs_a.append(sim_a.cost)
        costs_b.append(sim_b.cost)
        
    return costs_a, costs_b

class SupplyChainSim:
    def __init__(self, policy_name, lead_time):
        self.policy_name = policy_name
        self.lead_time = lead_time
        self.inventory = 60
        self.pipeline = []
        self.cost = 0
        
    def step(self, month, demand, signal):
        # Arrive
        self.inventory += sum(o[1] for o in self.pipeline if o[0] == month)
        self.pipeline = [o for o in self.pipeline if o[0] > month]
        # Demand
        if self.inventory >= demand: self.inventory -= demand
        else:
            self.cost += 50000 
            self.inventory = 0
        self.cost += self.inventory * 500
        
        # Policies
        trigger = False
        if "Legacy" in self.policy_name:
            # ROP Logic
            if self.inventory + sum(o[1] for o in self.pipeline) < 80: trigger = True
        elif "Readiness" in self.policy_name:
            # Signal Logic
            if signal > 0.75: trigger = True
            
        if trigger: self.pipeline.append([month + self.lead_time, 60])

if __name__ == "__main__":
    costs_a, costs_b = run()
    
    # Visualization
    plt.figure(figsize=(10,6))
    plt.boxplot([costs_a, costs_b], labels=['Legacy (12mo)', 'Readiness (3mo)'])
    plt.title('Cost Impact of "Black Swan" (10x Spike for 6mo)')
    plt.ylabel('Total Cost')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.savefig(os.path.join(OUTPUT_DIR, "black_swan_results.png"))
    print("Black Swan complete.")
