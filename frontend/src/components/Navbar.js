import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  const linkStyle = {
    margin: '0 15px',
    textDecoration: 'none',
    color: 'white',
    fontWeight: 'bold',
  };

  return (
    <nav style={{ background: '#2d2d2d', padding: '1rem' }}>
      <Link to="/" style={linkStyle}>Home</Link>
      <Link to="/login" style={linkStyle}>Login</Link>
      <Link to="/products" style={linkStyle}>Products</Link>
      <Link to="/product-details" style={linkStyle}>Product Details</Link>
      <Link to="/truck-details" style={linkStyle}>Truck Details</Link>
      <Link to="/sensor-readings" style={linkStyle}>Sensor Readings</Link>
    </nav>
  );
};

export default Navbar;
