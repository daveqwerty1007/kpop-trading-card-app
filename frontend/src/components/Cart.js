import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function Cart() {
  const [cartItems, setCartItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);

  useEffect(() => {
    // Fetch cart items from the backend
    axios.get('/orders/cart').then(response => {
      setCartItems(response.data.cart_items);
      setTotalAmount(response.data.total_amount);
    });
  }, []);

  const removeFromCart = (item_id) => {
    axios.post(`/orders/remove_from_cart/${item_id}`).then(response => {
      setCartItems(cartItems.filter(item => item.id !== item_id));
      setTotalAmount(totalAmount - response.data.item_price * response.data.item_quantity);
    });
  };

  return (
    <div>
      <h1>Shopping Cart</h1>
      <ul>
        {cartItems.map(item => (
          <li key={item.id}>
            {item.card.card_name} - ${item.card.price} x {item.quantity}
            <button onClick={() => removeFromCart(item.id)}>Remove</button>
          </li>
        ))}
      </ul>
      <p>Total: ${totalAmount}</p>
      <Link to="/checkout">Proceed to Checkout</Link>
    </div>
  );
}

export default Cart;
