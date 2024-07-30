import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
 
  useEffect(() => {
    fetch('/api/status')
      .then(response => response.json())
      .then(data => {
        if (data.status === 'authenticated') {
          setIsLoggedIn(true);
          setUser(data.user);
        }
      });
  }, []);

  const login = (username, password) => {
    return fetch('/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, password })
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          setIsLoggedIn(true);
          setUser(username);
        }
        return data;
      });
  };

  const logout = () => {
    return fetch('/api/logout', {
      method: 'POST'
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          setIsLoggedIn(false);
          setUser(null);
        }
        return data;
      });
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
