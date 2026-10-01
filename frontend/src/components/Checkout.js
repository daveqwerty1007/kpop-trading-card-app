import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import './Checkout.css';

const Checkout = () => {
  const [cartItems, setCartItems] = useState([]);
  const [totalAmount, setTotalAmount] = useState(0);
  const [paymentMethod, setPaymentMethod] = useState('');
  const [error, setError] = useState(null);
  const [checkoutError, setCheckoutError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchCartData = async () => {
      try {
        const response = await api.get('/orders/cart');
        setTotalAmount(response.data.total_amount || 0);
        setCartItems(response.data.cart_items.map(item => ({
          ...item,
          name: item.card_name,
          price: item.price,
        })));
      } catch (error) {
        setError('Failed to fetch cart data');
      }
    };

    fetchCartData();
  }, []);

  const handleCheckout = async () => {
    setCheckoutError(null);
    setSubmitting(true);
    try {
      const response = await api.post('/orders/checkout', { payment_method: paymentMethod });
      navigate(`/order-confirmation/${response.data.order_id}`);
    } catch (error) {
      // Shown inline so the customer can fix it (e.g. out of stock) and retry.
      setCheckoutError(error.response?.data?.message || 'Checkout failed');
      setSubmitting(false);
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
      <button
        className="checkout-button"
        onClick={handleCheckout}
        disabled={!paymentMethod || cartItems.length === 0 || submitting}
      >
        Complete Purchase
      </button>
      {checkoutError && <p className="error">{checkoutError}</p>}
    </div>
  );
};

export default Checkout;
