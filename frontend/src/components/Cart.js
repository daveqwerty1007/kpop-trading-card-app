import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import './Cart.css';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Initialize useNavigate

  useEffect(() => {
    const fetchCartData = async () => {
      const token = localStorage.getItem('authToken');
      try {
        const response = await fetch('http://localhost:5001/orders/cart', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error('Failed to fetch cart data');
        }
        const data = await response.json();
        setTotalAmount(data.total_amount || 0);

        const detailedItems = await Promise.all(data.cart_items.map(async (item) => {
          const response = await fetch(`http://localhost:5001/cards/${item.card_id}`, {
            headers: {
              'Authorization': `Bearer ${token}`,
            },
          });
          if (!response.ok) {
            throw new Error('Failed to fetch item details');
          }
          const cardData = await response.json();
          return {
            ...item,
            name: cardData.card_name,
            price: cardData.price,
          };
        }));
        setCartItems(detailedItems);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCartData();
  }, []);

  const handleQuantityChange = async (cartItemId, newQuantity) => {
    const token = localStorage.getItem('authToken');
    if (newQuantity < 1) return;  // Prevent setting a quantity less than 1

    try {
      const response = await fetch(`http://localhost:5001/cart_items/${cartItemId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ quantity: newQuantity }),
      });
      if (!response.ok) {
        throw new Error('Failed to update cart item');
      }
      const updatedCartItem = await response.json();
      setCartItems(prevItems =>
        prevItems.map(item => item.id === cartItemId ? { ...item, quantity: newQuantity } : item)
      );
      setTotalAmount(prevTotal => prevTotal + (updatedCartItem.price * (newQuantity - updatedCartItem.quantity)));
    } catch (error) {
      setError(error.message);
    }
  };

  const handleRemoveItem = async (cartItemId) => {
    const token = localStorage.getItem('authToken');
    try {
      const response = await fetch(`http://localhost:5001/cart_items/${cartItemId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to remove cart item');
      }
      const removedItem = cartItems.find(item => item.id === cartItemId);
      setCartItems(prevItems => prevItems.filter(item => item.id !== cartItemId));
      setTotalAmount(prevTotal => prevTotal - (removedItem.price * removedItem.quantity));
    } catch (error) {
      setError(error.message);
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
