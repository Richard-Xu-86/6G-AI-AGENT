import subprocess #Allows running terminal commands from Python
import re #Used for regular expressions, e.g. extracting numbers from ping output.
import time #For adding delays 
import numpy as np # For handling and returning the normalized Wi-Fi stats as an array.
from CoreWLAN import CWInterface   # macOS Wi-Fi interface access
import os
import csv

def get_rssi():
    try:
        iface = CWInterface.interface()
        return iface.rssiValue()
    except:
        return -100 # if not return -100 for bad signal (closer to 0 the better)
    
def get_ping_stats(host="8.8.8.8", count=3): #ping Google's DNS server 3 times
    try:
        result = subprocess.run(["ping", "-c", str(count), host], capture_output=True, text=True)
        output = result.stdout

        loss_match = re.search(r"(\d+)% packet loss", output)
        packet_loss = int(loss_match.group(1)) / 100 if loss_match else 0

        times = [float(m) for m in re.findall(r"time=(\d+\.\d+)", output)] #mutiple time outputs
        avg_latency = sum(times) / len(times) if times else 1000
        jitter = max(times) - min(times) if len(times) > 1 else 0.0

        return avg_latency, jitter, packet_loss
    except:
        return 1000, 0.1, 1.0

def get_wifi_stats():
    rssi = get_rssi()
    latency, jitter, packet_loss = get_ping_stats()

    rssi_norm = (rssi + 100) / 50 #to feed them to the ai agent, scale them similarily from (0-1)
    latency_norm = latency / 100 # higher the better
    jitter_norm = jitter
    loss_norm = packet_loss

    return np.array([rssi_norm, latency_norm, jitter_norm, loss_norm], dtype=np.float32) # packed into single numpy array

def reconnect_wifi():
    # 🔌 Turn Wi-Fi off
    subprocess.run(["/usr/sbin/networksetup", "-setairportpower", "en0", "off"]) #-setairportpower controls wifi power
    time.sleep(5)

    # 🔌 Turn Wi-Fi back on (macOS will reconnect to the best known AP)
    subprocess.run(["/usr/sbin/networksetup", "-setairportpower", "en0", "on"])
    time.sleep(5)  # Wait for reconnection

def log_data(timestamp, before, after, action, switched, filename="wifi_datas.csv"):
    file_exists = os.path.isfile(filename)
    is_empty = os.path.getsize(filename) == 0 if file_exists else True

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)

        # Only write the header if the file is new or empty
        if is_empty:
            writer.writerow([
                "Time", "Action", "Switched",
                "Before_RSSI", "Before_Latency", "Before_Jitter", "Before_PacketLoss",
                "After_RSSI", "After_Latency", "After_Jitter", "After_PacketLoss"
            ])
        
        writer.writerow([
            timestamp, action, switched,
            before[0], before[1], before[2], before[3],
            after[0], after[1], after[2], after[3]
        ])
