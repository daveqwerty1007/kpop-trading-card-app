import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './SearchResults.css';

const SearchResults = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const query = new URLSearchParams(location.search).get('q');
    if (query) {
      fetchSearchResults(query);
    }
  }, [location.search]);

  const fetchSearchResults = async (query) => {
    try {
      const response = await fetch(`http://localhost:5001/cards/search?q=${encodeURIComponent(query)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch search results');
      }
      const data = await response.json();
      setResults(data);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCardClick = (cardId) => {
    navigate(`/card/${cardId}`);
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="card-page">
      <h1>Search Results</h1>
      <div className="product-list">
        {results.length === 0 ? (
          <p>No results found for your search.</p>
        ) : (
          results.map((result) => (
            <div
              className="product-item"
              key={result.id}
              onClick={() => handleCardClick(result.id)}
              style={{ cursor: 'pointer' }}
            >
              <img src={result.image_url} alt={result.card_name} />
              <div className="card-details">
                <h3 className="card-name">{result.card_name}</h3>
                <p className="card-price">${result.price}</p>
                <p className="card-description">{result.description}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default SearchResults;
