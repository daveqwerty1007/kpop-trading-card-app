import time
from werkzeug.security import generate_password_hash
from app.database import db
from app.models import User


def _admin_headers(test_client):
    unique_email = f'inv.admin.{time.time()}@example.com'
    admin = User(
        name='Inventory Admin',
        email=unique_email,
        password=generate_password_hash('adminpass', method='pbkdf2:sha256'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    login_resp = test_client.post('/admin/login', json={'email': unique_email, 'password': 'adminpass'})
    token = login_resp.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def _create_card(test_client, headers):
    resp = test_client.post('/cards/', json={
        'card_name': 'Inventory Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    }, headers=headers)
    return resp.get_json()['id']


def test_create_inventory(test_client):
    headers = _admin_headers(test_client)
    card_id = _create_card(test_client, headers)

    response = test_client.post('/inventory/', json={
        'card_id': card_id,
        'quantity_available': 50
    }, headers=headers)
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['card_id'] == card_id
    assert response_json['quantity_available'] == 50

def test_get_inventory(test_client):
    headers = _admin_headers(test_client)
    card_id = _create_card(test_client, headers)

    inventory_response = test_client.post('/inventory/', json={
        'card_id': card_id,
        'quantity_available': 50
    }, headers=headers)
    inventory_id = inventory_response.get_json()['id']

    response = test_client.get(f'/inventory/{inventory_id}')
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['card_id'] == card_id
    assert response_json['quantity_available'] == 50

def test_update_inventory(test_client):
    headers = _admin_headers(test_client)
    card_id = _create_card(test_client, headers)

    inventory_response = test_client.post('/inventory/', json={
        'card_id': card_id,
        'quantity_available': 50
    }, headers=headers)
    inventory_id = inventory_response.get_json()['id']

    response = test_client.put(f'/inventory/{inventory_id}', json={
        'quantity_available': 100
    }, headers=headers)
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['quantity_available'] == 100

def test_delete_inventory(test_client):
    headers = _admin_headers(test_client)
    card_id = _create_card(test_client, headers)

    inventory_response = test_client.post('/inventory/', json={
        'card_id': card_id,
        'quantity_available': 50
    }, headers=headers)
    inventory_id = inventory_response.get_json()['id']

    response = test_client.delete(f'/inventory/{inventory_id}', headers=headers)
    assert response.status_code == 204
