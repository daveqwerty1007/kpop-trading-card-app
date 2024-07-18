import React, { useState } from 'react';
import './Card.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

function Card() {
  const [artistCollapsed, setArtistCollapsed] = useState(false);
  const [groupCollapsed, setGroupCollapsed] = useState(false);
  const [albumCollapsed, setAlbumCollapsed] = useState(false);
  const [priceCollapsed, setPriceCollapsed] = useState(false);

  return (
    <div className="card-page">
      <div className="filter">
        <h3 onClick={() => setArtistCollapsed(!artistCollapsed)}>
          Artist
          <i className={`fas ${artistCollapsed ? 'fa-chevron-right' : 'fa-chevron-down'}`} style={{ marginLeft: '10px' }}></i>
        </h3>
        {!artistCollapsed && (
          <div className="filter-section">
            <label>
              <input type="checkbox" name="artist1" /> Artist 1
            </label>
            <label>
              <input type="checkbox" name="artist2" /> Artist 2
            </label>
            <label>
              <input type="checkbox" name="artist3" /> Artist 3
            </label>
          </div>
        )}

        <h3 onClick={() => setGroupCollapsed(!groupCollapsed)}>
          Group
          <i className={`fas ${groupCollapsed ? 'fa-chevron-right' : 'fa-chevron-down'}`} style={{ marginLeft: '10px' }}></i>
        </h3>
        {!groupCollapsed && (
          <div className="filter-section">
            <label>
              <input type="checkbox" name="group1" /> Group 1
            </label>
            <label>
              <input type="checkbox" name="group2" /> Group 2
            </label>
          </div>
        )}

        <h3 onClick={() => setAlbumCollapsed(!albumCollapsed)}>
          Album
          <i className={`fas ${albumCollapsed ? 'fa-chevron-right' : 'fa-chevron-down'}`} style={{ marginLeft: '10px' }}></i>
        </h3>
        {!albumCollapsed && (
          <div className="filter-section">
            <label>
              <input type="checkbox" name="album1" /> Album 1
            </label>
            <label>
              <input type="checkbox" name="album2" /> Album 2
            </label>
          </div>
        )}

        <h3 onClick={() => setPriceCollapsed(!priceCollapsed)}>
          Price
          <i className={`fas ${priceCollapsed ? 'fa-chevron-right' : 'fa-chevron-down'}`} style={{ marginLeft: '10px' }}></i>
        </h3>
        {!priceCollapsed && (
          <div className="filter-section">
            <label>
              <input type="checkbox" name="price1" /> 0-100
            </label>
            <label>
              <input type="checkbox" name="price2" /> 100-200
            </label>
          </div>
        )}
      </div>
      <div className="products">
        <div className="sort">
          <label>
            Sort by:
            <select>
              <option value="popularity">Recommend</option>
              <option value="popularity">Most Popular</option>
              <option value="newest">Newest</option>
              <option value="priceLowToHigh">Price: Low to High</option>
              <option value="priceHighToLow">Price: High to Low</option>
            </select>
          </label>
        </div>
        <div className="product-list">
          <div className="product-item">Item 1</div>
          <div className="product-item">Item 2</div>
          <div className="product-item">Item 3</div>
          <div className="product-item">Item 4</div>
        </div>
      </div>
    </div>
  );
}

export default Card;
