// src/utils/auth.js
import { jwtDecode } from 'jwt-decode';

export const setToken = (token) => {
  localStorage.setItem('token', token);
};

export const getToken = () => {
  return localStorage.getItem('token');
};

export const decodeToken = (token) => {
  return jwtDecode(token);
};

export const removeToken = () => {
  localStorage.removeItem('token');
};
