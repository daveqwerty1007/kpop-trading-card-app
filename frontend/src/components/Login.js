import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import api from '../services/api';
import './Login.css';

const Login = () => {
  const [activeTab, setActiveTab] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState(''); // For registration
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { refreshUser } = useAuth();

  const storeToken = (token) => {
    localStorage.setItem('authToken', token);
  };

  const handleUserLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await api.post('/users/login', { email, password });
      storeToken(response.data.access_token);
      refreshUser();
      navigate('/user_panel');
    } catch (err) {
      console.error('User Login error:', err);
      setError(err.response?.data?.message || 'An error occurred. Please try again.');
    }
  };

  const handleAdminLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await api.post('/admin/login', { email, password });
      storeToken(response.data.access_token);
      navigate('/admin_panel'); // Adjust this path as necessary
    } catch (err) {
      console.error('Admin Login error:', err);
      setError(err.response?.data?.message || 'An error occurred. Please try again.');
    }
  };

  const handleSignupSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Ensure all required fields are provided
    if (!name || !email || !password) {
        setError('All fields are required.');
        return;
    }

    try {
        const response = await api.post('/users/register', { name, email, password });
        storeToken(response.data.access_token);
        refreshUser();
        // Navigate to user panel or login
        navigate('/user_panel'); // Adjust this path as necessary
    } catch (err) {
        console.error('Registration error:', err);
        const errors = err.response?.data?.errors;
        setError(errors ? errors.map(e => e.msg).join(', ') : 'An error occurred. Please try again.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    navigate('/login'); // Adjust the path as necessary
  };

  const renderForm = () => {
    switch (activeTab) {
      case 'login':
        return (
          <form className="login-form" onSubmit={handleUserLoginSubmit}>
            <h2>User Login</h2>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
            {error && <p className="error">{error}</p>}
          </form>
        );
      case 'signup':
        return (
          <form className="login-form" onSubmit={handleSignupSubmit}>
            <h2>Sign Up</h2>
            <input
              type="text"
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Sign Up</button>
            {error && <p className="error">{error}</p>}
          </form>
        );
      case 'admin':
        return (
          <form className="login-form" onSubmit={handleAdminLoginSubmit}>
            <h2>Admin Login</h2>
            <input
              type="email"
              placeholder="Admin Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Admin Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
            {error && <p className="error">{error}</p>}
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
