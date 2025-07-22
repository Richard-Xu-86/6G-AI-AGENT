// src/pages/HomePage.js
import React, { useState } from 'react';

function RunAI() {
  const [result, setResult] = useState(null);

  async function runAnalysis() {
    const res = await fetch("http://127.0.0.1:5000/api/analyze");
    const data = await res.json();

    const before = data.before.map(x => x.toFixed(3));
    const after = data.after.map(x => x.toFixed(3));

    setResult({ before, after, action: data.action, switched: data.switched });
  }

  return (
    <div className="run-page">
      <h1 className="run-title">AI Wi-Fi Optimizer</h1>
      <button onClick={runAnalysis} className="run-button">Run AI Optimize</button>

      {result && (
        <div className="run-result">
          <div><strong>AI Action:</strong> {result.action === 1 ? "Reconnect" : "Stay Connected"}</div>
          <div><strong>Switched:</strong> {result.switched.toString()}</div>

          <div className="result-block">
            <h3>Before:</h3>
            <div className="result-metrics">
              <div><span>RSSI:</span><span>{result.before[0]}</span></div>
              <div><span>Latency:</span><span>{result.before[1]}</span></div>
              <div><span>Jitter:</span><span>{result.before[2]}</span></div>
              <div><span>Packet Loss:</span><span>{result.before[3]}</span></div>
            </div>

            <h3>After:</h3>
            <div className="result-metrics">
              <div><span>RSSI:</span><span>{result.after[0]}</span></div>
              <div><span>Latency:</span><span>{result.after[1]}</span></div>
              <div><span>Jitter:</span><span>{result.after[2]}</span></div>
              <div><span>Packet Loss:</span><span>{result.after[3]}</span></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default RunAI;
