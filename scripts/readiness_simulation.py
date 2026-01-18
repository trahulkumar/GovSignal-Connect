
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
INITIAL_INVENTORY = 60
ORDER_QTY = 60

# Policy A: Legacy ERP
POLICY_A_LEAD_TIME = 12
POLICY_A_ROP = 80  # 12 * 5 + 20 safety stock

# Policy B: Readiness Protocol
POLICY_B_LEAD_TIME = 3
POLICY_B_SIGNAL_THRESHOLD = 0.75

# Get project root (assuming script is in scripts/ subdir)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
GRAPH_1_PATH = os.path.join(OUTPUT_DIR, "lead_time_comparison.png")
GRAPH_2_PATH = os.path.join(OUTPUT_DIR, "total_cost_comparison.png")

class SupplyChainSim:
    def __init__(self, policy_name, lead_time, initial_inv=INITIAL_INVENTORY):
        self.policy_name = policy_name
        self.lead_time = lead_time
        self.inventory = initial_inv
        self.pipeline = []  # List of [arrival_month, quantity]
        self.total_holding_cost = 0
        self.total_stockout_cost = 0
        self.stockout_events = 0
        self.orders_placed = 0

    def step(self, month, demand, signal_confidence):
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
            # Stockout
            self.stockout_events += 1
            self.total_stockout_cost += STOCKOUT_PENALTY
            self.inventory = 0 # Assume lost sales or backorder? Prompt implies penalty per event.
                               # Let's assume lost sales for simplicity in inventory tracking, 
                               # but the penalty captures the impact.
        
        # 3. Holding Cost
        self.total_holding_cost += self.inventory * HOLDING_COST_PER_UNIT

        # 4. Place Orders (Logic)
        order_triggered = False
        if self.policy_name == "Policy A (Legacy ERP)":
            # ROP Logic: Check total position (Inventory + On Order) ? 
            # Standard ROP usually checks Inventory Position = On Hand + On Order - Backorder
            # Prompt says "Trigger purchase ONLY when inventory < min_threshold". 
            # "inventory" usually means On Hand. If we ignore On Order, we might double order.
            # However, for 12 month lead time, simple ROP on On-Hand would trigger constantly if it doesn't account for pipeline.
            # Let's assume Inventory Position (Hand + Pipeline) < ROP.
            inventory_position = self.inventory + sum(o[1] for o in self.pipeline)
            if inventory_position < POLICY_A_ROP:
                order_triggered = True

        elif self.policy_name == "Policy B (Readiness Protocol)":
            # Signal Logic: Trigger when signal > 0.75.
            # regardless of inventory.
            # To avoid spamming orders every single month if signal remains high, 
            # we might need a cooldown or check if we already responded. 
            # Prompt says "Trigger purchase when external_signal_confidence > 0.75 (regardless of inventory)".
            # We will implement strictly as requested. IF signal > 0.75, buy.
            if signal_confidence > POLICY_B_SIGNAL_THRESHOLD:
                order_triggered = True

        if order_triggered:
            arrival_time = month + self.lead_time
            self.pipeline.append([arrival_time, ORDER_QTY])
            self.orders_placed += 1

    def total_cost(self):
        return self.total_holding_cost + self.total_stockout_cost

def run_simulation():
    results_a = []
    results_b = []

    print(f"Starting simulation with N={NUM_ITERATIONS} iterations...")

    for i in range(NUM_ITERATIONS):
        # Generate Demand Profile (fixed seed per iteration for fairness if we wanted pairs, 
        # but global seed handled above ensures reproducibility)
        demands = np.random.poisson(DEMAND_MEAN, SIMULATION_MONTHS)
        
        # Generate Signal Profile
        # Signal needs to be somewhat rare to not bankrupt Policy B.
        # Let's assume a signal that spikes occasionally. 
        # Using a Beta distribution or similar to bias towards low values but occasional highs.
        # Or simple uniform.
        # Let's use Uniform[0,1] but only > 0.75 triggers. 
        # If random, it triggers 25% of months (3 times a year). That's a bit high for "Strategic" maybe?
        # Let's assume "Readiness" signals are specialized. 
        # Let's stick to Uniform for complying with "confidence > 0.75".
        signals = np.random.uniform(0, 1, SIMULATION_MONTHS)
        
        # --- Policy A ---
        sim_a = SupplyChainSim("Policy A (Legacy ERP)", POLICY_A_LEAD_TIME)
        # --- Policy B ---
        sim_b = SupplyChainSim("Policy B (Readiness Protocol)", POLICY_B_LEAD_TIME)

        for m in range(SIMULATION_MONTHS):
            sim_a.step(m, demands[m], signals[m])
            sim_b.step(m, demands[m], signals[m])

        results_a.append(sim_a.total_cost())
        results_b.append(sim_b.total_cost())

    return results_a, results_b

def generate_visualizations(results_a, results_b):
    # Graph 1: Lead Time Comparison
    # Since Lead Times are fixed parameters (12 months vs 3 months), 
    # a "Distribution" graph isn't needed if we take the prompt literally about "Average Days to Delivery".
    # However, to make it a "Graph", we can compare the Fixed Lead Times as a bar chart.
    
    plt.figure(figsize=(8, 6))
    policies = ['Policy A\n(Legacy ERP)', 'Policy B\n(Readiness Protocol)']
    # Convert months to days (approx 30 days/month)
    avg_days = [POLICY_A_LEAD_TIME * 30, POLICY_B_LEAD_TIME * 30]
    bars = plt.bar(policies, avg_days, color=['#808080', '#007acc'])
    
    plt.title('Lead Time Comparison (Average Days to Delivery)')
    plt.ylabel('Days')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{int(height)} days',
                 ha='center', va='bottom')
    
    plt.savefig(GRAPH_1_PATH)
    plt.close()

    # Graph 2: Total Cost of Readiness
    plt.figure(figsize=(10, 6))
    data = [results_a, results_b]
    plt.boxplot(data, labels=policies, patch_artist=True, 
                boxprops=dict(facecolor='#D3D3D3', color='black'),
                medianprops=dict(color='red'))
    
    # Color Policy B box differently
    ax = plt.gca()
    box_patches = [patch for patch in ax.patches if isinstance(patch, matplotlib.patches.PathPatch)] # Dependent on implementation, boxplot returns dict usually if not patch_artist
    # Re-doing simply:
    # boxplot returns a dictionary
    
    plt.title('Total Cost of Readiness (Holding + Stockout Penalties)')
    plt.ylabel('Total Cost ($)')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.savefig(GRAPH_2_PATH)
    plt.close()

if __name__ == "__main__":
    import matplotlib
    import matplotlib.patches
    
    results_a, results_b = run_simulation()
    generate_visualizations(results_a, results_b)

    avg_cost_a = np.mean(results_a)
    avg_cost_b = np.mean(results_b)

    print(f"Policy A Average Cost: ${avg_cost_a:,.2f}")
    print(f"Policy B Average Cost: ${avg_cost_b:,.2f}")
    
    # Metric Calculation
    latency_reduction = ((POLICY_A_LEAD_TIME - POLICY_B_LEAD_TIME) / POLICY_A_LEAD_TIME) * 100
    
    # ROI of Pre-emptive buy (assuming Cost A is baseline loss, Cost B is improved state)
    # ROI = (Gain from Investment - Cost of Investment) / Cost of Investment
    # Here, "Investment" is the Readiness Protocol's cost structure. 
    # Usually simplest metric is % Cost Savings.
    # ROI as requested: "ROI of the pre-emptive buy".
    # Let's interpret as: Savings / Cost_B * 100.
    savings = avg_cost_a - avg_cost_b
    roi = (savings / avg_cost_b) * 100 if avg_cost_b > 0 else 0

    print(f"\n--- Metrics ---")
    print(f"Reduction in Readiness Latency: {latency_reduction:.1f}%")
    print(f"ROI of Pre-emptive Buy: {roi:.1f}%")
    print(f"Visualizations saved to:\n  - {GRAPH_1_PATH}\n  - {GRAPH_2_PATH}")

# Refined logic

# Updated metrics

# Final polish
