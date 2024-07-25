import React, { useState } from 'react';
import './AdminPanel.css';
import Dashboard from './Dashboard';
import Orders from './Orders';
import Products from './Products';
import Users from './Users';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const handleLogout = async () => {
    try {
      const response = await fetch('http://localhost:5001/admin/logout', {
        method: 'POST', // Assuming POST request for logout
        credentials: 'include', // Include cookies if your authentication relies on them
        headers: {
          'Content-Type': 'application/json',
        },
      });
      if (response.ok) {
        window.location.href = '/'; // Redirect to homepage
      } else {
        // Handle logout error (optional)
        console.error('Logout failed');
      }
    } catch (error) {
      console.error('An error occurred during logout', error);
    }
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
          <p>Welcome, Admin!</p>
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
