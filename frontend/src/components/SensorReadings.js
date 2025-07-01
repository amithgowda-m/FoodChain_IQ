import React, { useState } from 'react';
import axios from 'axios';

const SensorReadings = () => {
  const [productType, setProductType] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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
    </div>
  );
};

export default SensorReadings;