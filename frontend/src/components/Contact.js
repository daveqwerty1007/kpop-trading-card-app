import React from 'react';
import './Contact.css';
import wechatImage from './Wechat.png';

const Contact = () => {
  return (
    <div className="contact">
      <h1>Contact Us</h1>
      <div className="contact-links">
        <a href="https://www.instagram.com/jss123095/" className="contact-button">Instagram</a>
        <a href={wechatImage} className="contact-button">WeChat</a>
        <a href="mailto:megaminiondave@uwaterloo.ca" className="contact-button">Email</a>
      </div>
    </div>
  );
};

export default Contact;