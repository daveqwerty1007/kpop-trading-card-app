import React, { createContext, useState, useEffect, useCallback, useContext } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  const refreshUser = useCallback(() => {
    if (!localStorage.getItem('authToken')) {
      setIsLoggedIn(false);
      setUser(null);
      return;
    }
    api.get('/users/current')
      .then(response => {
        setIsLoggedIn(true);
        setUser(response.data);
      })
      .catch(() => {
        setIsLoggedIn(false);
        setUser(null);
      });
  }, []);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  const login = async (email, password) => {
    try {
      const response = await api.post('/users/login', { email, password });
      localStorage.setItem('authToken', response.data.access_token);
      refreshUser();
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setIsLoggedIn(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, user, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
