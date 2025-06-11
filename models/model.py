import torch.nn as nn
from collections import deque
import numpy as np
import random

class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QNetwork, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
            nn.Linear(128, output_dim)
        )

    def forward(self, x):
        return self.net(x)

class ReplayBuffer:
    def __init__(self, max_size):
        self.buffer = deque(maxlen=max_size)

    def push(self, state, action, reward, next_state, done):
        # Store them as-is (assuming state and next_state are already np.float32 arrays)
        self.buffer.append((np.array(state, dtype=np.float32),
                            action,
                            reward,
                            np.array(next_state, dtype=np.float32),
                            done))

    def sample(self, batch_size):
        samples = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*samples)

        return (
            np.array(states, dtype=np.float32),      # (batch_size, state_dim)
            np.array(actions),                       # (batch_size,)
            np.array(rewards, dtype=np.float32),     # (batch_size,)
            np.array(next_states, dtype=np.float32), # (batch_size, state_dim)
            np.array(dones, dtype=np.float32)        # (batch_size,)
        )

    def __len__(self):
        return len(self.buffer)

