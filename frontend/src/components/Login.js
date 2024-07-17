import React, { useState } from 'react';
import './Login.css';

const Login = () => {
  const [activeTab, setActiveTab] = useState('login');

  const renderForm = () => {
    switch (activeTab) {
      case 'login':
        return (
          <form className="login-form">
            <h2>User Login</h2>
            <input type="email" placeholder="Email" required />
            <input type="password" placeholder="Password" required />
            <button type="submit">Login</button>
          </form>
        );
      case 'signup':
        return (
          <form className="login-form">
            <h2>Sign Up</h2>
            <input type="text" placeholder="Name" required />
            <input type="email" placeholder="Email" required />
            <input type="password" placeholder="Password" required />
            <button type="submit">Sign Up</button>
          </form>
        );
      case 'admin':
        return (
          <form className="login-form">
            <h2>Admin Login</h2>
            <input type="email" placeholder="Admin Email" required />
            <input type="password" placeholder="Admin Password" required />
            <button type="submit">Login</button>
          </form>
        );
      default:
        return null;
    }
  };

  return (
    <div className="login-panel">
      <div className="tabs">
        <button className={activeTab === 'login' ? 'active' : ''} onClick={() => setActiveTab('login')}>Login</button>
        <button className={activeTab === 'signup' ? 'active' : ''} onClick={() => setActiveTab('signup')}>Sign Up</button>
        <button className={activeTab === 'admin' ? 'active' : ''} onClick={() => setActiveTab('admin')}>Admin Login</button>
      </div>
      <div className="form-container">
        {renderForm()}
      </div>
    </div>
  );
};

export default Login;
