# 📶 6G AI Wi-Fi Optimization Agent

An AI-powered Wi-Fi access point optimization system that collects real-time performance metrics, simulates environments, and uses reinforcement learning to automatically select the best wireless network.

---

## 🔧 Project Structure

---

## 🚀 Features

- 📡 Real-time Wi-Fi data collection (RSSI, latency, jitter, packet loss)
- 🧠 Reinforcement learning agent (DQN with Stable-Baselines3)
- 📊 Web dashboard for visualization and interaction
- 🔁 Automatic switching between Wi-Fi access points

---

## 🛠️ Setup Instructions

### 1. Backend (Flask + RL Agent)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create a .env file
cp .env.example .env

# Run the Flask server
flask run

#start frontend
cd frontend
npm install

# Create .env file with API endpoint
echo "REACT_APP_API_URL=http://localhost:5000" > .env

npm start

#Training the agent
cd rl

python train_agent.py