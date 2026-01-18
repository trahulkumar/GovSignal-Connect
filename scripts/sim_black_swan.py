
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
MONTHS = 36
NORMAL_DEMAND = 5
SPIKE_DEMAND = 50 
SPIKE_START = 12
SPIKE_END = 18

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
            if self.inventory + sum(o[1] for o in self.pipeline) < 80: trigger = True
        elif "Readiness" in self.policy_name:
            if signal > 0.75: trigger = True
            
        if trigger: self.pipeline.append([month + self.lead_time, 60])
