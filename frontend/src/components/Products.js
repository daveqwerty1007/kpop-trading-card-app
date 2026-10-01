import React, { useEffect, useState } from 'react';
import api from '../services/api';
import './Products.css';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [actionError, setActionError] = useState(null);
  const [form, setForm] = useState({ id: null, card_name: '', artist: '', group: '', album: '', price: '', description: '', image_url: '' });
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const response = await api.get('/cards/list');
      setProducts(response.data);
    } catch (error) {
      setError('Failed to fetch products');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm(prevForm => ({ ...prevForm, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const productData = { ...form, price: parseFloat(form.price) }; // Ensure price is a number

    setActionError(null);
    try {
      if (isEditing) {
        await api.put(`/cards/${form.id}`, productData);
      } else {
        await api.post('/cards/', productData);
      }

      setForm({ id: null, card_name: '', artist: '', group: '', album: '', price: '', description: '', image_url: '' });
      setIsEditing(false);
      fetchProducts(); // Refresh products list
    } catch (error) {
      setActionError(error.response?.data?.message || 'Failed to save product');
    }
  };

  const editProduct = (product) => {
    setForm(product);
    setIsEditing(true);
  };

  const deleteProduct = async (productId) => {
    setActionError(null);
    try {
      await api.delete(`/cards/${productId}`);
      setProducts(products.filter(product => product.id !== productId));
    } catch (error) {
      setActionError(error.response?.data?.message || 'Failed to delete product');
    }
  };

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="products">
      <h1>Products</h1>
      {actionError && <p className="error">{actionError}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="card_name"
          value={form.card_name}
          onChange={handleInputChange}
          placeholder="Card Name"
          required
        />
        <input
          type="text"
          name="artist"
          value={form.artist}
          onChange={handleInputChange}
          placeholder="Artist"
          required
        />
        <input
          type="text"
          name="group"
          value={form.group}
          onChange={handleInputChange}
          placeholder="Group"
          required
        />
        <input
          type="text"
          name="album"
          value={form.album}
          onChange={handleInputChange}
          placeholder="Album"
        />
        <input
          type="number"
          name="price"
          value={form.price}
          onChange={handleInputChange}
          placeholder="Price"
          required
        />
        <textarea
          name="description"
          value={form.description}
          onChange={handleInputChange}
          placeholder="Description"
        />
        <input
          type="text"
          name="image_url"
          value={form.image_url}
          onChange={handleInputChange}
          placeholder="Image URL"
        />
        <button type="submit">{isEditing ? 'Update' : 'Create'} Product</button>
      </form>
      <div className="product-grid">
        {products.map(product => (
          <div key={product.id} className="product-card">
            <img src={product.image_url} alt={product.card_name} />
            <h3>{product.card_name}</h3>
            <p>Artist: {product.artist}</p>
            <p>Group: {product.group}</p>
            <p>Album: {product.album}</p>
            <p>Price: ${product.price.toFixed(2)}</p>
            <p>{product.description}</p>
            <div className="product-actions">
              <button className="edit-btn" onClick={() => editProduct(product)}>Edit</button>
              <button className="delete-btn" onClick={() => deleteProduct(product.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Products;
