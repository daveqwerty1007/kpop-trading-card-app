import React, { useEffect, useState } from 'react';
import Slider from 'react-slick';
import { useNavigate } from 'react-router-dom';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import './Home.css';

const Home = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [latest, setLatest] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('http://localhost:5001/cards/list?sort_by=recommended')
      .then(response => response.json())
      .then(data => setRecommendations(data))
      .catch(error => console.error('Error fetching recommendations:', error));

    fetch('http://localhost:5001/cards/list?sort_by=latest')
      .then(response => response.json())
      .then(data => setLatest(data))
      .catch(error => console.error('Error fetching latest cards:', error));
  }, []);

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 4,
    slidesToScroll: 4,
    responsive: [
      {
        breakpoint: 1024,
        settings: {
          slidesToShow: 3,
          slidesToScroll: 3,
          infinite: true,
          dots: true
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
    ]
  };

  const handleCardClick = (id) => {
    navigate(`/card/${id}`);
  };

  const handleTitleClick = (sortBy) => {
    navigate(`/card?sort_by=${sortBy}`);
  };

  const handleViewAllCardsClick = () => {
    navigate('/card');
  };

  return (
    <div className="home">
      <section className="recommend">
        <h2 onClick={() => handleTitleClick('recommended')}>Today's Recommend</h2>
        <Slider {...settings}>
          {recommendations.map(card => (
            <div className="card" key={card.id} onClick={() => handleCardClick(card.id)}>
              <img src={card.image_url} alt={card.card_name} />
              <div className="card-info">
                <h3>{card.card_name}</h3>
                <p>Artist: {card.artist}</p>
                <p>Album: {card.album}</p>
                <p>Price: ${card.price}</p>
              </div>
            </div>
          ))}
        </Slider>
      </section>
      <section className="latest">
        <h2 onClick={() => handleTitleClick('latest')}>Latest</h2>
        <Slider {...settings}>
          {latest.map(card => (
            <div className="card" key={card.id} onClick={() => handleCardClick(card.id)}>
              <img src={card.image_url} alt={card.card_name} />
              <div className="card-info">
                <h3>{card.card_name}</h3>
                <p>Artist: {card.artist}</p>
                <p>Album: {card.album}</p>
                <p>Price: ${card.price}</p>
              </div>
            </div>
          ))}
        </Slider>
      </section>
      <section className="view-all-cards">
        <div className="view-all-cards-bar" onClick={handleViewAllCardsClick}>
          View All Cards
        </div>
      </section>
    </div>
  );
};

export default Home;
