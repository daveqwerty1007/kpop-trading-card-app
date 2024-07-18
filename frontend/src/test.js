// Example of making a GET request
import api from './services/api';

const fetchData = async () => {
  try {
    const response = await api.get('/endpoint');
    console.log(response.data);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

fetchData();
