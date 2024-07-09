// src/pages/CardDetail.js
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { addItemToCart } from '../redux/slices/cartSlice';
import api from '../services/api';
import { Container, Typography, Button, Card, CardMedia, CardContent, TextField } from '@mui/material';

const CardDetail = () => {
  const { id } = useParams();
  const [card, setCard] = useState(null);
  const [quoteRequest, setQuoteRequest] = useState('');
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);

  useEffect(() => {
    const fetchCard = async () => {
      try {
        const response = await api.get(`/cards/${id}`);
        setCard(response.data);
      } catch (error) {
        console.error('Failed to fetch card', error);
      }
    };

    fetchCard();
  }, [id]);

  const handleAddToCart = () => {
    dispatch(addItemToCart(card));
  };

  const handleRequestQuote = async () => {
    try {
      await api.post('/quotes', { cardId: id, message: quoteRequest });
      alert('Quote request sent successfully!');
    } catch (error) {
      console.error('Failed to send quote request', error);
    }
  };

  if (!card) {
    return <div>Loading...</div>;
  }

  return (
    <Container>
      <Card>
        <CardMedia
          component="img"
          height="300"
          image={card.imageUrl}
          alt={card.title}
        />
        <CardContent>
          <Typography variant="h4" gutterBottom>
            {card.title}
          </Typography>
          <Typography variant="body1" color="textSecondary" paragraph>
            {card.description}
          </Typography>
          <Typography variant="h6" color="textPrimary">
            Price: ${card.price}
          </Typography>
          <Button variant="contained" color="primary" onClick={handleAddToCart} style={{ marginTop: '10px' }}>
            Add to Cart
          </Button>
          {user && (
            <div style={{ marginTop: '20px' }}>
              <Typography variant="h6" color="textPrimary">
                Request a Picture and Quote
              </Typography>
              <TextField
                label="Message"
                value={quoteRequest}
                onChange={(e) => setQuoteRequest(e.target.value)}
                fullWidth
                multiline
                rows={4}
                variant="outlined"
                margin="normal"
              />
              <Button variant="contained" color="secondary" onClick={handleRequestQuote}>
                Request Quote
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </Container>
  );
};

export default CardDetail;
