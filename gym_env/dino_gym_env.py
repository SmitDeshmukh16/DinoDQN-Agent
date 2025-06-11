import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame
from Game.Dino_game import DinoGame  # Import your class


class DinoGameEnv(gym.Env):
    metadata = {"render.modes": ["human"]}

    def __init__(self, render_mode=None):
        super(DinoGameEnv, self).__init__()
        self.dino_game = DinoGame()
        self.render_mode = render_mode
        
        # Normalized observation space [0-1]
        low = np.array([0, 0, 0, 0, -1, 0, 0, -1], dtype=np.float32)  # Added game_speed and jump_vel
        high = np.array([1, 1, 1, 1, 2, 1, 1, 1], dtype=np.float32)    # Adjusted for 8 dimensions
        
        self.observation_space = spaces.Box(low=low, high=high, dtype=np.float32)
        self.action_space = spaces.Discrete(3)

    def step(self, action):
        obs, reward, done = self.dino_game.step(action)
        return obs, reward, done, False, {}

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.dino_game.reset()
        return self.dino_game.get_observation(), {}

    def render(self, mode="human"):
        self.dino_game.render()  # Rendering handled inside DinoGame class

    def close(self):
        pygame.quit()