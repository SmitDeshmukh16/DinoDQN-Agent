
# 🦖 DinoDQN-Agent

A Deep Q-Network (DQN) based reinforcement learning agent trained to play the classic Chrome Dino Game using Python and PyTorch.

## 🎯 Project Overview

This project uses Deep Q-Learning to train an AI agent to play the Chrome Dino game. The agent interacts with a custom-built game environment, learns from its actions, and improves over time to maximize its score.

## 📂 Project Structure

```
📁 DinoDQN-Agent/
├──gym_env
    └── dino_gym_env     #Gym Enviorment
├──models
    └── model.py         #DQN Model
├── Dino_game.py         # Dino Py Game
├── train_dqn.py         # DQN training script
├── test_dqn.py          # DQN evaluation script
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 🚀 Features

- Fully functional Chrome Dino environment
- DQN implementation with experience replay and target networks
- Training and evaluation modes
- Logs and model checkpoints (optional)

## 🧠 Technologies Used

- Python 3
- PyTorch
- NumPy
- OpenAI Gym (if integrated)
- Pygame (for game environment)

## 🛠️ Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/your-username/DinoDQN-Agent.git
cd DinoDQN-Agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Train the agent**
```bash
python train_dqn.py
```

4. **Test the agent**
```bash
python test_dqn.py
```
