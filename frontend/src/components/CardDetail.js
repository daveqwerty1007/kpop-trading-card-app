import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './CardDetail.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

function CardDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [card, setCard] = useState(null);
  const [relatedCards, setRelatedCards] = useState([]);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    fetchCardData();
  }, [id]);

  const fetchCardData = () => {
    const token = localStorage.getItem('authToken');
    fetch(`http://localhost:5001/cards/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch card data');
        }
        return response.json();
      })
      .then(data => {
        setCard(data);
        fetchRelatedCards(data.artist.split(' ')[0]);
      })
      .catch(error => {
        console.error('Error fetching card:', error);
        setError('Error fetching card. Please try again later.');
      });
  };

  const fetchRelatedCards = (artistFirstName) => {
    const token = localStorage.getItem('authToken');
    fetch(`http://localhost:5001/cards/search?q=${artistFirstName}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
      .then(response => response.json())
      .then(data => {
        setRelatedCards(data.filter(relatedCard => relatedCard.id !== parseInt(id)));
      })
      .catch(error => {
        console.error('Error fetching related cards:', error);
      });
  };

  const handleAddToCart = () => {
    const token = localStorage.getItem('authToken');
    fetch('http://localhost:5001/cart_items/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        card_id: card.id,
        quantity: quantity
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Failed to add item to cart');
      }
      return response.json();
    })
    .then(data => {
      console.log(`Added ${quantity} of ${data.card_name} to the cart.`);
    })
    .catch(error => console.error('Error adding item to cart:', error));
  };

  const handleQuantityChange = (change) => {
    setQuantity(prevQuantity => Math.max(1, prevQuantity + change));
  };

  const handleRelatedCardClick = (relatedCardId) => {
    navigate(`/card/${relatedCardId}`);
  };

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (!card) {
    return <div>Loading...</div>;
  }

  return (
    <div className="card-detail-page">
      <div className="card-detail-container">
        <div className="card-image">
          <img src={card.image_url} alt={card.card_name} />
        </div>
        <div className="card-info">
          <h2>{card.card_name}</h2>
          <p><strong>Artist:</strong> {card.artist}</p>
          <p><strong>Group:</strong> {card.group}</p>
          <p><strong>Album:</strong> {card.album}</p>
          <p><strong>Description:</strong> {card.description}</p>
          <p><strong>Price:</strong> ${card.price}</p>
          <div className="quantity-selector">
            <label htmlFor="quantity">Qty:</label>
            <button onClick={() => handleQuantityChange(-1)}>-</button>
            <input
              type="text"
              id="quantity"
              value={quantity}
              readOnly
            />
            <button onClick={() => handleQuantityChange(1)}>+</button>
          </div>
          <button className="add-to-cart" onClick={handleAddToCart}>
            <i className="fas fa-cart-plus"></i> Add to Cart
          </button>
        </div>
      </div>
      <div className="related-cards">
        <h3>Also from {card.artist}</h3>
        <div className="related-cards-list">
          {relatedCards.map((relatedCard) => (
            <div
              className="related-card-item"
              key={relatedCard.id}
              onClick={() => handleRelatedCardClick(relatedCard.id)}
              style={{ cursor: 'pointer' }}
            >
              <img src={relatedCard.image_url} alt={relatedCard.card_name} />
              <p>{relatedCard.card_name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CardDetail;
