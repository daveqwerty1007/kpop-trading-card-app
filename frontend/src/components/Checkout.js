import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Checkout.css';

const Checkout = () => {
  const [cartItems, setCartItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);
  const [paymentMethod, setPaymentMethod] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

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
        setCartItems(data.cart_items.map(item => ({
          ...item,
          name: item.card_name,
          price: item.price,
        })));
      } catch (error) {
        setError(error.message);
      }
    };

    fetchCartData();
  }, []);

  const handleCheckout = async () => {
    const token = localStorage.getItem('authToken');
    try {
      const response = await fetch('http://localhost:5001/orders/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ payment_method: paymentMethod }),
      });
      if (!response.ok) {
        throw new Error('Checkout failed');
      }
      const data = await response.json();
      navigate(`/order-confirmation/${data.order_id}`);
    } catch (error) {
      setError(error.message);
    }
  };

  if (error) return <p className="error">Error: {error}</p>;

  return (
    <div className="checkout">
      <h2>Checkout</h2>
      <div className="order-summary">
        <h3>Order Summary</h3>
        <ul>
          {cartItems.map(item => (
            <li key={item.id}>
              {item.name} x {item.quantity} = ${(item.price * item.quantity).toFixed(2)}
            </li>
          ))}
        </ul>
        <h3>Total: ${totalAmount.toFixed(2)}</h3>
      </div>
      <div className="payment-method">
        <h3>Payment Method</h3>
        <select value={paymentMethod} onChange={(e) => setPaymentMethod(e.target.value)}>
          <option value="">Select a payment method</option>
          <option value="credit_card">Credit Card</option>
          <option value="paypal">PayPal</option>
          <option value="bank_transfer">Bank Transfer</option>
        </select>
      </div>
      <button className="checkout-button" onClick={handleCheckout}>Complete Purchase</button>
    </div>
  );
};

export default Checkout;
