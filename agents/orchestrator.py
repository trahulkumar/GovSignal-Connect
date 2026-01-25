import numpy as np
try:
    from market_sim.environment import SupplyChainEnv
    from agents.inventory_agent import InventoryAgent
    from agents.credit_agent import CreditAgent
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from market_sim.environment import SupplyChainEnv
    from agents.inventory_agent import InventoryAgent
    from agents.credit_agent import CreditAgent

class Orchestrator:
    """
    Cooperative Multi-Agent System Loop.
    Coordinates Inventory Agent (PPO) and Credit Agent (Rule/DQN).
    """
    def __init__(self):
        self.env = SupplyChainEnv()
        self.inventory_agent = InventoryAgent(env=None) # Pass env if wrapping needed
        # We manually bridge them here for the orchestration loop
        self.credit_agent = CreditAgent()

    def run_episode(self):
        obs, _ = self.env.reset()
        done = False
        total_reward = 0
        
        print("Starting Cooperative Episode...")
        
        while not done:
            # 1. Inventory Agent decides what it WANTS to buy
            # Predict returns [Order_Qty, Capital_Request] (Initial PPO trained on full action space)
            # OR we can mask it so PPO only outputs Order Qty and Credit Agent outputs Capital.
            # For this 'Trifecta' concept, let's assume PPO suggests both, but Credit Agent overrides Capital.
            
            raw_action = self.inventory_agent.predict(obs)
            suggested_order_qty = raw_action[0]
            
            # 2. Credit Agent reviews the state (Financial Intelligence)
            credit_action = self.credit_agent.act(obs)
            
            # 3. Combine Actions
            # Final Action: [Inventory_Agent_Order, Credit_Agent_Cash_Release]
            final_action = np.array([suggested_order_qty, credit_action], dtype=np.float32)
            
            # 4. Execute in Environment
            new_obs, reward, done, truncated, info = self.env.step(final_action)
            
            obs = new_obs
            total_reward += reward
            
            if self.env.current_step % 50 == 0:
                 print(f"Step {self.env.current_step}: Reward={reward:.2f}, Vol={info['volatility']:.2f}")

        print(f"Episode Complete. Total Reward: {total_reward:.2f}")
        return total_reward

if __name__ == "__main__":
    orch = Orchestrator()
    # Pre-train inventory agent briefly if needed, or just run
    orch.inventory_agent.train(total_timesteps=1000)
    orch.run_episode()
