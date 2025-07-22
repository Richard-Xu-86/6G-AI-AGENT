# rl/gym_env.py
import gymnasium as gym #modern version of OpenAI Gym for rl
from gymnasium import spaces #defines allowed actions and observations
import numpy as np #for array operations and randomness.
import os, sys #for file paths

# Add backend path for real stats during evaluation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.collect_wifi import get_wifi_stats, reconnect_wifi


class WiFiEnv(gym.Env):
    def __init__(self, training=True):
        super(WiFiEnv, self).__init__()
        self.training = training

        self.action_space = spaces.Discrete(2)  # 0 = stay, 1 = reconnect
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)

        self.state = self._get_initial_state()
        self.step_count = 0
        self.max_steps = 100

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.step_count = 0
        self.state = self._get_initial_state()
        return self.state, {}

    def step(self, action):
        before = self.state

        if action == 1:  # reconnect
            after = self._simulate_state_change(before) if self.training else self._reconnect_and_measure()
        else:
            after = self._get_initial_state()

        reward = self._calculate_reward(before, after, action)
        self.state = after
        self.step_count += 1

        terminated = False
        truncated = self.step_count >= self.max_steps
        return after, reward, terminated, truncated, {}

    def _get_initial_state(self):
        if self.training:
            return np.random.uniform(0, 1, size=4).astype(np.float32)
        else:
            state = get_wifi_stats()
            if state is None or len(state) != 4:
                return np.array([0.0, 1.0, 1.0, 1.0], dtype=np.float32)
            return state

    def _reconnect_and_measure(self):
        reconnect_wifi()
        return self._get_initial_state()

    def _simulate_state_change(self, before):
        rssi, lat, jit, pl = before

        # Simulated effect of reconnect (generally positive)
        rssi += 0.03 + np.random.normal(0, 0.01)
        lat -= 0.04 + np.random.normal(0, 0.01)
        jit -= 0.03 + np.random.normal(0, 0.01)
        pl -= 0.02 + np.random.normal(0, 0.005)

        new_state = np.clip([rssi, lat, jit, pl], 0, 1)
        return np.array(new_state, dtype=np.float32)

    def _calculate_reward(self, before, after, action):
        rssi_b, lat_b, jit_b, pl_b = before
        rssi_a, lat_a, jit_a, pl_a = after

        delta_rssi = rssi_a - rssi_b
        delta_latency = lat_b - lat_a
        delta_jitter = jit_b - jit_a
        delta_packet_loss = pl_b - pl_a

        reward = (
            3.0 * delta_rssi +
            10.0 * delta_latency +
            15.0 * delta_jitter +
            20.0 * delta_packet_loss
        )

        # Strong penalty if all metrics got worse
        if delta_latency < 0 and delta_jitter < 0 and delta_rssi < 0:
            reward -= 10

        # Extra penalty for reconnects with no improvement
        if action == 1 and (delta_latency <= 0 and delta_jitter <= 0 and delta_rssi <= 0):
            reward -= 5

        # Bonus: reward staying if metrics were already good
        if action == 0 and (lat_b < 0.5 and jit_b < 50 and pl_b == 0):
            reward += 2.0

        return reward

