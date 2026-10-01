import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import api from '../services/api';
import './CardDetail.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

function CardDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [card, setCard] = useState(null);
  const [relatedCards, setRelatedCards] = useState([]);
  const [error, setError] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [cartStatus, setCartStatus] = useState(null); // 'added' | 'login' | error message

  useEffect(() => {
    setCartStatus(null);

    const fetchRelatedCards = (artistFirstName) => {
      api.get(`/cards/search?q=${encodeURIComponent(artistFirstName)}`)
        .then(response => {
          setRelatedCards(response.data.filter(relatedCard => relatedCard.id !== parseInt(id)));
        })
        .catch(error => {
          console.error('Error fetching related cards:', error);
        });
    };

    api.get(`/cards/${id}`)
      .then(response => {
        setCard(response.data);
        fetchRelatedCards(response.data.artist.split(' ')[0]);
      })
      .catch(error => {
        console.error('Error fetching card:', error);
        setError('Error fetching card. Please try again later.');
      });
  }, [id]);

  const handleAddToCart = () => {
    api.post('/cart_items/', {
      card_id: card.id,
      quantity: quantity
    })
    .then(() => setCartStatus('added'))
    .catch(error => {
      const status = error.response?.status;
      // 401/422: no token, or one the server rejected
      setCartStatus(status === 401 || status === 422
        ? 'login'
        : error.response?.data?.message || 'Could not add this card to your cart.');
    });
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
          {cartStatus === 'added' && (
            <p className="cart-message">Added to your cart. <Link to="/cart">View cart</Link></p>
          )}
          {cartStatus === 'login' && (
            <p className="cart-message">Please <Link to="/login">log in</Link> to add cards to your cart.</p>
          )}
          {cartStatus && cartStatus !== 'added' && cartStatus !== 'login' && (
            <p className="cart-message error">{cartStatus}</p>
          )}
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
