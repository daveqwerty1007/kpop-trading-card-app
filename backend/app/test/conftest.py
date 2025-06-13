import pytest
from datetime import datetime
from app import create_app, db
from flask import current_app
import logging
import time

logging.basicConfig(level=logging.INFO)

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    
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
def create_user(test_client):
    unique_email = f'john.doe{time.time()}@example.com'
    response = test_client.post('/users/', json={
        'name': 'John Doe',
        'email': unique_email,
        'password': 'password123'
    })
    assert response.status_code == 201
    return response.get_json()['user_id']

@pytest.fixture
def create_order(test_client, create_user):
    user_id = create_user
    response = test_client.post('/orders/', json={
        'user_id': user_id,
        'order_date': '2022-01-01T00:00:00Z',
        'total_amount': 100.0
    })
    assert response.status_code == 201
    return response.get_json()['id']

@pytest.fixture
def create_payment(test_client, create_order):
    order_id = create_order
    response = test_client.post('/payments/', json={
        'order_id': order_id,
        'payment_date': '2022-01-01T00:00:00Z',
        'payment_method': 'credit_card',
        'payment_status': 'Completed'
    })
    assert response.status_code == 201
    return response.get_json()['id']
