# rl/train_agent.py
import os #For checking if the model file exists or saving it
from stable_baselines3 import DQN #Deep Q-Network agent
from stable_baselines3.common.monitor import Monitor #Wraps env to track training stats (like rewards, episode length)
from stable_baselines3.common.vec_env import DummyVecEnv #Required wrapper to make the env "vectorized" (SB3 expects this)
from gym_env import WiFiEnv #custom gym environment
from stable_baselines3.common.callbacks import EvalCallback, ProgressBarCallback, CallbackList #For tracking progress and evaluating the agent


# Create a monitored training environment
def make_train_env():
    return Monitor(WiFiEnv(training=True))

# Create a separate monitored evaluation environment
def make_eval_env():
    return Monitor(WiFiEnv(training=True))


# Wrapping in DummyVecEnv (SB3 expects this even for a single environment)
train_env = DummyVecEnv([make_train_env])
eval_env = DummyVecEnv([make_eval_env])

model_path = "wifi_dqn_agent2.zip"

# Load or create model
if os.path.exists(model_path):
    print("✅ Loaded existing model.")
    model = DQN.load(model_path, env=train_env, verbose=1)
else:
    print("📦 Created new model.")
    model = DQN("MlpPolicy", train_env, verbose=1)

# Evaluation callback using separate eval_env
eval_callback = EvalCallback(
    eval_env,
    best_model_save_path=None,
    log_path="./logs/",
    eval_freq=50,
    n_eval_episodes=1,
    verbose=1
)

# Progress bar
progress_bar = ProgressBarCallback()
callbacks = CallbackList([eval_callback, progress_bar])

# Train
print("🏋️ Training...")
model.learn(total_timesteps=3000000, callback=callbacks)

# Save model
model.save(model_path)
print("✅ Model saved.")