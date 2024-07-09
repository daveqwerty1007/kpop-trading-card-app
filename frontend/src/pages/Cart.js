// src/pages/Cart.js
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Container, List, ListItem, ListItemText, Button, Typography } from '@mui/material';
import { removeItemFromCart, clearCart } from '../redux/slices/cartSlice';

const Cart = () => {
  const dispatch = useDispatch();
  const cartItems = useSelector((state) => state.cart.items);

  const handleRemoveFromCart = (id) => {
    dispatch(removeItemFromCart({ id }));
  };

  const handleClearCart = () => {
    dispatch(clearCart());
  };

  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Shopping Cart
      </Typography>
      <List>
        {cartItems.map((item) => (
          <ListItem key={item.id}>
            <ListItemText
              primary={item.title}
              secondary={`Quantity: ${item.quantity} - Price: $${item.price}`}
            />
            <Button onClick={() => handleRemoveFromCart(item.id)}>
              Remove
            </Button>
          </ListItem>
        ))}
      </List>
      {cartItems.length > 0 && (
        <div>
          <Button onClick={handleClearCart}>Clear Cart</Button>
          <Button variant="contained" color="primary">
            Proceed to Checkout
          </Button>
        </div>
      )}
    </Container>
  );
};

export default Cart;
