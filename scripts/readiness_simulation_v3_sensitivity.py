"""
Readiness Simulation v3: Signal Sensitivity Analysis
====================================================

Goal:
-----
Analyze the impact of Signal Precision (True Positive Rate/False Alarm Rate) on the Total Cost of the Readiness Protocol.
Determine the "Break-even Precision" where the Readiness Protocol becomes cheaper than the Legacy Policy.

Key Metrics:
------------
- Total Cost vs. Signal Precision
- Break-even Point

Hypothesis:
-----------
As Signal Precision increases (fewer False Alarms), the Readiness Protocol's cost decreases.
There exists a precision threshold above which the Readiness Protocol is superior to Legacy ERP.

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set random seed
np.random.seed(42)

# --- Configuration ---
NUM_ITERATIONS = 500 # Reduced slightly for sensitivity loop speed if needed, but 1000 is fine
SIMULATION_MONTHS = 36
DEMAND_MEAN = 5
HOLDING_COST_PER_UNIT = 500
STOCKOUT_PENALTY = 50000
ORDERING_COST = 2000
INITIAL_INVENTORY = 60
ORDER_QTY = 60

# Policy A: Legacy ERP
POLICY_A_LEAD_TIME = 12
POLICY_A_ROP = 80

# Policy B: Readiness Protocol
POLICY_B_LEAD_TIME = 3
# Signal Threshold not used directly; we model Signal Precision directly.
CHECK_ROP = 20 # "Hidden" ROP that the Scout Agent detects (Lead Time 3 * Demand 5 + Safety)

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# Output to parent's output folder
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "..", "output", "v3_sensitivity")
os.makedirs(OUTPUT_DIR, exist_ok=True)
GRAPH_PATH = os.path.join(OUTPUT_DIR, "signal_sensitivity.png")

class SupplyChainSim:
    def __init__(self, policy_name, lead_time, initial_inv=INITIAL_INVENTORY):
        self.policy_name = policy_name
        self.lead_time = lead_time
        self.inventory = initial_inv
        self.pipeline = []
        self.total_holding_cost = 0
        self.total_stockout_cost = 0
        self.total_ordering_cost = 0
        
        # Signal Metrics
        self.true_positives = 0
        self.false_positives = 0
        self.false_negatives = 0

    def step(self, month, demand, fp_prob=0.0):
        # 1. Receive Orders
        idx_to_remove = []
        for i, order in enumerate(self.pipeline):
            if order[0] == month:
                self.inventory += order[1]
                idx_to_remove.append(i)
        for i in sorted(idx_to_remove, reverse=True):
            del self.pipeline[i]

        # 2. Fulfill Demand
        if self.inventory >= demand:
            self.inventory -= demand
        else:
            self.inventory = 0
            self.total_stockout_cost += STOCKOUT_PENALTY

        # 3. Holding Cost
        self.total_holding_cost += self.inventory * HOLDING_COST_PER_UNIT

        # 4. Ordering Logic
        order_qty = 0
        inventory_position = self.inventory + sum(o[1] for o in self.pipeline)

        if self.policy_name == "Legacy ERP":
            if inventory_position < POLICY_A_ROP:
                order_qty = ORDER_QTY
        
        elif self.policy_name == "Readiness Protocol":
            # "True Need" definition: If we don't order, will we stock out in Lead Time?
            # Approximation: Forecasted Inv at (t + LeadTime) < Safety.
            # Simplified: Is Inventory Position low?
            # A "Perfect Scout" signals exactly when Inventory Position < CHECK_ROP.
            
            is_needed = inventory_position < CHECK_ROP
            
            signal = False
            
            if is_needed:
                # True Positive (Recall assumed 1.0 for this test)
                signal = True
                self.true_positives += 1
            else:
                # False Alarm Opportunity
                if np.random.random() < fp_prob:
                    signal = True
                    self.false_positives += 1
                else:
                    signal = False
            
            # Additional constraint: Don't re-signal if we just ordered? 
            # The logic above "inventory_position" includes pipeline, 
            # so if we ordered last month, is_needed becomes False.
            # So continuous signaling is handled by the state check.
            
            if signal:
                order_qty = ORDER_QTY

        if order_qty > 0:
            arrival_time = month + self.lead_time
            self.pipeline.append([arrival_time, order_qty])
            self.total_ordering_cost += ORDERING_COST

    def total_cost(self):
        return self.total_holding_cost + self.total_stockout_cost + self.total_ordering_cost

    def get_precision(self):
        if self.true_positives + self.false_positives == 0:
            return 1.0 # No signals, conceptually perfect or undefined.
        return self.true_positives / (self.true_positives + self.false_positives)

def run_sensitivity_analysis():
    # 1. Calculate Legacy Baseline
    legacy_costs = []
    print("Running Baseline (Legacy ERP)...")
    for _ in range(NUM_ITERATIONS):
        sim = SupplyChainSim("Legacy ERP", POLICY_A_LEAD_TIME)
        demands = np.random.poisson(DEMAND_MEAN, SIMULATION_MONTHS)
        for m in range(SIMULATION_MONTHS):
            sim.step(m, demands[m])
        legacy_costs.append(sim.total_cost())
    
    avg_legacy_cost = np.mean(legacy_costs)
    print(f"Legacy Baseline Cost: ${avg_legacy_cost:,.2f}")

    # 2. Sweep Signal Precision (via FP Prob)
    # Target Precision 0.5 to 1.0
    # We iterate varied FP probs and measure resulting precision/cost
    fp_probs = np.linspace(0.0, 0.4, 20) # 0.0 -> Prec 1.0. 0.4 -> Low Prec
    
    results = [] # List of (precision, cost) tuples

    print("Running Sensitivity Analysis...")
    for fp_p in fp_probs:
        costs = []
        precisions = []
        
        for _ in range(NUM_ITERATIONS): # Smaller N per point?
            sim = SupplyChainSim("Readiness Protocol", POLICY_B_LEAD_TIME)
            demands = np.random.poisson(DEMAND_MEAN, SIMULATION_MONTHS)
            for m in range(SIMULATION_MONTHS):
                sim.step(m, demands[m], fp_prob=fp_p)
            
            costs.append(sim.total_cost())
            precisions.append(sim.get_precision())
            
        avg_cost = np.mean(costs)
        avg_prec = np.mean(precisions)
        results.append((avg_prec, avg_cost))
        # print(f"FP_Prob: {fp_p:.2f} -> Avg Precision: {avg_prec:.2f}, Cost: ${avg_cost:,.0f}")

    # Sort results by Precision for plotting
    results.sort(key=lambda x: x[0])
    
    # Extract
    x_prec = [r[0] for r in results]
    y_cost = [r[1] for r in results]

    # --- Plotting ---
    plt.figure(figsize=(10, 6))
    
    # User requested: Plot Total Cost (y) vs Signal Precision (x) 0.5 to 1.0
    
    # Filter for x >= 0.5
    filtered_data = [(x, y) for x, y in zip(x_prec, y_cost) if x >= 0.45]
    if not filtered_data:
        filtered_data = zip(x_prec, y_cost) # Fallback
        
    x_plot, y_plot = zip(*filtered_data)
    
    plt.plot(x_plot, y_plot, 'b-o', label='Readiness Protocol Cost', linewidth=2)
    plt.axhline(y=avg_legacy_cost, color='r', linestyle='--', label='Legacy Policy Baseline', linewidth=2)
    
    # Find Intersection (Break-even)
    # Simple check: where does Current < Legacy?
    crossover_x = None
    for x, y in sorted(zip(x_plot, y_plot)):
        if y < avg_legacy_cost:
            crossover_x = x
            break # First measurement below baseline
            # Interpolate for better accuracy?
            
    if crossover_x:
        plt.annotate(f'Break-even Reliability\nPrecision > {crossover_x:.2f}', 
                     xy=(crossover_x, avg_legacy_cost), 
                     xytext=(crossover_x, avg_legacy_cost + (max(y_plot)-min(y_plot))*0.2),
                     arrowprops=dict(facecolor='black', shrink=0.05))

    plt.title('Prompt 2: Signal Sensitivity Analysis (The "False Alarm" Test)')
    plt.xlabel('Signal Precision (True Positive Rate)')
    plt.ylabel('Total Cost ($)')
    plt.xlim(0.5, 1.0)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    plt.savefig(GRAPH_PATH)
    print(f"Graph saved to {GRAPH_PATH}")
    
    # Text Report
    print(f"\nSensitivity Result:")
    print(f"Legacy Cost: ${avg_legacy_cost:,.0f}")
    if crossover_x:
        print(f"Readiness Protocol becomes cheaper at Signal Precision > {crossover_x:.2f}")
    else:
        print(f"Readiness Protocol did not beat Legacy in this range (Max Prec tested: {max(x_prec):.2f})")

if __name__ == "__main__":
    run_sensitivity_analysis()
