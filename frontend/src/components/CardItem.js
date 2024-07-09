// src/components/CardItem.js
import React from 'react';
import { useDispatch } from 'react-redux';
import { Card, CardContent, CardMedia, Typography, Button } from '@mui/material';
import { addItemToCart } from '../redux/slices/cartSlice';

const CardItem = ({ card }) => {
  const dispatch = useDispatch();

  const handleAddToCart = () => {
    dispatch(addItemToCart(card));
  };

  return (
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
        <Button size="small" onClick={handleAddToCart}>
          Add to Cart
        </Button>
      </CardContent>
    </Card>
  );
};

export default CardItem;
