import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
try:
    from market_sim.environment import SupplyChainEnv
except ImportError:
    # If package structure issues, assume localized run
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from market_sim.environment import SupplyChainEnv

class InventoryAgent:
    """
    PPO Agent optimized for Inventory Management.
    Focuses on minimizing stockouts while managing holding costs.
    """
    def __init__(self, env=None, model_path=None):
        if env is None:
            self.env = make_vec_env(SupplyChainEnv, n_envs=1)
        else:
            self.env = env
            
        if model_path:
            self.model = PPO.load(model_path)
        else:
            # Initialize new PPO model
            # MlpPolicy is suitable for vector observations
            self.model = PPO("MlpPolicy", self.env, verbose=1, tensorboard_log="./tensorboard/")

    def train(self, total_timesteps=10000):
        print(f"Training Inventory Agent for {total_timesteps} steps...")
        self.model.learn(total_timesteps=total_timesteps)
        print("Training complete.")

    def save(self, path="ppo_inventory_agent"):
        self.model.save(path)

    def predict(self, observation):
        """
        Returns the recommended action.
        """
        action, _states = self.model.predict(observation, deterministic=True)
        return action
