import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5001'
});

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  response => response,
  error => {
    // The server rejected our token (401 expired, 422 invalid): we're logged
    // out, so drop it and let AuthContext update the UI.
    const status = error.response?.status;
    if ((status === 401 || status === 422) && error.config?.headers?.Authorization) {
      localStorage.removeItem('authToken');
      window.dispatchEvent(new Event('auth:logout'));
    }
    if (error.response) {
      console.error('API error:', error.response);
    } else if (error.request) {
      console.error('Network error:', error.request);
    } else {
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

export default api;
