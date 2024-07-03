import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CardDetail({ match }) {
  const [card, setCard] = useState({});

  useEffect(() => {
    // Fetch card data from the backend
    axios.get(`/cards/${match.params.id}`).then(response => {
      setCard(response.data);
    });
  }, [match.params.id]);

  const addToCart = () => {
    axios.post(`/orders/add_to_cart/${card.id}`).then(response => {
      alert('Card added to cart!');
    });
  };

  return (
    <div>
      <h1>{card.card_name}</h1>
      <p>{card.artist}</p>
      <p>{card.group}</p>
      <p>{card.album}</p>
      <p>{card.description}</p>
      <p>{card.price}</p>
      <img src={card.image_url} alt={card.card_name} />
      <button onClick={addToCart}>Add to Cart</button>
    </div>
  );
}

export default CardDetail;
