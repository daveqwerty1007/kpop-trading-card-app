import React from 'react';
import './Home.css';

const Home = () => {
  return (
    <div className="home">
      <section className="recommend">
        <h2>Recommend</h2>
        {/* Add carousel or grid of recommended cards here */}
      </section>
      <section className="popular">
        <h2>Popular</h2>
        {/* Add grid of popular cards here */}
      </section>
      <section className="browse">
        <h2>Browse Our Inventory</h2>
        {/* Add browse by inventory section here */}
      </section>
    </div>
  );
};

export default Home;