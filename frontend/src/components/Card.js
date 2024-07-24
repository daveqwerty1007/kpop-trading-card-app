import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom'; 
import './Card.css';

const CardList = () => {
  const [cards, setCards] = useState([]);
  const [error, setError] = useState('');
  const [filters, setFilters] = useState({
    artist: [],
    group: [],
    album: [],
    min_price: '',
    max_price: '',
    sort_by: ''
  });
  const [filterOptions, setFilterOptions] = useState({
    artists: [],
    groups: [],
    albums: []
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [collapsedSections, setCollapsedSections] = useState({
    artist: false,
    group: false,
    album: false,
    price: false
  });
  const cardsPerPage = 10;
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const sortBy = params.get('sort_by');
    if (sortBy) {
      setFilters(prevFilters => ({
        ...prevFilters,
        sort_by: sortBy
      }));
    }
    fetchFilteredCards();
    fetchFilterOptions();
  }, [filters, currentPage]);

  const fetchFilteredCards = () => {
    let url = 'http://localhost:5001/cards/list';
    const params = new URLSearchParams({
      ...filters,
      artist: filters.artist.join(','),
      group: filters.group.join(','),
      album: filters.album.join(','),
      page: currentPage,
      limit: cardsPerPage
    });
    if (params.toString()) {
      url += `?${params.toString()}`;
    }

    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          setCards(data);
          setTotalPages(Math.ceil(data.total / cardsPerPage));
          setError('');
        } else {
          setError('Unexpected response format');
        }
      })
      .catch(error => {
        console.error('Error fetching cards:', error);
        setError('Failed to load cards');
      });
  };

  const fetchFilterOptions = () => {
    fetch('http://localhost:5001/cards/filter-options')
      .then(response => response.json())
      .then(data => {
        setFilterOptions({
          artists: data.artists || [],
          groups: data.groups || [],
          albums: data.albums || []
        });
      })
      .catch(error => {
        console.error('Error fetching filter options:', error);
      });
  };

  const handleCheckboxChange = (event) => {
    const { name, value, checked } = event.target;
    setFilters(prevFilters => {
      const values = checked
        ? [...prevFilters[name], value]
        : prevFilters[name].filter(v => v !== value);
      return { ...prevFilters, [name]: values };
    });
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFilters(prevFilters => ({ ...prevFilters, [name]: value }));
  };

  const handleSortChange = (event) => {
    setFilters(prevFilters => ({
      ...prevFilters,
      sort_by: event.target.value
    }));
  };

  const handleClearFilters = () => {
    setFilters({
      artist: [],
      group: [],
      album: [],
      min_price: '',
      max_price: '',
      sort_by: ''
    });
    setCurrentPage(1);
  };

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };

  const toggleSection = (section) => {
    setCollapsedSections(prevState => ({
      ...prevState,
      [section]: !prevState[section]
    }));
  };

  const handleCardClick = (cardId) => {
    navigate(`/card/${cardId}`);
  };

  return (
    <div className="card-page">
      <div className="filter-bar">
        <div className="filter-header">
          <h3>Filter by:</h3>
          <button type="button" onClick={handleClearFilters} className="clear-button">Clear Filters</button>
        </div>
        <div className="filter-section">
          <h4 onClick={() => toggleSection('artist')}>Artists {collapsedSections.artist ? '+' : '-'}</h4>
          {!collapsedSections.artist && (
            <div>
              {filterOptions.artists.map((artist, index) => (
                <label key={index}>
                  <input
                    type="checkbox"
                    name="artist"
                    value={artist}
                    checked={filters.artist.includes(artist)}
                    onChange={handleCheckboxChange}
                  />
                  {artist}
                </label>
              ))}
            </div>
          )}
        </div>
        <div className="filter-section">
          <h4 onClick={() => toggleSection('group')}>Groups {collapsedSections.group ? '+' : '-'}</h4>
          {!collapsedSections.group && (
            <div>
              {filterOptions.groups.map((group, index) => (
                <label key={index}>
                  <input
                    type="checkbox"
                    name="group"
                    value={group}
                    checked={filters.group.includes(group)}
                    onChange={handleCheckboxChange}
                  />
                  {group}
                </label>
              ))}
            </div>
          )}
        </div>
        <div className="filter-section">
          <h4 onClick={() => toggleSection('album')}>Albums {collapsedSections.album ? '+' : '-'}</h4>
          {!collapsedSections.album && (
            <div>
              {filterOptions.albums.map((album, index) => (
                <label key={index}>
                  <input
                    type="checkbox"
                    name="album"
                    value={album}
                    checked={filters.album.includes(album)}
                    onChange={handleCheckboxChange}
                  />
                  {album}
                </label>
              ))}
            </div>
          )}
        </div>
        <div className="filter-section">
          <h4 onClick={() => toggleSection('price')}>Price Range {collapsedSections.price ? '+' : '-'}</h4>
          {!collapsedSections.price && (
            <div>
              <label>
                Min Price:
                <input
                  type="number"
                  name="min_price"
                  value={filters.min_price}
                  onChange={handleInputChange}
                  placeholder="Min"
                />
              </label>
              <label>
                Max Price:
                <input
                  type="number"
                  name="max_price"
                  value={filters.max_price}
                  onChange={handleInputChange}
                  placeholder="Max"
                />
              </label>
            </div>
          )}
        </div>
      </div>
      <div className="products">
        <div className="sort-bar">
          <select value={filters.sort_by} onChange={handleSortChange}>
            <option value="">Sort By</option>
            <option value="price_asc">Price: Low to High</option>
            <option value="price_desc">Price: High to Low</option>
            <option value="latest">Latest</option>
            <option value="recommended">Recommended</option>
          </select>
        </div>
        {error && <div className="error">{error}</div>}
        <div className="product-list">
          {cards.map(card => (
            <div
              className="product-item"
              key={card.id}
              onClick={() => handleCardClick(card.id)}
              style={{ cursor: 'pointer' }}
            >
              <img src={card.image_url} alt={card.card_name} />
              <div className="card-details">
                <h3 className="card-name">{card.card_name}</h3>
                <p className="card-price">${card.price}</p>
                <p className="card-description">{card.description}</p>
              </div>
            </div>
          ))}
        </div>
        <div className="pagination">
          {Array.from({ length: totalPages }, (_, i) => (
            <button
              key={i}
              onClick={() => handlePageChange(i + 1)}
              disabled={i + 1 === currentPage}
            >
              {i + 1}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CardList;
