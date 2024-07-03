import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserProfile() {
  const [user, setUser] = useState({});

  useEffect(() => {
    // Fetch user data from the backend
    axios.get('/users/profile').then(response => {
      setUser(response.data);
    });
  }, []);

  return (
    <div>
      <h1>User Profile</h1>
      <form>
        <label>Name:</label>
        <input type="text" value={user.name} readOnly />
        <label>Email:</label>
        <input type="email" value={user.email} readOnly />
        <label>Address:</label>
        <input type="text" value={user.address} readOnly />
        <label>Phone Number:</label>
        <input type="text" value={user.phone_number} readOnly />
      </form>
    </div>
  );
}

export default UserProfile;
