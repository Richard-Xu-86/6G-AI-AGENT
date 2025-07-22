from collect_wifi import get_wifi_stats, reconnect_wifi, log_data
from stable_baselines3 import DQN #Deep Q-Network class, RL library
import numpy as np
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # absolute path of the folder containing this script.
MODEL_PATH = os.path.join(BASE_DIR, "..", "rl", "wifi_dqn_agent2.zip")

model = DQN.load(MODEL_PATH)

def run_ai_decision():
    before = get_wifi_stats()
    action = int(model.predict(before.reshape(1, -1))[0])

    if action == 1:
        reconnect_wifi()
        after = get_wifi_stats()
        switched = True
    else:
        after = before
        switched = False

        
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    log_data(timestamp, before, after, action, switched)

    return {
        "before": before.tolist(),
        "after": after.tolist(),
        "action": action,
        "switched": switched
    }
