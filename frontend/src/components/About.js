// src/components/About.js
import React from 'react';
import './About.css';
import aboutImage from './About.png'; 
const About = () => {
  return (
    <div className="about">
      <h1>About Us</h1>
      <img src={aboutImage} alt="About Us" className="about-image" />
      <section className="about-section">
        <h2>Our Mission</h2>
        <p>At JssCards.co, our mission is to provide the best platform for buying and selling K-pop trading cards. We strive to offer a wide selection of cards, competitive pricing, and excellent customer service to K-pop enthusiasts around the world.</p>
      </section>
      <section className="about-section">
        <h2>Our Values</h2>
        <ul className="values-list">
          <li><strong>Integrity:</strong> We conduct our business with honesty and transparency.</li>
          <li><strong>Customer Satisfaction:</strong> Our customers are our top priority, and we aim to exceed their expectations.</li>
          <li><strong>Community:</strong> We are committed to building a strong and supportive community for K-pop fans.</li>
        </ul>
      </section>
      <section className="about-section">
        <h2>General Information</h2>
        <p><strong>Location:</strong> Based in Canada <span role="img" aria-label="Canada">🇨🇦</span></p>
        <p><strong>Pricing:</strong> All prices are in USD unless otherwise noted.</p>
        <p><strong>Worldwide Shipping:</strong> Worldwide shipping available.</p>
        <p><strong>Response Time:</strong> Please connect with us on social media if you do not receive a reply within 24 hours.</p>
        <p><strong>Proof of Purchase:</strong> Clickable proofs are appreciated.</p>
      </section>
    </div>
  );
};

export default About;
