import React, { useEffect, useState } from 'react';

export default function HistoryPage() {
    const [history, setHistory] = useState([]);
    const [error, setError] = useState(null);

    const fetchHistory = () => {
        fetch("http://127.0.0.1:5000/api/history")
            .then((res) => {
                if (!res.ok) throw new Error("Failed to fetch");
                return res.json();
            })
            .then((data) => setHistory(data))
            .catch((err) => setError(err.message));
    };

    const handleReset = async () => {
        try {
            const res = await fetch("http://127.0.0.1:5000/api/reset_data", {
                method: "POST"
            });
            const result = await res.json();
            if (result.status === 'success') {
                alert("History reset!");
                fetchHistory(); // Refresh the table
            } else {
                alert("Reset failed.");
            }
        } catch (error) {
            console.error(error);
            alert("Error resetting data.");
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    if (error) return <div className="history-error">Error: {error}</div>;
    if (!history.length) return <div>No history to show.</div>;

    return (
        <div className="history-page">
            <div className="history-section">
                <h1 className="history-title">Wi-Fi History</h1>
                <button onClick={handleReset} className="history-button"> Reset History </button>
            </div>
            <table className="history-table">
                <thead>
                    <tr>
                        {Object.keys(history[0]).map((key) => (
                            <th key={key} className="history-header">{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {history.map((row, i) => (
                        <tr key={i}>
                            {Object.values(row).map((val, j) => (
                                <td key={j} className="history-data">{val}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
