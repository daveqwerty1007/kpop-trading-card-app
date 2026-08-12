import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import api from '../services/api';
import './UserPanel.css';

const UserPanel = () => {
  const [activeTab, setActiveTab] = useState('account');
  const navigate = useNavigate();
  const { logout } = useAuth();
  const renderContent = () => {
    switch (activeTab) {
      case 'account':
        return <Account />;
      case 'orders':
        return <Orders />;
      case 'settings':
        return <Settings />;
      default:
        return <Account />;
    }
  };

const handleLogout = async () => {
  try {
    await api.post('/users/logout');
  } catch (error) {
    console.error('Error during logout:', error);
  }
  logout();
  navigate('/');
};

  return (
    <div className="user-panel">
      <div className="sidebar">
        <div className="profile">
          <h2>User Panel</h2>
          <p>Welcome, User!</p>
        </div>
        <nav>
          <ul>
            <li className={activeTab === 'account' ? 'active' : ''} onClick={() => setActiveTab('account')}>Account Details</li>
            <li className={activeTab === 'orders' ? 'active' : ''} onClick={() => setActiveTab('orders')}>Orders</li>
            <li className={activeTab === 'settings' ? 'active' : ''} onClick={() => setActiveTab('settings')}>Settings</li>
            <li onClick={handleLogout}>Logout</li>
          </ul>
        </nav>
      </div>
      <div className="main-content">
        {renderContent()}
      </div>
    </div>
  );
};

const Account = () => {
  const [accountDetails, setAccountDetails] = useState({});
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    api.get('/users/current')
      .then(response => setAccountDetails(response.data))
      .catch(error => console.error('Error fetching account details:', error));
  }, []);

  const handleChange = (e) => {
    setAccountDetails({
      ...accountDetails,
      [e.target.name]: e.target.value,
    });
  };

  const handleSave = () => {
    api.post('/users/update_user', accountDetails)
      .then(response => {
        setAccountDetails(response.data);
        setEditing(false);
      })
      .catch(error => console.error('Error updating account details:', error));
  };

  return (
    <div>
      <h1>Account Details</h1>
      {editing ? (
        <div>
          <label>
            Name:
            <input type="text" name="name" value={accountDetails.name || ''} onChange={handleChange} />
          </label>
          <label>
            Email:
            <input type="email" name="email" value={accountDetails.email || ''} onChange={handleChange} />
          </label>
          <button onClick={handleSave}>Save</button>
          <button onClick={() => setEditing(false)}>Cancel</button>
        </div>
      ) : (
        <div>
          <p><strong>Name:</strong> {accountDetails.name}</p>
          <p><strong>Email:</strong> {accountDetails.email}</p>
          <button onClick={() => setEditing(true)}>Edit</button>
        </div>
      )}
    </div>
  );
};

const Orders = () => {
  const [orders, setOrders] = useState([]); // Ensure orders is always an array
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api.get('/users/orders')
      .then(response => {
        if (Array.isArray(response.data)) {
          setOrders(response.data);
        } else {
          setOrders([]);
          setError('Unexpected response format');
        }
      })
      .catch(error => {
        console.error('Error fetching orders:', error);
        setError('An error occurred');
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Orders</h1>
      {orders.length === 0 ? (
        <p>No orders found.</p>
      ) : (
        <ul>
          {orders.map(order => (
            <li key={order.order_id}>
              <p><strong>Order ID:</strong> {order.order_id}</p>
              <p><strong>Date:</strong> {new Date(order.order_date).toLocaleDateString()}</p>
              <p><strong>Total:</strong> ${order.total_amount.toFixed(2)}</p>
              <ul>
                {order.items.map(item => (
                  <li key={item.item_id}>
                    {item.quantity}x {item.card_name} by {item.artist}
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

const Settings = () => {
  const [settings, setSettings] = useState({
    emailMarketing: false,
  });

  useEffect(() => {
    api.get('/users/settings')
      .then(response => setSettings(response.data))
      .catch(error => console.error('Error fetching settings:', error));
  }, []);

  const handleChange = (e) => {
    setSettings({
      ...settings,
      [e.target.name]: e.target.checked,
    });
  };

  const handleSave = () => {
    api.put('/users/settings', settings)
      .then(response => setSettings(response.data))
      .catch(error => console.error('Error saving settings:', error));
  };

  return (
    <div>
      <h1>Settings</h1>
      <label>
        <input
          type="checkbox"
          name="emailMarketing"
          checked={settings.emailMarketing}
          onChange={handleChange}
        />
        Subscribe to email marketing
      </label>
      <button onClick={handleSave}>Save</button>
    </div>
  );
};

export default UserPanel;
