import React, { createContext, useState, useEffect, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);
 
  useEffect(() => {
    const token = localStorage.getItem('authToken');
    if (token) {
      fetch('/api/status', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'authenticated') {
            setIsLoggedIn(true);
            setUser(data.user);
          } else {
            setIsLoggedIn(false);
            setUser(null);
          }
        })
        .catch(() => {
          setIsLoggedIn(false);
          setUser(null);
        });
    }
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
          localStorage.setItem('authToken', data.token);
          setIsLoggedIn(true);
          setUser(data.user);
        } else {
          throw new Error('Login failed');
        }
        return data;
      });
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    return fetch('/api/logout', {
      method: 'POST',
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
