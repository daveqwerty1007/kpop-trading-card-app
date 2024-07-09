// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://172.17.0.2:5000/api', // Update this to match your backend URL
});

// Add a request interceptor to include the token in headers
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
