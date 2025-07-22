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
<img width="1512" height="823" alt="Screenshot 2025-07-22 at 15 04 54" src="https://github.com/user-attachments/assets/e3f8d952-092f-484e-8b66-6e245147e814" />
<img width="1512" height="824" alt="Screenshot 2025-07-22 at 15 05 01" src="https://github.com/user-attachments/assets/83a038a0-3201-4db4-83b4-d13d6042a02e" />
<img width="1512" height="823" alt="Screenshot 2025-07-22 at 15 04 29" src="https://github.com/user-attachments/assets/7735b717-2d10-4e25-99dc-8c2f4e8b6139" />
<img width="1512" height="822" alt="Screenshot 2025-07-22 at 15 13 09" src="https://github.com/user-attachments/assets/29681f5f-4ff0-49e4-9e5d-4fff75f235f4" />
<img width="1512" height="824" alt="Screenshot 2025-07-22 at 15 09 00" src="https://github.com/user-attachments/assets/36f85832-6aef-4a72-b9dd-69b4b69143a2" />
<img width="1512" height="823" alt="Screenshot 2025-07-22 at 15 09 07" src="https://github.com/user-attachments/assets/e1a80dce-7951-44bf-99e6-807a25fba340" />
<img width="1512" height="823" alt="Screenshot 2025-07-22 at 15 09 15" src="https://github.com/user-attachments/assets/5d320543-5224-4c08-84c2-a29b01dd319f" />
<img width="1512" height="823" alt="Screenshot 2025-07-22 at 15 13 18" src="https://github.com/user-attachments/assets/2282c7d3-458a-40b7-8b8e-4ebc37f291d9" />


---

## 🛠️ Setup Instructions

### 1. Backend (Flask)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create a .env file
cp .env.example .env

# Run the Flask server
flask run

---
```

### 2. Frontend (React)
```bash
#start frontend
cd frontend
npm install

# Create .env file with API endpoint
echo "REACT_APP_API_URL=http://localhost:5000" > .env

npm start
```
### 3. RL AGENT (DQN)
```bash
#Training the agent
cd rl

python train_agent.py
```
