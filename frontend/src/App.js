import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Login from './components/Login';
import ProductList from './components/ProductList';
import ProductDetails from './components/ProductDetails';
import TruckDetails from './components/TruckDetails';
import SensorReadings from './components/SensorReadings';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/products" element={<ProductList />} />
        <Route path="/product-details" element={<ProductDetails />} />
        <Route path="/truck-details" element={<TruckDetails />} />
        <Route path="/sensor-readings" element={<SensorReadings />} />
      </Routes>
    </Router>
  );
}

export default App;
