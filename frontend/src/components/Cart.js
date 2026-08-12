import React, { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import api from '../services/api';
import './Cart.css';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    const fetchCartData = async () => {
      try {
        const response = await api.get('/orders/cart');
        setCartItems(response.data.cart_items.map(item => ({ ...item, name: item.card_name })));
      } catch (error) {
        setError('Failed to fetch cart data');
      } finally {
        setLoading(false);
      }
    };

    fetchCartData();
  }, []);

  const totalAmount = useMemo(
    () => cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0),
    [cartItems]
  );

  const handleQuantityChange = async (cartItemId, newQuantity) => {
    if (newQuantity < 1) return;  // Prevent setting a quantity less than 1

    try {
      await api.put(`/cart_items/${cartItemId}`, { quantity: newQuantity });
      setCartItems(prevItems =>
        prevItems.map(item => item.id === cartItemId ? { ...item, quantity: newQuantity } : item)
      );
    } catch (error) {
      setError('Failed to update cart item');
    }
  };

  const handleRemoveItem = async (cartItemId) => {
    try {
      await api.delete(`/cart_items/${cartItemId}`);
      setCartItems(prevItems => prevItems.filter(item => item.id !== cartItemId));
    } catch (error) {
      setError('Failed to remove cart item');
    }
  };

  const handleCheckout = () => {
    navigate('/checkout');
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="cart">
      <h2>Shopping Cart</h2>
      <ul className="cart-items">
        {cartItems.map(item => (
          <li key={item.id} className="cart-item">
            <div className="item-details">
              <span>{item.name}</span>
              <span>Quantity: </span>
              <div className="quantity-controls">
                <button onClick={() => handleQuantityChange(item.id, item.quantity - 1)}>-</button>
                <input type="text" value={item.quantity} readOnly />
                <button onClick={() => handleQuantityChange(item.id, item.quantity + 1)}>+</button>
              </div>
              <span>Price: ${item.price}</span>
            </div>
            <button className="remove-item" onClick={() => handleRemoveItem(item.id)}>Remove</button>
          </li>
        ))}
      </ul>
      <div className="cart-total">
        <h3>Total Price: ${totalAmount.toFixed(2)}</h3>
      </div>
      <button className="checkout-button" onClick={handleCheckout}>Proceed to Checkout</button>
    </div>
  );
};

export default Cart;
