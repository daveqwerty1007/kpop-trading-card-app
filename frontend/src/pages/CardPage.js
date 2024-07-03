import React from 'react';
import CardDetail from '../components/CardDetail';

function CardPage({ match }) {
  return (
    <div>
      <CardDetail match={match} />
    </div>
  );
}

export default CardPage;
