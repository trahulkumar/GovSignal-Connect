
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

# Simulation: Black Swan Event

NUM_ITERATIONS = 500
MONTHS = 36
NORMAL_DEMAND = 5
SPIKE_DEMAND = 50  # 10x spike
SPIKE_START = 12
SPIKE_END = 18
