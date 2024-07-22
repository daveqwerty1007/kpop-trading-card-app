import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './Header.css';

const Header = () => {
  const { isLoggedIn, user, logout } = useAuth();

  return (
    <header className="header">
      <div className="header-logo">JssCards.co</div>
      <div className="header-right">
        <div className="header-search">
          <input type="text" placeholder="Search..." />
        </div>
        <div className="header-icons">
          {isLoggedIn ? (
            <>
              <Link to="/account" className="header-button">Account</Link>
              <button onClick={logout} className="header-button">Logout</button>
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
