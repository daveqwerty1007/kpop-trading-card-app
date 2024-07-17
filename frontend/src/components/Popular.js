import React from 'react';
import './Popular.css';

const Popular = () => {
  return (
    <div className="popular-page">
      <div className="popular-content">
        <aside className="popular-filter">
          <h2>Filter</h2>
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
        <main className="popular-items">
          <h2>Popular Items</h2>
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

export default Popular;
