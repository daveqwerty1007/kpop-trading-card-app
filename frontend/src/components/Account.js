import React from 'react';

const Account = () => {
  return (
    <div>
      <h2>Account</h2>
      <p>Name: John Doe</p>
      <p>Email: john@example.com</p>
      <button>Edit Profile</button>
      <h3>Orders</h3>
      <ul>
        <li>Order 1</li>
        <li>Order 2</li>
      </ul>
      <button>Logout</button>
    </div>
  );
};

export default Account;