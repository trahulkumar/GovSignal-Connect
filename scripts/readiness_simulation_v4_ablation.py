"""
Readiness Simulation v4: Ablation Study
=======================================

Goal:
-----
Perform an ablation study to isolate the value of each agent in the multi-agent system.
Compare three configurations on 'Capital Utilization Efficiency'.

Configurations:
---------------
1. Full System (Scout + Inventory + Credit Agents):
   - Smart Order Quantity (Inventory Agent)
   - Signal-based Triggering (Scout Agent)
   - Budget Constraints (Credit Agent)

2. No Credit Constraint (Scout + Inventory):
   - Smart Order Quantity
   - Signal-based Triggering
   - Infinite Budget

3. Heuristic Only:
   - Fixed Order Quantity (No Inventory Agent optimization)
   - Simple Threshold Triggering (Signal > 0.75)
   - Infinite Budget

Metrics:
--------
- Capital Utilization Efficiency (Revenue / Average Working Capital)

Assumptions:
------------
- Unit Cost: $5,000
- Revenue Per Unit: $8,000
- Initial Budget (for Credit Constraint): $500,000 (roughly 100 units)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

np.random.seed(60) # Changed seed for fresh metrics

# --- Configuration ---
NUM_ITERATIONS = 1000
SIMULATION_MONTHS = 36
DEMAND_MEAN = 5
LEAD_TIME = 3 # All Readiness Based policies use the fast lane

# Financials
UNIT_COST = 5000
REVENUE_PER_UNIT = 8000
HOLDING_COST = 500 # Per unit per month
STOCKOUT_PENALTY = 50000

# Constraints
CREDIT_LIMIT = 500000 # Max Working Capital Allowed

# Agent Logic
FIXED_ORDER_QTY = 60
TARGET_INVENTORY = 80 # S for (s, S) logic
MIN_INVENTORY_S = 20  # s for (s, S) logic
SIGNAL_THRESHOLD = 0.75

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "..", "output", "v4_ablation")
os.makedirs(OUTPUT_DIR, exist_ok=True)
GRAPH_PATH = os.path.join(OUTPUT_DIR, "ablation_study.png")

class AblationSim:
    def __init__(self, config_name):
        self.config_name = config_name
        self.inventory = 60
        self.pipeline = []
        
        # Financial Tracking
        self.total_revenue = 0
        self.inventory_history = [] # To calculate Avg Working Capital
        
        # Agent Flags
        self.use_smart_inventory = "Inventory" in config_name or "Full" in config_name
        self.use_credit_limit = "Credit" in config_name or "Full" in config_name # "Full System" implies Credit
        
    def step(self, month, demand, signal):
        # 1. Update Inventory from Pipeline
        idx_to_remove = []
        for i, order in enumerate(self.pipeline):
            if order[0] == month:
                self.inventory += order[1]
                idx_to_remove.append(i)
        for i in sorted(idx_to_remove, reverse=True):
            del self.pipeline[i]

        # Track Working Capital (Inventory Value *before* sales)
        # Working Capital = Value of Goods we are holding/financing
        current_wc = self.inventory * UNIT_COST
        self.inventory_history.append(current_wc)

        # 2. Fulfill Demand
        filled = 0
        if self.inventory >= demand:
            filled = demand
            self.inventory -= demand
        else:
            filled = self.inventory
            self.inventory = 0
            # Stockout Penalty not explicitly in Efficiency metric, but affects Revenue (Lost Sales)
            
        self.total_revenue += filled * REVENUE_PER_UNIT

        # 3. Agent Ordering Decisions
        order_qty = 0
        
        # Scout Agent Signal
        signal_active = signal > SIGNAL_THRESHOLD
        
        inventory_position = self.inventory + sum(o[1] for o in self.pipeline)

        if self.use_smart_inventory:
            # Inventory Agent: (s, S) logic modulated by Signal
            # If Signal is Strong, we ensure we are at Target S
            # If Signal is Weak, we might hold less? Or simplified:
            # Smart Inventory Agent uses Signal to trigger "Top Up" early.
            
            # Logic: If Signal Active OR Inv < Min_s, Order up to Target
            if signal_active or inventory_position < MIN_INVENTORY_S:
                needed = TARGET_INVENTORY - inventory_position
                if needed > 0:
                    order_qty = needed
        else:
            # Heuristic Only: Fixed logic
            # "Scout triggers buy always when signal > 0.75"
            if signal_active and inventory_position < TARGET_INVENTORY: # Avoid infinite piling?
                # Prompt says "always when signal > 0.75". 
                # Pure implementation:
                order_qty = FIXED_ORDER_QTY
                
        # Credit Agent Constraints
        if order_qty > 0 and self.use_credit_limit:
            # Calculate projected WC impact
            cost_of_order = order_qty * UNIT_COST
            # Current WC (after sales) + New Order Cost ?
            # Usually Credit Limit is on Total Exposure (Inventory + Payables).
            # Let's assume Limit applies to (Current Inv Value + Incoming Pipeline Value + New Order)
            total_exposure = (self.inventory + sum(o[1] for o in self.pipeline)) * UNIT_COST
            
            if total_exposure + cost_of_order > CREDIT_LIMIT:
                # Cap the order
                allowable_value = CREDIT_LIMIT - total_exposure
                if allowable_value > 0:
                    order_qty = int(allowable_value // UNIT_COST)
                else:
                    order_qty = 0

        # Execute Order
        if order_qty > 0:
            arrival_time = month + LEAD_TIME
            self.pipeline.append([arrival_time, order_qty])

    def get_efficiency(self):
        if not self.inventory_history: return 0
        avg_wc = np.mean(self.inventory_history)
        if avg_wc == 0: return 0 # Infinite efficiency?
        return self.total_revenue / avg_wc

def run_ablation():
    configs = [
        "Full System",
        "No Credit Constraint",
        "Heuristic Only"
    ]
    
    results = {c: [] for c in configs}
    
    print("Running Ablation Study...")
    
    for _ in range(NUM_ITERATIONS):
        demands = np.random.poisson(DEMAND_MEAN, SIMULATION_MONTHS)
        signals = np.random.uniform(0, 1, SIMULATION_MONTHS)
        
        for cfg in configs:
            sim = AblationSim(cfg)
            for m in range(SIMULATION_MONTHS):
                sim.step(m, demands[m], signals[m])
            results[cfg].append(sim.get_efficiency())

    # Aggregate
    avg_eff = {k: np.mean(v) for k, v in results.items()}

    print("\nCapital Utilization Efficiency (Revenue / Working Capital):")
    for k, v in avg_eff.items():
        print(f"{k}: {v:.2f}x")

    # Plotting
    plt.figure(figsize=(10, 6))
    bars = plt.bar(avg_eff.keys(), avg_eff.values(), color=['#2ca02c', '#ff7f0e', '#1f77b4'])
    
    plt.title('Ablation Study: Capital Utilization Efficiency')
    plt.ylabel('Efficiency Ratio (Revenue / Avg WC)')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}x',
                 ha='center', va='bottom')

    plt.savefig(GRAPH_PATH)
    print(f"Graph saved to {GRAPH_PATH}")

if __name__ == "__main__":
    run_ablation()
