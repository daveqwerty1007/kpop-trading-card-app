import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import './Dashboard.css';

// Register the components
Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const Dashboard = () => {
  const [stats, setStats] = useState({});
  const [salesData, setSalesData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch('http://localhost:5001/admin/dashboard');
      if (!response.ok) {
        throw new Error('Failed to fetch dashboard stats');
      }
      const data = await response.json();
      setStats(data);
      setSalesData(data.sales_data_last_week);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const chartData = {
    labels: salesData.map(data => data.date),
    datasets: [
      {
        label: 'Sales',
        data: salesData.map(data => data.sales),
        borderColor: 'rgba(75,192,192,1)',
        backgroundColor: 'rgba(75,192,192,0.2)',
      },
    ],
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      <div className="stats">
        <div className="stat">
          <h2>Users</h2>
          <p>{stats.user_count}</p>
        </div>
        <div className="stat">
          <h2>Orders</h2>
          <p>{stats.order_count}</p>
        </div>
        <div className="stat">
          <h2>Products</h2>
          <p>{stats.product_count}</p>
        </div>
        <div className="stat">
          <h2>Total Sales</h2>
          <p>${stats.total_sales}</p>
        </div>
      </div>
      <div className="chart-container">
        <h2>Sales for the Past Week</h2>
        <Line data={chartData} />
      </div>
      <div className="additional-data">
        <div className="section">
          <h2>Fraudulent Orders</h2>
          <ul>
            {stats.fraudulent_orders && stats.fraudulent_orders.map(order => (
              <li key={order.order_id}>
                <strong>{order.customer_name}</strong> ({order.customer_email}): Order #{order.order_id} - {order.payment_status}
              </li>
            ))}
          </ul>
        </div>
        <div className="section">
          <h2>Top Spending Users</h2>
          <ul>
            {stats.top_spending_users && stats.top_spending_users.map(user => (
              <li key={user.id}>
                <strong>{user.name}</strong> ({user.email}): ${user.total_spent.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
        <div className="section">
          <h2>Old Inventory</h2>
          <ul>
            {stats.old_inventory && stats.old_inventory.map(item => (
              <li key={item.card_name}>
                <strong>{item.card_name}</strong> by {item.artist} - {item.album} ({item.quantity_available} available)
              </li>
            ))}
          </ul>
        </div>
        <div className="section">
          <h2>Restock List</h2>
          <ul>
            {stats.restock_list && stats.restock_list.map(item => (
              <li key={item.card_name}>
                <strong>{item.card_name}</strong> by {item.artist} - {item.album} (Only {item.quantity_available} left)
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
