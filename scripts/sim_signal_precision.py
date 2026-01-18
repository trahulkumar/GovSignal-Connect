"""
Simulation: High-Precision Signal Impact
========================================

Goal:
-----
Demonstrate the maximum potential of the Readiness Protocol when using a highly trusted, high-precision signal (Future Demand correlated).
Contrasts "Blind" Legacy policy with a "Precise" Readiness policy.

Key Metrics:
------------
- Total Cost Distribution (Boxplot)

Methodology:
------------
Generates a synthetic signal that is explicitly correlated with demand 3 months in the future, simulating a highly effective Scout Agent.
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

# Simulation: Signal Precision
# Correlating signal to future demand
NUM_ITERATIONS = 500
MONTHS = 36

def generate_correlated_signal(demands):
    # If demand in next 3 months is high, signal goes high
    signals = []
    for i in range(len(demands)):
        future_avg = np.mean(demands[i:min(i+3, len(demands))]) if i < len(demands) else 5
        if future_avg > 7: # Threshold
            signals.append(np.random.uniform(0.7, 1.0))
        else:
            signals.append(np.random.uniform(0.0, 0.4)) # Quiet otherwise
    return signals

class SupplyChainSim:
    def __init__(self, policy_name, lead_time):
        self.inventory = 60
        self.pipeline = []
        self.cost = 0
        self.policy = policy_name
        self.lead_time = lead_time
        
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
        if "Legacy" in self.policy:
            if self.inventory + sum(o[1] for o in self.pipeline) < 80: trigger = True
        else:
            if signal > 0.75: trigger = True
            
        if trigger: self.pipeline.append([month + self.lead_time, 60])

if __name__ == "__main__":
    costs_a, costs_b = [], []
    for _ in range(NUM_ITERATIONS):
        demands = np.random.poisson(5, MONTHS)
        # Perfect Signal
        signals = generate_correlated_signal(demands)
        
        s_a = SupplyChainSim("Legacy", 12)
        s_b = SupplyChainSim("Readiness", 3)
        for m in range(MONTHS):
            s_a.step(m, demands[m], signals[m])
            s_b.step(m, demands[m], signals[m])
        costs_a.append(s_a.cost)
        costs_b.append(s_b.cost)

    plt.figure()
    plt.boxplot([costs_a, costs_b], labels=['Legacy (Blind)', 'Readiness (Precise)'])
    plt.title('Impact of High-Precision Signal')
    plt.ylabel('Cost')
    plt.savefig(os.path.join(OUTPUT_DIR, "signal_precision_results.png"))
