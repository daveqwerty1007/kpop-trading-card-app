import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import './CardDetail.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

function CardDetail() {
  const { id } = useParams();
  const [card, setCard] = useState(null);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);

  useEffect(() => {
    fetch(`/api/cards/${id}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => setCard(data))
      .catch(error => {
        console.error('Error fetching card:', error);
        setError('Error fetching card. Please try again later.');
      });
  }, [id]);

  const handleAddToCart = () => {
    // Logic to add the item to the cart
    console.log(`Added ${quantity} of ${card.card_name} to the cart.`);
  };

  const handleQuantityChange = (change) => {
    setQuantity(prevQuantity => Math.max(1, prevQuantity + change));
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
          {card.relatedCards.map((relatedCard, index) => (
            <div className="related-card-item" key={index}>
              <img src={relatedCard.image_url} alt={relatedCard.name} />
              <p>{relatedCard.name}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CardDetail;
