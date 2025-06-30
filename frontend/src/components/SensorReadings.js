import React from 'react';
import './SensorReadings.css';

function SensorReadings() {
  const readings = [
    { time: "10:00 AM", temperature: "4.1°C", humidity: "65%" },
    { time: "10:30 AM", temperature: "4.3°C", humidity: "63%" },
  ];

  return (
    <div className="sensor-container">
      <h2>Sensor Readings</h2>
      <table className="sensor-table">
        <thead>
          <tr>
            <th>Time</th>
            <th>Temperature</th>
            <th>Humidity</th>
          </tr>
        </thead>
        <tbody>
          {readings.map((reading, index) => (
            <tr key={index}>
              <td>{reading.time}</td>
              <td>{reading.temperature}</td>
              <td>{reading.humidity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SensorReadings;
<div className="sensor-table-container">
  <table className="sensor-table">
    {/* existing code */}
  </table>
</div>
