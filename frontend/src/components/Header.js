import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './Header.css';

const Header = () => {
  const { isLoggedIn, user, logout } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    logout();
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <header className="header">
      <div className="header-logo">JssCards.co</div>
      <div className="header-right">
        <form onSubmit={handleSearch} className="header-search">
          <input
            type="text"
            placeholder="Search..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </form>
        <div className="header-icons">
          {isLoggedIn ? (
            <>
              <Link to="/account" className="header-button">{user.name}</Link>
              <button onClick={handleLogout} className="header-button">Logout</button>
            </>
          ) : (
            <Link to="/login" className="header-button">Login</Link>
          )}
          <Link to="/cart" className="header-button">Cart</Link>
        </div>
      </div>
    </header>
  );
};

export default Header;
