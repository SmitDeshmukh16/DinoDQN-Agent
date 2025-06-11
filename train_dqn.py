import torch
import time
import torch.optim as optim
import torch.nn as nn
import numpy as np
import random
from models.model import QNetwork,ReplayBuffer
from gym_env.dino_gym_env import DinoGameEnv

# Hyperparameters
BATCH_SIZE = 64
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_END = 0.01
EPSILON_DECAY = 300
LR = 1e-3
TARGET_UPDATE = 10
REPLAY_BUFFER_SIZE = 10000
NUM_EPISODES = 1000
NUM_FRAMES = 10000


def epsilon_by_frame(frame_idx):
    return EPSILON_END + (EPSILON_START - EPSILON_END) * np.exp(-1. * frame_idx / EPSILON_DECAY)

def train():
    env = DinoGameEnv()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    state_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n

    policy_net = QNetwork(state_dim, n_actions).to(device)
    target_net = QNetwork(state_dim, n_actions).to(device)
    target_net.load_state_dict(policy_net.state_dict())
    optimizer = optim.Adam(policy_net.parameters(), lr=LR)

    replay_buffer = ReplayBuffer(REPLAY_BUFFER_SIZE)

    frame_idx = 0
    episode_rewards = []

    for episode in range(NUM_EPISODES):
        state ,_= env.reset()
        done = False
        episode_reward = 0

        while not done:
            frame_idx += 1
            epsilon = epsilon_by_frame(frame_idx)

            if random.random() > epsilon:
                with torch.no_grad():
                    state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
                    action = policy_net(state_tensor).max(1)[1].item()
            else:
                action = random.randrange(n_actions)

            next_state, reward, done,truncated, info = env.step(action)
            #print(f"Action: {action}, Reward: {reward}, Done: {done}")
            replay_buffer.push(state, action, reward, next_state, done)
            state = next_state
            episode_reward += reward
            time.sleep(0.03)

            if len(replay_buffer) >= BATCH_SIZE:
                states, actions, rewards, next_states, dones = replay_buffer.sample(BATCH_SIZE)
                states = torch.FloatTensor(states).to(device)
                actions = torch.LongTensor(actions).unsqueeze(1).to(device)
                rewards = torch.FloatTensor(rewards).unsqueeze(1).to(device)
                next_states = torch.FloatTensor(next_states).to(device)
                dones = torch.FloatTensor(dones).unsqueeze(1).to(device)

                q_values = policy_net(states).gather(1, actions)
                next_q_values = target_net(next_states).max(1)[0].unsqueeze(1)
                expected_q_values = rewards + GAMMA * next_q_values * (1 - dones)

                loss = nn.MSELoss()(q_values, expected_q_values)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if frame_idx % (TARGET_UPDATE * 30) == 0:
                target_net.load_state_dict(policy_net.state_dict())

        episode_rewards.append(episode_reward)
        print(f"Episode {episode} | Reward: {episode_reward} | Epsilon: {epsilon:.3f}")

    torch.save(policy_net.state_dict(), "dino_dqn_scratch.pth")

if __name__ == "__main__":
    train()