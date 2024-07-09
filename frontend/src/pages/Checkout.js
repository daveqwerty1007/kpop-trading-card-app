// src/pages/Checkout.js
import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Container, TextField, Button, Typography } from '@mui/material';
import api from '../services/api';
import { clearCart } from '../redux/slices/cartSlice';

const Checkout = ({ history }) => {
  const dispatch = useDispatch();
  const cartItems = useSelector((state) => state.cart.items);
  const [shippingInfo, setShippingInfo] = useState({
    name: '',
    address: '',
    city: '',
    zip: '',
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setShippingInfo((prevState) => ({ ...prevState, [name]: value }));
  };

  const handleCheckout = async (e) => {
    e.preventDefault();
    try {
      await api.post('/checkout', { cartItems, shippingInfo });
      dispatch(clearCart());
      history.push('/');
    } catch (error) {
      console.error('Checkout failed', error);
    }
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Checkout
      </Typography>
      <form onSubmit={handleCheckout}>
        <TextField
          label="Name"
          name="name"
          value={shippingInfo.name}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Address"
          name="address"
          value={shippingInfo.address}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="City"
          name="city"
          value={shippingInfo.city}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="Zip Code"
          name="zip"
          value={shippingInfo.zip}
          onChange={handleInputChange}
          fullWidth
          margin="normal"
        />
        <Button type="submit" variant="contained" color="primary" fullWidth>
          Place Order
        </Button>
      </form>
    </Container>
  );
};

export default Checkout;
