import os
import pytest
from datetime import datetime
from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import User
from flask import current_app
import logging
import time

os.environ["TESTING"] = "1"

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    # Requests below share this one app context, so Flask-SQLAlchemy never
    # ends the session between them. Roll back after each request like a real
    # one would, so a failed request can't poison every later test.
    flask_app.teardown_request(lambda exc: db.session.rollback())

    with flask_app.app_context():
        db.create_all()
        logging.info("Database tables created for testing.")
        
        yield flask_app.test_client()
        
        db.drop_all()
        logging.info("Database tables dropped after testing.")

@pytest.fixture(scope='module')
def init_database():
    flask_app = create_app()
    
    with flask_app.app_context():
        db.create_all()
        logging.info("Database tables created for init_database fixture.")
        
        yield db
        
        db.session.remove()
        db.drop_all()
        logging.info("Database tables dropped after init_database fixture.")

@pytest.fixture
def auth_headers(test_client):
    """Register a fresh user and return Authorization headers for it."""
    unique_email = f'auth.user.{time.time()}@example.com'
    test_client.post('/users/', json={
        'name': 'Auth User',
        'email': unique_email,
        'password': 'password123'
    })
    login_resp = test_client.post('/users/login', json={
        'email': unique_email,
        'password': 'password123'
    })
    token = login_resp.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def admin_headers(test_client):
    """Create a fresh admin and return Authorization headers for it."""
    unique_email = f'admin.{time.time()}@example.com'
    db.session.add(User(
        name='Fixture Admin',
        email=unique_email,
        password=generate_password_hash('adminpass', method='pbkdf2:sha256'),
        role='admin'
    ))
    db.session.commit()
    login_resp = test_client.post('/admin/login', json={'email': unique_email, 'password': 'adminpass'})
    token = login_resp.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def create_order(test_client, auth_headers, admin_headers):
    """Create a real order via the cart/checkout flow (there is no direct
    order-creation endpoint). Returns (order_id, headers) for the owning user."""
    card_resp = test_client.post('/cards/', json={
        'card_name': 'Fixture Card', 'artist': 'A', 'group': 'G', 'album': 'Al',
        'price': 100.0, 'description': 'd', 'image_url': 'url'
    }, headers=admin_headers)
    card_id = card_resp.get_json()['id']
    test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': 1}, headers=auth_headers)
    checkout_resp = test_client.post('/orders/checkout', json={'payment_method': 'credit_card'}, headers=auth_headers)
    assert checkout_resp.status_code == 200
    return checkout_resp.get_json()['order_id'], auth_headers

@pytest.fixture
def create_payment(test_client, create_order, admin_headers):
    """Returns (payment_id, owner_headers, admin_headers)."""
    order_id, headers = create_order
    response = test_client.post('/payments/', json={
        'order_id': order_id,
        'payment_date': '2022-01-01T00:00:00Z',
        'payment_method': 'credit_card',
        'payment_status': 'Completed'
    }, headers=admin_headers)
    assert response.status_code == 201
    return response.get_json()['id'], headers, admin_headers
