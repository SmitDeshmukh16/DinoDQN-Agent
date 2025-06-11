import time
import random
from gym_env.dino_gym_env import DinoGameEnv
import torch
from models.model import QNetwork
env = DinoGameEnv()
obs_dim = env.observation_space.shape[0]
n_actions = env.action_space.n

# Initialize and load the model
model = QNetwork(obs_dim, n_actions)
model.load_state_dict(torch.load("dino_dqn_scratch.pth"))
model.eval()  # Set the model to evaluation mode


# Run one episode
state,_ = env.reset()

done = False
while not done:
    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    with torch.no_grad():
        q_values = model(state_tensor)
        action = torch.argmax(q_values).item()
    state, reward, done, truncate,info = env.step(action)
    env.render()

env.close()
