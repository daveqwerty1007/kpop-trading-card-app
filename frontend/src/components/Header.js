import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
  return (
    <header className="header">
      <div className="header-logo">JssCards.co</div>
      <div className="header-right">
        <div className="header-search">
          <input type="text" placeholder="Search..." />
        </div>
        <div className="header-icons">
          <Link to="/login" className="header-button">Login</Link>
          <Link to="/cart" className="header-button">Cart</Link>
        </div>
      </div>
    </header>
  );
};

export default Header;