import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProductDetails = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/products')
      .then(response => {
        setProducts(response.data);
      })
      .catch(error => {
        console.error('Error fetching products:', error);
      });
  }, []);

  return (
    <div style={{ padding: '40px' }}>
      <h1 style={{
        textAlign: 'center',
        fontSize: '32px',
        marginBottom: '30px',
        fontWeight: 'bold',
        color: '#2e7d32'
      }}>
        🛒 Available Products
      </h1>

      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        justifyContent: 'center',
        gap: '20px',
      }}>
        {products.length === 0 ? (
          <p style={{ fontSize: '18px' }}>No products available.</p>
        ) : (
          products.map((product, index) => (
            <div
              key={index}
              style={{
                border: '1px solid #ddd',
                borderRadius: '12px',
                padding: '20px',
                backgroundColor: '#f0f9ff',
                minWidth: '200px',
                maxWidth: '250px',
                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
                transition: 'transform 0.2s',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.transform = 'scale(1.02)')}
              onMouseLeave={(e) => (e.currentTarget.style.transform = 'scale(1)')}
            >
              <h3 style={{ marginBottom: '10px', color: '#0d47a1' }}>{product.name}</h3>
              <p style={{ margin: 0, color: '#555' }}>{product.status}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ProductDetails;
