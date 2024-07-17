import React from 'react';
import './Cart.css';

const Cart = () => {
  // Example cart items
  const cartItems = [
    { id: 1, name: 'Item 1', quantity: 2, price: 10 },
    { id: 2, name: 'Item 2', quantity: 1, price: 20 },
    { id: 3, name: 'Item 3', quantity: 3, price: 15 },
  ];

  const getTotalPrice = () => {
    return cartItems.reduce((total, item) => total + item.price * item.quantity, 0);
  };

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
        <h3>Total Price: ${getTotalPrice()}</h3>
      </div>
    </div>
  );
};

export default Cart;