
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

