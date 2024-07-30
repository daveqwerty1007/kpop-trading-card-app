import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Footer from './components/Footer';
import Cart from './components/Cart';
import Login from './components/Login';
import Contact from './components/Contact';
import About from './components/About';
import Privacy from './components/Privacy';
import Card from './components/Card';
import CardDetail from './components/CardDetail';
import AdminPanel from './components/AdminPanel';
import UserPanel from './components/UserPanel';
import SearchResults from './components/SearchResult';
import Checkout from './components/Checkout';
import OrderConfirmation from './components/OrderConfirmation';

const App = () => {
  return (
    <Router>
      <Header />
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/login" element={<Login />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/about" element={<About />} />
        <Route path="/privacy" element={<Privacy />} />
        <Route path="/card" element={<Card />} />
        <Route path="/card/:id" element={<CardDetail />} />
        <Route path="/admin_panel" element={<AdminPanel />} />
        <Route path="/user_panel" element={<UserPanel />} />
        <Route path='/search' element={<SearchResults/>}/>
        <Route path='/checkout' element={<Checkout/>}/>
        <Route path="/order-confirmation/:order_id" element={<OrderConfirmation />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;
