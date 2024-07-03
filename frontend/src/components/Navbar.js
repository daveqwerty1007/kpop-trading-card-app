import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <header>
      <nav>
        <Link to="/">Home</Link>
        <Link to="/dashboard">Profile</Link>
        <Link to="/card">Cards</Link>
        <Link to="/cart">Cart</Link>
        <Link to="/admin">Admin</Link>
      </nav>
    </header>
  );
}

export default Navbar;
