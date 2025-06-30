import React from 'react';
import './TruckDetails.css';

const TruckDetails = () => {
  const trucks = [
    { id: 1, name: 'Truck A', origin: 'Bangalore', destination: 'Mysore', driver: 'Ramesh' },
    { id: 2, name: 'Truck B', origin: 'Chennai', destination: 'Coimbatore', driver: 'Suresh' },
    { id: 3, name: 'Truck C', origin: 'Hyderabad', destination: 'Vizag', driver: 'Mahesh' },
  ];

  return (
    <div className="truck-container">
      <h2 className="truck-heading">Truck Details</h2>
      <div className="truck-table">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Truck Name</th>
              <th>Origin</th>
              <th>Destination</th>
              <th>Driver</th>
            </tr>
          </thead>
          <tbody>
            {trucks.map(truck => (
              <tr key={truck.id}>
                <td>{truck.id}</td>
                <td>{truck.name}</td>
                <td>{truck.origin}</td>
                <td>{truck.destination}</td>
                <td>{truck.driver}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TruckDetails;
