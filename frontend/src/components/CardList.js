import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function CardList() {
  const [cards, setCards] = useState([]);

  useEffect(() => {
    // Fetch card data from the backend
    axios.get('/cards').then(response => {
      setCards(response.data);
    });
  }, []);

  return (
    <div>
      <h1>Card List</h1>
      <ul>
        {cards.map(card => (
          <li key={card.id}>
            <Link to={`/card/${card.id}`}>{card.card_name}</Link>
            <p>{card.artist}</p>
            <p>{card.group}</p>
            <p>{card.price}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CardList;
