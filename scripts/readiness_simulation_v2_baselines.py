"""
Readiness Simulation v2: Expanded Baselines
===========================================

Goal:
-----
Compare the 'Readiness Protocol' against robust baselines including:
1. Legacy ERP (Standard ROP)
2. (s, S) Standard Inventory Policy
3. Perfect Forecast Oracle (Theoretical Upper Bound)

Key Metrics:
------------
- Service Level (Fill Rate %)
- Average Backorder Duration (Days)
- Total Cost Breakdown (Holding vs Stockout vs Ordering)

Policies:
---------
- Policy A: Legacy ERP (Lead Time=12m)
- Policy B: Readiness Protocol (Lead Time=3m, Signal-based)
- Policy C: (s, S) Policy (Lead Time=12m)
- Policy D: Perfect Forecast Oracle (Lead Time=3m)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Set random seed for reproducibility
np.random.seed(42)

# --- Configuration ---
NUM_ITERATIONS = 1000
SIMULATION_MONTHS = 36
DEMAND_MEAN = 5  # Poisson lambda
HOLDING_COST_PER_UNIT = 500
STOCKOUT_PENALTY = 50000
ORDERING_COST = 2000  # Cost per order placement
INITIAL_INVENTORY = 60
ORDER_QTY = 60

# Policy A: Legacy ERP (Standard ROP)
POLICY_A_LEAD_TIME = 12
POLICY_A_ROP = 80

# Policy B: Readiness Protocol
POLICY_B_LEAD_TIME = 3
POLICY_B_SIGNAL_THRESHOLD = 0.75

# Policy C: (s, S) Policy
# Utilizing same lead time as Legacy for fair baseline comparison of "Inventory Strategy" vs "Readiness Speed"
POLICY_C_LEAD_TIME = 12
POLICY_C_MIN_s = 60
POLICY_C_MAX_S = 180

# Policy D: Perfect Forecast Oracle
# Theoretical bound: knows demand 3 months ahead, lead time 3 months
POLICY_D_LEAD_TIME = 3

# Get project root (assuming script is in root)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output", "v2_baselines")
os.makedirs(OUTPUT_DIR, exist_ok=True)
GRAPH_COMP_PATH = os.path.join(OUTPUT_DIR, "baseline_comparison.png")
GRAPH_COST_PATH = os.path.join(OUTPUT_DIR, "cost_breakdown.png")

class SupplyChainSim:
    def __init__(self, policy_name, lead_time, initial_inv=INITIAL_INVENTORY):
        self.policy_name = policy_name
        self.lead_time = lead_time
        self.inventory = initial_inv
        self.pipeline = []  # List of [arrival_month, quantity]
        
        # Costs
        self.total_holding_cost = 0
        self.total_stockout_cost = 0
        self.total_ordering_cost = 0
        
        # Metrics
        self.total_demand = 0
        self.total_filled = 0
        self.stockout_events = 0
        self.current_stockout_duration = 0
        self.completed_stockout_durations = []
        self.orders_placed = 0

    def step(self, month, demand, signal_confidence, future_demand=None):
        self.total_demand += demand
        
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
            filled = demand
            self.inventory -= demand
            
            # If we were in a stockout, it ends now (if inventory > 0)
            if self.current_stockout_duration > 0:
                self.completed_stockout_durations.append(self.current_stockout_duration)
                self.current_stockout_duration = 0
        else:
            # Stockout
            filled = self.inventory
            missed = demand - self.inventory
            self.inventory = 0
            
            if filled < demand: # Genuine stockout
                self.stockout_events += 1
                self.total_stockout_cost += STOCKOUT_PENALTY
                self.current_stockout_duration += 1
            
        self.total_filled += filled
        
        # 3. Holding Cost
        self.total_holding_cost += self.inventory * HOLDING_COST_PER_UNIT

        # 4. Place Orders (Logic)
        order_qty = 0
        
        # Calculate Inventory Position = On Hand + On Order
        inventory_position = self.inventory + sum(o[1] for o in self.pipeline)

        if self.policy_name == "Policy A (Legacy ERP)":
            if inventory_position < POLICY_A_ROP:
                order_qty = ORDER_QTY

        elif self.policy_name == "Policy B (Readiness Protocol)":
            if signal_confidence > POLICY_B_SIGNAL_THRESHOLD:
                order_qty = ORDER_QTY

        elif self.policy_name == "(s, S) Policy":
            if inventory_position < POLICY_C_MIN_s:
                order_qty = POLICY_C_MAX_S - inventory_position

        elif self.policy_name == "Perfect Forecast Oracle":
            # Order exactly what is needed for arrival time
            target_month = month + self.lead_time
            if future_demand is not None and target_month < len(future_demand):
                req_demand = future_demand[target_month]
                order_qty = req_demand
            else:
                order_qty = 0 # End of simulation approaching

        if order_qty > 0:
            arrival_time = month + self.lead_time
            self.pipeline.append([arrival_time, order_qty])
            self.orders_placed += 1
            self.total_ordering_cost += ORDERING_COST

    def finish(self):
        # Capture any ongoing stockout at simulation end
        if self.current_stockout_duration > 0:
            self.completed_stockout_durations.append(self.current_stockout_duration)
            
    def total_cost(self):
        return self.total_holding_cost + self.total_stockout_cost + self.total_ordering_cost

    def service_level(self):
        if self.total_demand == 0: return 1.0
        return self.total_filled / self.total_demand

    def avg_backorder_duration(self):
        if not self.completed_stockout_durations:
            return 0.0
        # Convert months to days (approx 30 days)
        return np.mean(self.completed_stockout_durations) * 30

def run_simulation():
    policies = ["Policy A (Legacy ERP)", "Policy B (Readiness Protocol)", "(s, S) Policy", "Perfect Forecast Oracle"]
    results = {p: {'costs': [], 'service_levels': [], 'backorder_days': [], 'holding_costs': [], 'stockout_costs': [], 'ordering_costs': []} for p in policies}

    print(f"Starting simulation with N={NUM_ITERATIONS} iterations...")

    for i in range(NUM_ITERATIONS):
        demands = np.random.poisson(DEMAND_MEAN, SIMULATION_MONTHS)
        signals = np.random.uniform(0, 1, SIMULATION_MONTHS)
        
        sims = [
            SupplyChainSim(policies[0], POLICY_A_LEAD_TIME),
            SupplyChainSim(policies[1], POLICY_B_LEAD_TIME),
            SupplyChainSim(policies[2], POLICY_C_LEAD_TIME),  # (s,S) uses standard lead time
            SupplyChainSim(policies[3], POLICY_D_LEAD_TIME)
        ]

        for m in range(SIMULATION_MONTHS):
            for sim in sims:
                sim.step(m, demands[m], signals[m], future_demand=demands)
        
        for sim in sims:
            sim.finish()
            p = sim.policy_name
            results[p]['costs'].append(sim.total_cost())
            results[p]['service_levels'].append(sim.service_level())
            results[p]['backorder_days'].append(sim.avg_backorder_duration())
            results[p]['holding_costs'].append(sim.total_holding_cost)
            results[p]['stockout_costs'].append(sim.total_stockout_cost)
            results[p]['ordering_costs'].append(sim.total_ordering_cost)

    return results

def generate_visualizations(results):
    policies = list(results.keys())
    
    # --- 1. Baseline Comparison (Service Level & Backorder Duration) ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Service Level
    avg_sl = [np.mean(results[p]['service_levels']) * 100 for p in policies]
    axes[0].bar(policies, avg_sl, color=['#808080', '#007acc', '#2ca02c', '#d62728'])
    axes[0].set_title('Service Level (Fill Rate %)')
    axes[0].set_ylabel('Percentage (%)')
    axes[0].set_ylim(0, 105)
    for i, v in enumerate(avg_sl):
        axes[0].text(i, v + 1, f"{v:.1f}%", ha='center')
    axes[0].tick_params(axis='x', rotation=45)

    # Backorder Duration
    avg_bd = [np.mean(results[p]['backorder_days']) for p in policies]
    axes[1].bar(policies, avg_bd, color=['#808080', '#007acc', '#2ca02c', '#d62728'])
    axes[1].set_title('Average Backorder Duration')
    axes[1].set_ylabel('Days')
    for i, v in enumerate(avg_bd):
        axes[1].text(i, v + 0.5, f"{v:.1f} d", ha='center')
    axes[1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig(GRAPH_COMP_PATH)
    plt.close()

    # --- 2. Cost Breakdown (Stacked Bar) ---
    plt.figure(figsize=(10, 6))
    
    avg_holding = [np.mean(results[p]['holding_costs']) for p in policies]
    avg_stockout = [np.mean(results[p]['stockout_costs']) for p in policies]
    avg_ordering = [np.mean(results[p]['ordering_costs']) for p in policies]
    
    bar_width = 0.5
    indices = np.arange(len(policies))
    
    p1 = plt.bar(indices, avg_holding, bar_width, label='Holding Cost', color='#1f77b4')
    p2 = plt.bar(indices, avg_stockout, bar_width, bottom=avg_holding, label='Stockout Cost', color='#ff7f0e')
    p3 = plt.bar(indices, avg_ordering, bar_width, bottom=np.array(avg_holding)+np.array(avg_stockout), label='Ordering Cost', color='#2ca02c')
    
    plt.title('Cost Breakdown by Policy')
    plt.xticks(indices, policies, rotation=45, ha='right')
    plt.ylabel('Cost ($)')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(GRAPH_COST_PATH)
    plt.close()

    print(f"Visualizations saved to:\n  - {GRAPH_COMP_PATH}\n  - {GRAPH_COST_PATH}")

if __name__ == "__main__":
    results = run_simulation()
    generate_visualizations(results)

    # Print Text Metrics
    print("\n--- Simulation Summary ---")
    for p in results:
        cost = np.mean(results[p]['costs'])
        sl = np.mean(results[p]['service_levels']) * 100
        bd = np.mean(results[p]['backorder_days'])
        print(f"{p}: Total Cost=${cost:,.0f} | Service Level={sl:.1f}% | Backorder={bd:.1f} days")
