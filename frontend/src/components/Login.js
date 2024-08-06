import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Login.css';

const Login = () => {
  const [activeTab, setActiveTab] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState(''); // For registration
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const storeToken = (token) => {
    localStorage.setItem('authToken', token);
  };

  const handleUserLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:5001/users/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include'
      });

      const data = await response.json();
      console.log('User Login response:', data);

      if (response.ok) {
        storeToken(data.access_token);
        navigate('/user_panel'); 
      } else {
        setError(data.message || 'Unknown error occurred');
      }
    } catch (err) {
      console.error('User Login error:', err);
      setError('An error occurred. Please try again.');
    }
  };

  const handleAdminLoginSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:5001/admin/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
        credentials: 'include'
      });

      const data = await response.json();
      console.log('Admin Login response:', data);

      if (response.ok) {
        storeToken(data.access_token);
        navigate('/admin_panel'); // Adjust this path as necessary
      } else {
        setError(data.message || 'Unknown error occurred');
      }
    } catch (err) {
      console.error('Admin Login error:', err);
      setError('An error occurred. Please try again.');
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
        const response = await fetch('http://localhost:5001/users/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, email, password }),
            credentials: 'include'
        });

        const data = await response.json();
        console.log('Registration response:', data);
        storeToken(data.access_token);
        if (response.ok) {
            // Navigate to user panel or login
            navigate('/user_panel'); // Adjust this path as necessary
        } else {
            setError(data.errors ? data.errors.map(err => err.msg).join(', ') : 'Unknown error occurred');
        }
    } catch (err) {
        console.error('Registration error:', err);
        setError('An error occurred. Please try again.');
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
