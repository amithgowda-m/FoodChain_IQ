import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ProductList = () => {
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
    <div style={styles.container}>
      <h2 style={styles.heading}>Available Products</h2>
      <div style={styles.cardContainer}>
        {products.map((product, index) => (
          <div key={index} style={styles.card}>
            <h3 style={styles.name}>{product.name}</h3>
            <p style={styles.status}><strong>Status:</strong> {product.status}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '2rem',
    backgroundColor: '#f9f9f9',
    minHeight: '90vh',
  },
  heading: {
    fontSize: '2rem',
    marginBottom: '1rem',
    color: '#333',
  },
  cardContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    gap: '1rem',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: '10px',
    boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
    padding: '1rem',
    width: '250px',
  },
  name: {
    margin: 0,
    fontSize: '1.2rem',
    color: '#222',
  },
  status: {
    marginTop: '0.5rem',
    color: '#555',
  },
};

export default ProductList;
