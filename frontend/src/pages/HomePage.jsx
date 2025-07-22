import React from 'react';

export default function HomePage() {
  return (
    <div className="home-container">
      <section className="hero-section">
        <img src="/ai.gif" alt="Hero" className="hero-gif" />
        <div className="hero-content">
          <div className="hero-card">
            <h1 className="hero-title">Home</h1>
            <p className="hero-text">
              Welcome to your AI-powered Wi-Fi optimization assistant.
            </p>
          </div>
        </div>
      </section>

      <section className="info-section">
        <h2 className="info-title">
            🚀 What This App Does
        </h2>
        <p className="info-text-main">
            Our AI-powered assistant monitors your Wi-Fi connection in real-time and intelligently decides whether to stay connected or switch to a stronger access point for optimal performance.
        </p>
        <ul className="info-text">
            <li>
                <span className="info-stats">📶 RSSI:</span> Measures the received signal strength of your current Wi-Fi connection.
            </li>
            <li>
                <span className="info-stats">⏱️ Latency:</span> Time it takes for data to travel between your device and the server (in milliseconds).
            </li>
            <li>
                <span className="info-stats">⚡ Jitter:</span> Fluctuation in latency — high jitter can cause lag in video calls or gaming.
            </li>
            <li>
                <span className="info-stats">📦 Packet Loss:</span> Percentage of data packets lost during transmission — affects connection stability.
            </li>
        </ul>
      </section>

    </div>
  );
}