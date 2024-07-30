import React, { useState, useEffect } from 'react';
import './AdminPanel.css';
import Dashboard from './Dashboard';
import Orders from './Orders';
import Products from './Products';
import Users from './Users';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [adminName, setAdminName] = useState('Admin');

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      fetch('http://localhost:5001/admin/profile', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
        .then(response => response.json())
        .then(data => setAdminName(data.name || 'Admin'))
        .catch(error => console.error('Error fetching admin profile:', error));
    }
  }, []);

  const handleLogout = async () => {
    localStorage.removeItem('authToken'); // Remove token from local storage
    window.location.href = '/'; // Redirect to homepage
  };

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'orders':
        return <Orders />;
      case 'products':
        return <Products />;
      case 'users':
        return <Users />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="admin-panel">
      <div className="sidebar">
        <div className="profile">
          <h2>Admin Panel</h2>
          <p>Welcome, {adminName}!</p>
        </div>
        <nav>
          <ul>
            <li className={activeTab === 'dashboard' ? 'active' : ''} onClick={() => setActiveTab('dashboard')}>Dashboard</li>
            <li className={activeTab === 'orders' ? 'active' : ''} onClick={() => setActiveTab('orders')}>Orders</li>
            <li className={activeTab === 'products' ? 'active' : ''} onClick={() => setActiveTab('products')}>Products</li>
            <li className={activeTab === 'users' ? 'active' : ''} onClick={() => setActiveTab('users')}>Users</li>
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

export default AdminPanel;
