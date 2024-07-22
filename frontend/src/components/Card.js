import React, { useState, useEffect } from 'react';
import './Card.css';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { Link } from 'react-router-dom';

function Card() {
  const [artistCollapsed, setArtistCollapsed] = useState(false);
  const [groupCollapsed, setGroupCollapsed] = useState(false);
  const [albumCollapsed, setAlbumCollapsed] = useState(false);
  const [priceCollapsed, setPriceCollapsed] = useState(false);
  const [cards, setCards] = useState([]);
  const [artists, setArtists] = useState([]);
  const [groups, setGroups] = useState([]);
  const [albums, setAlbums] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch cards from the backend
    fetch('/api/cards')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setCards(data);
        // Extract unique artists, groups, and albums from the fetched cards
        const uniqueArtists = [...new Set(data.map(card => card.artist))];
        const uniqueGroups = [...new Set(data.map(card => card.group))];
        const uniqueAlbums = [...new Set(data.map(card => card.album))];
        setArtists(uniqueArtists);
        setGroups(uniqueGroups);
        setAlbums(uniqueAlbums);
      })
      .catch(error => {
        console.error('Error fetching cards:', error);
        setError('Error fetching cards. Please try again later.');
      });
  }, []);

  return (
    <div className="card-page">
      <div className="filter">
        <h3 onClick={() => setArtistCollapsed(!artistCollapsed)}>
          Artist
          <i className={`fas ${artistCollapsed ? 'fa-chevron-right' : 'fa-chevron-down'}`} style={{ marginLeft: '10px' }}></i>
        </h3>
        {!artistCollapsed && (
          <div className="filter-section">
            {artists.map((artist, index) => (
              <label key={index}>
                <input type="checkbox" name={`artist${index}`} /> {artist}
              </label>
            ))}
          </div>
        )}

        <h3 onClick={() => setGroupCollapsed(!groupCollapsed)}>
          Group
          <i className={`fas ${groupCollapsed ? 'fa-chevron-right' : 'fa-chevron-down'}`} style={{ marginLeft: '10px' }}></i>
        </h3>
        {!groupCollapsed && (
          <div className="filter-section">
            {groups.map((group, index) => (
              <label key={index}>
                <input type="checkbox" name={`group${index}`} /> {group}
              </label>
            ))}
          </div>
        )}

        <h3 onClick={() => setAlbumCollapsed(!albumCollapsed)}>
          Album
          <i className={`fas ${albumCollapsed ? 'fa-chevron-right' : 'fa-chevron-down'}`} style={{ marginLeft: '10px' }}></i>
        </h3>
        {!albumCollapsed && (
          <div className="filter-section">
            {albums.map((album, index) => (
              <label key={index}>
                <input type="checkbox" name={`album${index}`} /> {album}
              </label>
            ))}
          </div>
        )}

        <h3 onClick={() => setPriceCollapsed(!priceCollapsed)}>
          Price
          <i className={`fas ${priceCollapsed ? 'fa-chevron-right' : 'fa-chevron-down'}`} style={{ marginLeft: '10px' }}></i>
        </h3>
        {!priceCollapsed && (
          <div className="filter-section">
            <label>
              <input type="checkbox" name="price1" /> 0-20
            </label>
            <label>
              <input type="checkbox" name="price2" /> 20-40
            </label>
            <label>
              <input type="checkbox" name="price3" /> 40-60
            </label>
            <label>
              <input type="checkbox" name="price4" /> 60-80
            </label>
            <label>
              <input type="checkbox" name="price5" /> 80-100
            </label>
          </div>
        )}
      </div>
      <div className="products">
        <div className="sort">
          <label>
            Sort by:
            <select>
              <option value="recommend">Recommend</option>
              <option value="popularity">Most Popular</option>
              <option value="newest">Newest</option>
              <option value="priceLowToHigh">Price: Low to High</option>
              <option value="priceHighToLow">Price: High to Low</option>
            </select>
          </label>
        </div>
        <div className="product-list">
          {error ? (
            <div className="error">{error}</div>
          ) : (
            cards.map(card => (
              <Link to={`/card/${card.id}`} key={card.id} className="product-item">
                <img src={card.image_url} alt={card.card_name} className="card-image" />
                <div className="card-details">
                  <h2 className="card-name">{card.card_name}</h2>
                  <p className="card-price">${card.price}</p>
                  <p className="card-description">{card.description}</p>
                </div>
              </Link>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default Card;
