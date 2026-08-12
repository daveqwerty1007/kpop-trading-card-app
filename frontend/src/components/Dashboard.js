import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import api from '../services/api';
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
      const response = await api.get('/admin/dashboard');
      setStats(response.data);
      setSalesData(response.data.sales_data_last_week);
    } catch (error) {
      setError('Failed to fetch dashboard stats');
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
      <CollapsibleList title="Fraudulent Orders" items={stats.fraudulent_orders} />
      <CollapsibleList title="Top Spending Users" items={stats.top_spending_users} />
      <CollapsibleList title="Old Inventory" items={stats.old_inventory} />
      <CollapsibleList title="Restock List" items={stats.restock_list} />
    </div>
  );
};

const COLLAPSED_VISIBLE_COUNT = 3;

const CollapsibleList = ({ title, items = [] }) => {
  const [collapsed, setCollapsed] = useState(true);

  const toggleCollapse = () => setCollapsed(!collapsed);

  const visibleItems = collapsed ? items.slice(0, COLLAPSED_VISIBLE_COUNT) : items;

  return (
    <div className="section">
      <h2>{title}</h2>
      <ul>
        {visibleItems.map((item, index) => (
          <li key={index}>
            {item.order_id && (
              <>
                <strong>Order ID:</strong> {item.order_id}<br />
                <strong>Customer:</strong> {item.customer_name} ({item.customer_email})<br />
                <strong>Status:</strong> {item.payment_status}
              </>
            )}
            {item.id && item.total_spent && (
              <>
                <strong>User:</strong> {item.name} ({item.email})<br />
                <strong>Total Spent:</strong> ${item.total_spent.toFixed(2)}
              </>
            )}
            {item.card_name && (
              <>
                <strong>Card:</strong> {item.card_name}<br />
                <strong>Artist:</strong> {item.artist}<br />
                <strong>Album:</strong> {item.album}<br />
                <strong>Quantity Available:</strong> {item.quantity_available}
              </>
            )}
          </li>
        ))}
      </ul>
      {items.length > COLLAPSED_VISIBLE_COUNT && (
        <button onClick={toggleCollapse}>
          {collapsed ? 'Show More' : 'Show Less'}
        </button>
      )}
    </div>
  );
};

export default Dashboard;
