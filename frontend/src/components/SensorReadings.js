import React, { useState, useEffect } from 'react';
import axios from 'axios';

const SensorReadings = () => {
  const [productType, setProductType] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!productType.trim()) {
      setError("Please select a product type");
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/api/v1/predict', {
        product_type: productType,
      });

      setPrediction(response.data); // Set full response
    } catch (err) {
      console.error(err);
      setError("Failed to get prediction from server.");
    } finally {
      setLoading(false);
    }
  };

  // Fetch historical predictions
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get("http://localhost:8000/api/v1/history");
        setHistory(res.data.history || []);
      } catch (err) {
        console.error("Failed to fetch history:", err);
      }
    };

    fetchHistory(); // Initial fetch
    const interval = setInterval(fetchHistory, 5000); // Refresh every 5 sec

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial' }}>
      <h2>Select Product Type</h2>

      <form onSubmit={handleSubmit}>
        <label>
          Product Type:
          <select
            value={productType}
            onChange={(e) => setProductType(e.target.value)}
            style={{
              marginLeft: '10px',
              padding: '5px',
              width: '200px',
              fontSize: '16px'
            }}
          >
            <option value="">-- Select --</option>
            <option value="Fruits">Fruits</option>
            <option value="Vegetables">Vegetables</option>
            <option value="Dairy">Dairy</option>
            <option value="Meat">Meat</option>
            <option value="Milk">Milk</option>
          </select>
        </label>

        <br /><br />
        <button
          type="submit"
          disabled={loading || !productType}
          style={{
            padding: '10px 20px',
            backgroundColor: loading ? '#aaa' : '#007bff',
            color: 'white',
            border: 'none',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          {loading ? 'Predicting...' : 'Predict Spoilage Risk'}
        </button>
      </form>

      {/* Prediction Result */}
      {prediction && (
        <div style={{
          marginTop: '30px',
          padding: '20px',
          backgroundColor: prediction.prediction === 'Spoiled' ? '#f8d7da' : '#d4edda',
          color: prediction.prediction === 'Spoiled' ? '#721c24' : '#155724',
          borderRadius: '5px',
          fontWeight: 'bold'
        }}>
          <h3>Prediction: {prediction.prediction}</h3>
          <p><strong>Sensor Data Used:</strong></p>
          <ul>
            <li>🌡️ Temperature: {prediction.sensor_data.temperature}°C</li>
            <li>💧 Humidity: {prediction.sensor_data.humidity}%</li>
            <li>🧊 Shock Level: {prediction.sensor_data.shock_level}g</li>
          </ul>
        </div>
      )}

      {/* Error Message */}
      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}

      {/* Show/Hide Prediction History Button */}
      <div style={{ marginTop: '40px' }}>
        <button onClick={() => setShowHistory(!showHistory)}>
          {showHistory ? "Hide Prediction History" : "Show Prediction History"}
        </button>

        {/* Prediction History Table */}
        {showHistory && (
          <div style={{ marginTop: '20px' }}>
            <h3>📜 Prediction History</h3>
            <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
              <thead>
                <tr style={{ background: '#f0f0f0' }}>
                  <th style={tableHeaderStyle}>ID</th>
                  <th style={tableHeaderStyle}>Product</th>
                  <th style={tableHeaderStyle}>Prediction</th>
                  <th style={tableHeaderStyle}>Temperature (°C)</th>
                  <th style={tableHeaderStyle}>Humidity (%)</th>
                  <th style={tableHeaderStyle}>Shock Level (g)</th>
                  <th style={tableHeaderStyle}>Timestamp</th>
                </tr>
              </thead>
              <tbody>
                {history.map((entry, index) => (
                  <tr key={index} style={tableRowStyle(entry.prediction)}>
                    <td style={tableCellStyle}>{entry.id}</td>
                    <td style={tableCellStyle}>{entry.product_type}</td>
                    <td style={{
                      ...tableCellStyle,
                      color: entry.prediction === 'Spoiled' ? '#721c24' : '#155724',
                      fontWeight: 'bold'
                    }}>{entry.prediction}</td>
                    <td style={tableCellStyle}>{entry.temperature}</td>
                    <td style={tableCellStyle}>{entry.humidity}</td>
                    <td style={tableCellStyle}>{entry.shock_level}</td>
                    <td style={tableCellStyle}>{new Date(entry.timestamp).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

// Styles for the table
const tableHeaderStyle = {
  border: '1px solid #ccc',
  padding: '8px',
  textAlign: 'left'
};

const tableCellStyle = {
  border: '1px solid #eee',
  padding: '8px'
};

const tableRowStyle = (prediction) => ({
  borderBottom: '1px solid #ddd'
});

export default SensorReadings;