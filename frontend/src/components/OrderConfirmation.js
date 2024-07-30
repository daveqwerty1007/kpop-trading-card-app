import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import './OrderConfirmation.css';

const OrderConfirmation = () => {
  const { order_id } = useParams(); // Get the order ID from the URL
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrderDetails = async () => {
      const token = localStorage.getItem('authToken');
      try {
        const response = await fetch(`http://localhost:5001/orders/${order_id}`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch order details');
        }
        const data = await response.json();
        setOrder(data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchOrderDetails();
  }, [order_id]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="error">Error: {error}</p>;

  return (
    <div className="order-confirmation">
      <h2>Order Confirmation</h2>
      {order ? (
        <div className="order-details">
          <h3>Order ID: {order.id}</h3>
          <p>Order Date: {new Date(order.order_date).toLocaleString()}</p>
          <p>Total Amount: ${order.total_amount.toFixed(2)}</p>
          <Link to="/" className="back-to-home">Back to Home</Link>
        </div>
      ) : (
        <p>Order not found</p>
      )}
    </div>
  );
};

export default OrderConfirmation;
