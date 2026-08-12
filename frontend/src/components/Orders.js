import React, { useEffect, useState } from 'react';
import api from '../services/api';
import './Orders.css';

const Orders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchOrders();
  }, []);

  const fetchOrders = async () => {
    try {
      const response = await api.get('/orders/list');
      setOrders(response.data);
    } catch (error) {
      setError('Failed to fetch orders');
    } finally {
      setLoading(false);
    }
  };

  const deleteOrder = async (orderId) => {
    try {
      await api.delete(`/orders/${orderId}`);
      // Refresh orders list after successful deletion
      setOrders(orders.filter(order => order.id !== orderId));
    } catch (error) {
      setError('Failed to delete order');
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="orders">
      <h1>Orders</h1>
      <table>
        <thead>
          <tr>
            <th>Order ID</th>
            <th>User</th>
            <th>Total Amount</th>
            <th>Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(order => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.user_id}</td>
              <td>${order.total_amount.toFixed(2)}</td>
              <td>{new Date(order.order_date).toLocaleDateString()}</td>
              <td>{order.status}</td>
              <td>
                <button onClick={() => deleteOrder(order.id)}>Delete</button>
                {/* Add more actions like edit or view details if needed */}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Orders;
