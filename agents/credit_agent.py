import numpy as np
try:
    from config import CAPITAL_COST
except ImportError:
    CAPITAL_COST = 0.08

class CreditAgent:
    """
    Agent responsible for Liquidity Management.
    Decides whether to approve capital requests or raise external funds.
    """
    def __init__(self, strategy="rule_based"):
        self.strategy = strategy
        self.wacc = CAPITAL_COST

    def act(self, observation, requested_capital=0.0):
        """
        Decides on capital release.
        observation: [Inventory, Cash, Pending, Volatility]
        requested_capital: Amount requested by Inventory Agent (implicit or explicit)
        """
        cash_on_hand = observation[1]
        volatility = observation[3]
        
        if self.strategy == "rule_based":
            # Conservative Strategy
            # Keep a buffer of 50000
            min_cash_buffer = 50000.0
            
            # If high volatility, we might want to hoard cash OR release it for panic buying?
            # Readiness Protocol: If Volatility High -> Release Capital for Strategic Buys.
            
            if volatility > 0.6:
                # "War Chest" logic: approve requests to secure inventory
                return 50000.0 # Release extra capital tranche
            
            if cash_on_hand < min_cash_buffer:
                # Liquidity Crunch: Deny or raise small amount
                return 10000.0 # Emergency credit line
            
            # Normal operations
            return 0.0

        elif self.strategy == "dqn":
            # Placeholder for future DQN implementation
            # Would need a separate Reward Function maximizing (Cash - Cost of Capital)
            return 0.0
        
        return 0.0
