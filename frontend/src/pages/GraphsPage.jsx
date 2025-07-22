import React, { useEffect, useState } from 'react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

export default function GraphPage() {
  const [chartData, setChartData] = useState([]);
  const [averages, setAverages] = useState(null);
  const [timeRange, setTimeRange] = useState("all"); // "day", "month", "year", "all"
  const [error, setError] = useState(null);


  useEffect(() => {
    fetch(`http://127.0.0.1:5000/api/graph_rssi?range=${timeRange}`)
      .then(res => {
        if (!res.ok) throw new Error("Failed to load graph data");
        return res.json();
      })
      .then(data => {
        setChartData(data.chart_data || []);
        setAverages(data.avg_data || null);
      })
      .catch(err => {
        setError(err.message);
        setChartData([]);
        setAverages(null);
      });
  }, [timeRange]);

  const renderChart = (title, dataKeyBefore, dataKeyAfter, unit) => (
    <div className="graph-card">
      <h2 className="graph-title">{title}</h2>
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={chartData} margin={{ top: 20, right: 30, bottom: 110, left: 50 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" angle={-10} textAnchor="end" tick={{ fontSize: 10 }} />
          <YAxis />
          <Tooltip />
          <Legend verticalAlign="bottom" align="center" height={36} wrapperStyle={{ paddingTop: 20, marginBottom: -50, fontSize: 18 }} />
          <Line type="monotone" dataKey={dataKeyBefore} stroke="#8884d8" name={`Before: ${title}`} />
          <Line type="monotone" dataKey={dataKeyAfter} stroke="#82ca9d" name={`After: ${title}`} />
        </LineChart>
      </ResponsiveContainer>
      {averages && (
        <p className="graph-summary">
          <strong>Avg Before:</strong> {averages[`avg_${dataKeyBefore}`]} {unit} |{" "}
          <strong>Avg After:</strong> {averages[`avg_${dataKeyAfter}`]} {unit}
        </p>
      )}
    </div>
  );

  if (error) {
    return <div className="graphs-error">Error: {error}</div>;
  }

  if (chartData.length === 0) {
    return <div className="graphs-empty">No graph data available. Try running the agent or reconnecting Wi-Fi.</div>;
  }

  return (
    <div className="graphs-page">
      <div className="graphs-filter">
        <label htmlFor="range" className="graphs-TimeRange">Time Range:</label>
        <select id="range" value={timeRange} onChange={e => setTimeRange(e.target.value)} className="graphs-range">
          <option value="day">Past Day</option>
          <option value="week">Past Week</option>
          <option value="month">Past Month</option>
          <option value="year">Past Year</option>
          <option value="all">All Time</option>
        </select>
      </div>

      {renderChart("RSSI", "before_rssi", "after_rssi", "dBm")}
      {renderChart("Latency", "before_latency", "after_latency", "ms")}
      {renderChart("Jitter", "before_jitter", "after_jitter", "ms")}
    </div>
  );
}

