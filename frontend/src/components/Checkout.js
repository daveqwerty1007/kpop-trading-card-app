import React from 'react';
import { useHistory } from 'react-router-dom';
import axios from 'axios';

function Checkout() {
  const history = useHistory();

  const handleSubmit = (event) => {
    event.preventDefault();
    const paymentMethod = event.target.payment_method.value;

    axios.post('/orders/checkout', { payment_method: paymentMethod }).then(response => {
      alert('Checkout successful!');
      history.push('/');
    });
  };

  return (
    <div>
      <h1>Checkout</h1>
      <form onSubmit={handleSubmit}>
        <label for="payment_method">Payment Method:</label>
        <select id="payment_method" name="payment_method" required>
          <option value="credit_card">Credit Card</option>
          <option value="paypal">PayPal</option>
        </select>
        <br />
        <button type="submit">Complete Purchase</button>
      </form>
    </div>
  );
}

export default Checkout;
