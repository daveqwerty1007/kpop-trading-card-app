import React from 'react';
import './Recommend.css';

const Recommend = () => {
  return (
    <div className="recommend-page">
      <div className="recommend-content">
        <aside className="recommend-filter">
          <div className="filter-group">
            <h3>Artist</h3>
            <ul>
              <li><input type="checkbox" /> Artist 1</li>
              <li><input type="checkbox" /> Artist 2</li>
              <li><input type="checkbox" /> Artist 3</li>
            </ul>
          </div>
          <div className="filter-group">
            <h3>Group</h3>
            <ul>
              <li><input type="checkbox" /> Group 1</li>
              <li><input type="checkbox" /> Group 2</li>
              <li><input type="checkbox" /> Group 3</li>
            </ul>
          </div>
          <div className="filter-group">
            <h3>Album</h3>
            <ul>
              <li><input type="checkbox" /> Album 1</li>
              <li><input type="checkbox" /> Album 2</li>
              <li><input type="checkbox" /> Album 3</li>
            </ul>
          </div>
          <div className="filter-group">
            <h3>Price</h3>
            <ul>
              <li><input type="checkbox" /> 0 - 100</li>
              <li><input type="checkbox" /> 100 - 200</li>
            </ul>
          </div>
        </aside>
        <main className="recommend-items">
          <div className="sort-by">
            <label htmlFor="sort">Sort by:</label>
            <select id="sort">
              <option value="popularity">Popularity</option>
              <option value="newest">Newest</option>
              <option value="price-asc">Price: Low to High</option>
              <option value="price-desc">Price: High to Low</option>
            </select>
          </div>
          <div className="items-grid">
            {/* Add your items here */}
            <div className="item-card">Item 1</div>
            <div className="item-card">Item 2</div>
            <div className="item-card">Item 3</div>
            <div className="item-card">Item 4</div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Recommend;
