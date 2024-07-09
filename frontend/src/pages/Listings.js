// src/pages/Listings.js
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Grid, Container, Card, CardContent, CardMedia, Typography, Button } from '@mui/material';
import api from '../services/api';

const Listings = () => {
  const [cards, setCards] = useState([]);

  useEffect(() => {
    const fetchCards = async () => {
      try {
        const response = await api.get('/cards');
        setCards(response.data);
      } catch (error) {
        console.error('Failed to fetch cards', error);
      }
    };

    fetchCards();
  }, []);

  return (
    <Container>
      <Grid container spacing={3}>
        {cards.map((card) => (
          <Grid item xs={12} sm={6} md={4} key={card.id}>
            <Card>
              <CardMedia
                component="img"
                height="140"
                image={card.imageUrl}
                alt={card.title}
              />
              <CardContent>
                <Typography variant="h5" component="div">
                  {card.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {card.description}
                </Typography>
                <Typography variant="h6" component="div">
                  ${card.price}
                </Typography>
                <Button size="small" component={Link} to={`/card/${card.id}`}>
                  View Details
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Listings;
