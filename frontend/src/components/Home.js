import React from 'react';
import './Home.css';

function Home() {
  return (
    <div className="home-container">
      <h1>Welcome to FoodChain IQ</h1>
      <p className="subtitle">
        A smart platform to monitor and manage your cold chain logistics efficiently.
      </p>

      <div className="feature-section">
        <h3>📦 Key Features</h3>
        <ul>
          <li>🚚 Track and monitor truck location and storage conditions</li>
          <li>🌡️ Real-time temperature and humidity sensors</li>
          <li>📋 Manage product data with expiry and quantity details</li>
          <li>🔒 Secure login for admins and authorized users</li>
        </ul>
      </div>

      <footer className="footer">
        &copy; {new Date().getFullYear()} FoodChain IQ | Cold Chain Monitoring System
      </footer>
    </div>
  );
}

export default Home;
