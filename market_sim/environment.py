import gymnasium as gym
import numpy as np
from gymnasium import spaces
import random

# Import configuration constants (assuming config.py causes no circular imports or is in python path)
# In a real package structure, we might need relative imports or package installations.
# For now, we'll import from a sibling or root if possible, or just hardcode defaults if simple.
# Let's assume we can import from config.py if we run this as a module or add root to path.
try:
    from config import SIMULATION_STEPS, CAPITAL_COST, SERVICE_LEVEL_TARGET, SHOCK_PROBABILITY
except ImportError:
    # Fallback defaults if config not found in path
    SIMULATION_STEPS = 365
    CAPITAL_COST = 0.08
    SERVICE_LEVEL_TARGET = 0.99
    SHOCK_PROBABILITY = 0.05

class SupplyChainEnv(gym.Env):
    """
    OpenAI Gym Environment for a Volatile Supply Chain.
    Simulates inventory management under geopolitical shocks.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SupplyChainEnv, self).__init__()

        # State Space: [Current_Inventory, Cash_on_Hand, Pending_Orders, Market_Volatility_Index]
        # Using Box for continuous values, but Inventory/Orders could be Discrete if simplified.
        # We'll use semi-bounded Box.
        self.observation_space = spaces.Box(
            low=np.array([0, -np.inf, 0, 0.0]), 
            high=np.array([np.inf, np.inf, np.inf, 1.0]), 
            dtype=np.float32
        )

        # Action Space: [Order_Quantity, Release_Capital_Amount]
        # Order_Quantity: how much to buy.
        # Release_Capital_Amount: how much extra cash to approve (or request).
        self.action_space = spaces.Box(
            low=np.array([0, 0]), 
            high=np.array([1000, 1000000]), # Arbitrary maxes for normalization
            dtype=np.float32
        )

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        
        # Initial State
        self.inventory = 100.0
        self.cash = 100000.0
        self.pending_orders = 0.0
        self.volatility_index = 0.1 # Low initial risk

        return self._get_obs(), {}

    def _get_obs(self):
        return np.array([
            self.inventory, 
            self.cash, 
            self.pending_orders, 
            self.volatility_index
        ], dtype=np.float32)

    def step(self, action):
        order_qty = action[0]
        capital_release = action[1]
        
        # Update Volatility (External Signal Simulation)
        # In a real scenario, this would come from the LLM Nexus. 
        # Here we simulate random shocks if probability met.
        if random.random() < SHOCK_PROBABILITY:
            # External "Shock" event
            self.volatility_index = min(1.0, self.volatility_index + 0.3)
        else:
            # Mean reversion
            self.volatility_index = max(0.0, self.volatility_index * 0.95)

        # Demand Logic
        base_demand = 10 # Daily average
        # Shock Logic: Panic buying doubles demand if volatility is high
        demand_multiplier = 2.0 if self.volatility_index > 0.5 else 1.0
        actual_demand = np.random.poisson(base_demand * demand_multiplier)

        # Supply Chain Dynamics
        # 1. Receive Goods (Simplified: Orders arrive immediately next step or valid delay)
        # Let's assume 1 step lead time for simplicity in this version, 
        # or we treat 'pending_orders' as arriving today.
        # For this logic, let's say pending orders from yesterday arrive today.
        arrivals = self.pending_orders
        self.inventory += arrivals
        
        # 2. Fulfill Demand
        sold = min(self.inventory, actual_demand)
        self.inventory -= sold
        missed_sales = actual_demand - sold
        
        # 3. Place New Orders & Pay
        # Cost of goods simulated at $10/unit
        unit_cost = 10.0
        sales_price = 15.0
        
        cost_of_order = order_qty * unit_cost
        
        # Financial Check (Credit Agent Logic simplified or enforced)
        # If we requested capital, add it to cash (minus cost of capital?)
        # For simulation simplicity:
        self.cash += capital_release
        
        # Pay for order if we have cash
        if self.cash >= cost_of_order:
            self.cash -= cost_of_order
            self.pending_orders = order_qty # Arrives next step
        else:
            # Partial order or rejection
            affordable_qty = self.cash // unit_cost
            cost_of_order = affordable_qty * unit_cost
            self.cash -= cost_of_order
            self.pending_orders = affordable_qty
            
        # 4. Revenue
        revenue = sold * sales_price
        self.cash += revenue
        
        # Holding Cost
        holding_cost = self.inventory * 0.1
        self.cash -= holding_cost

        # Reward Calculation
        # Goal: Maximize Profit while keeping Service Level high?
        # Or minimize CCC?
        # Let's use a composite reward: Profit - Penalty for Stockouts
        profit = revenue - cost_of_order - holding_cost
        penalty = missed_sales * 20.0 # High penalty for stockout
        reward = profit - penalty

        self.current_step += 1
        done = self.current_step >= SIMULATION_STEPS
        
        info = {
            "demand": actual_demand, 
            "sold": sold, 
            "missed": missed_sales,
            "volatility": self.volatility_index
        }
        
        return self._get_obs(), reward, done, False, info

    def render(self, mode='human'):
        print(f"Step: {self.current_step} | Inv: {self.inventory:.1f} | Cash: {self.cash:.1f} | Vol: {self.volatility_index:.2f}")


class LegacyERP:
    """
    Baseline 'Dumb' Agent using Min/Max Logic.
    """
    def __init__(self, min_inventory=20, max_inventory=100):
        self.min_inventory = min_inventory
        self.max_inventory = max_inventory

    def act(self, observation):
        """
        observation: [Current_Inventory, Cash_on_Hand, Pending_Orders, Market_Volatility_Index]
        Returns: action [Order_Quantity, Release_Capital_Amount]
        """
        inventory = observation[0]
        
        # Deterministic Logic
        if inventory < self.min_inventory:
            order_qty = self.max_inventory - inventory
        else:
            order_qty = 0.0
            
        # Legacy systems don't manage capital dynamically usually, 
        # or they just ask for what they need.
        # We'll assume it requests enough cash to cover the order if needed, 
        # but the action space implies explicit management.
        # Let's simple-return 0 for capital release as it relies on existing cash or credit lines implicitly.
        return np.array([order_qty, 0.0])
