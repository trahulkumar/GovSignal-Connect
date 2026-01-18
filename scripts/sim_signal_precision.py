
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

# ... Constants ...
def generate_correlated_signal(demands, noise=0.1):
    signals = []
    for i in range(len(demands)):
        future = demands[i:i+3]
        if len(future) > 0 and np.mean(future) > 7:
            # High risk -> High Signal
            signals.append(np.clip(0.9 + np.random.normal(0, noise), 0, 1))
        else:
            signals.append(np.clip(0.1 + np.random.normal(0, noise), 0, 1))
    return signals
