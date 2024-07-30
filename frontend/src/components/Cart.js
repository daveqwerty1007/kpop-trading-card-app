import React, { useEffect, useState } from 'react';
import './Cart.css';

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);

  useEffect(() => {
    fetch('http://localhost:5001/orders/cart')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data) {
          setTotalAmount(data.total_amount || 0);
          // Fetch details for each cart item
          const fetchItemDetails = data.cart_items.map(item =>
            fetch(`http://localhost:5001/cards/${item.card_id}`)
              .then(response => response.json())
              .then(cardData => ({
                ...item,
                name: cardData.card_name,
                price: cardData.price,
              }))
          );
          return Promise.all(fetchItemDetails);
        }
      })
      .then(detailedItems => {
        setCartItems(detailedItems || []);
      })
      .catch(error => console.error('Error fetching cart data:', error));
  }, []);

  return (
    <div className="cart">
      <h2>Shopping Cart</h2>
      <ul className="cart-items">
        {cartItems.map(item => (
          <li key={item.id} className="cart-item">
            <div className="item-details">
              <span>{item.name}</span>
              <span>Quantity: {item.quantity}</span>
              <span>Price: ${item.price}</span>
            </div>
          </li>
        ))}
      </ul>
      <div className="cart-total">
        <h3>Total Price: ${totalAmount}</h3>
      </div>
    </div>
  );
};

export default Cart;
