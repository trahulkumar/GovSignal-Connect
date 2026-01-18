
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
