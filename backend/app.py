from flask import Flask, jsonify, request
from flask_cors import CORS #Cross-Origin Resource Sharing, allows react to access flask api
import pandas as pd #reading and handling csv files
from datetime import datetime, timedelta
from reconnect_measure import run_ai_decision
#from graphs_pandas import before_rssi, after_rssi, before_latency, after_latency, before_jitter,after_jitter
import os
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from React

@app.route('/api/history')
def full_data():
    try:
        df = pd.read_csv("wifi_datas.csv")
        df.columns = df.columns.str.strip()  # Ensure no extra spaces

        # Sort by most recent first
        df = df.sort_values(by="Time", ascending=False)

        return df.to_dict(orient="records")
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/api/analyze")
def analyze():
    result = run_ai_decision()
    return jsonify(result)

@app.route("/api/graph_rssi")
def graph_rssi():
    if not os.path.exists("wifi_datas.csv"):
        return jsonify({"chart_data": [], "avg_data": {}})

    df = pd.read_csv("wifi_datas.csv")
    df.columns = df.columns.str.strip()

    if df.empty:
        return jsonify({"chart_data": [], "avg_data": {}})

    # Convert time column to datetime
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    df = df.dropna(subset=["Time"])

    if df.empty:
        return jsonify({"chart_data": [], "avg_data": {}})

    # ⏱️ Filter by time range (from query param)
    range_filter = request.args.get("range", "all")  # "day", "month", "week",  "year", "all"
    now = datetime.now()

    if range_filter == "day":
        df = df[df["Time"] > now - timedelta(days=1)]
    elif range_filter == "week":
        df = df[df["Time"] > now - timedelta(days=7)]
    elif range_filter == "month":
        df = df[df["Time"] > now - timedelta(days=30)]
    elif range_filter == "year":
        df = df[df["Time"] > now - timedelta(days=365)]
    # else: no filtering for "all"

    if df.empty:
        return jsonify({"chart_data": [], "avg_data": {}})
    
    # Unnormalize
    df["real_before_rssi"] = df["Before_RSSI"] * 50 - 100
    df["real_after_rssi"] = df["After_RSSI"] * 50 - 100
    df["real_before_latency"] = df["Before_Latency"] * 100
    df["real_after_latency"] = df["After_Latency"] * 100
    df["real_before_jitter"] = df["Before_Jitter"]
    df["real_after_jitter"] = df["After_Jitter"]

    # Build array of time-series data for frontend
    time_strings = df["Time"].dt.strftime("%Y-%m-%d %H:%M:%S")

    chart_data = [
        {
            "time": time,
            "before_rssi": b_rssi,
            "after_rssi": a_rssi,
            "before_latency": b_lat,
            "after_latency": a_lat,
            "before_jitter": b_jit,
            "after_jitter": a_jit,
        }
        for time, b_rssi, a_rssi, b_lat, a_lat, b_jit, a_jit in zip(
            time_strings,
            df["real_before_rssi"],
            df["real_after_rssi"],
            df["real_before_latency"],
            df["real_after_latency"],
            df["real_before_jitter"],
            df["real_after_jitter"],
        )
    ]

    # Averages
    avg_data = {
        "avg_before_rssi": round(df["real_before_rssi"].mean(), 2),
        "avg_after_rssi": round(df["real_after_rssi"].mean(), 2),
        "avg_before_latency": round(df["real_before_latency"].mean(), 2),
        "avg_after_latency": round(df["real_after_latency"].mean(), 2),
        "avg_before_jitter": round(df["real_before_jitter"].mean(), 2),
        "avg_after_jitter": round(df["real_after_jitter"].mean(), 2),
    }

    return jsonify({
        "chart_data": chart_data,
        "avg_data":avg_data
    })

@app.route('/api/reset_data', methods=['POST'])
def reset_data():
    try:
        open('wifi_datas.csv', 'w').close()  # <-- this clears your actual CSV
        return jsonify({"status": "success", "message": "Data reset."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)




