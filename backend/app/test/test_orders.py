import time
from werkzeug.security import generate_password_hash
from app.database import db
from app.models import User


def _user_headers(test_client):
    unique_email = f'order.user.{time.time()}@example.com'
    test_client.post('/users/', json={
        'name': 'Order Tester',
        'email': unique_email,
        'password': 'password123'
    })
    login_resp = test_client.post('/users/login', json={'email': unique_email, 'password': 'password123'})
    token = login_resp.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def _admin_headers(test_client):
    unique_email = f'order.admin.{time.time()}@example.com'
    admin = User(
        name='Order Admin',
        email=unique_email,
        password=generate_password_hash('adminpass', method='pbkdf2:sha256'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    login_resp = test_client.post('/admin/login', json={'email': unique_email, 'password': 'adminpass'})
    token = login_resp.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def _checkout_order(test_client):
    """There is no direct order-creation endpoint — orders only come from
    the cart/checkout flow. Returns (order_id, owner_headers)."""
    headers = _user_headers(test_client)
    card_resp = test_client.post('/cards/', json={
        'card_name': 'Order Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 25.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    }, headers=_admin_headers(test_client))
    card_id = card_resp.get_json()['id']

    test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': 2}, headers=headers)

    checkout_resp = test_client.post('/orders/checkout', json={'payment_method': 'credit_card'}, headers=headers)
    assert checkout_resp.status_code == 200
    return checkout_resp.get_json()['order_id'], headers


def test_checkout_creates_order(test_client):
    order_id, headers = _checkout_order(test_client)
    assert order_id is not None

    response = test_client.get(f'/orders/{order_id}', headers=headers)
    assert response.status_code == 200
    assert response.get_json()['total_amount'] == 50.0

def test_get_order(test_client):
    order_id, headers = _checkout_order(test_client)

    response = test_client.get(f'/orders/{order_id}', headers=headers)
    assert response.status_code == 200

def test_get_order_forbidden_for_other_user(test_client):
    order_id, _owner_headers = _checkout_order(test_client)
    other_user_headers = _user_headers(test_client)

    response = test_client.get(f'/orders/{order_id}', headers=other_user_headers)
    assert response.status_code == 403

def test_update_order(test_client):
    order_id, _owner_headers = _checkout_order(test_client)
    admin_headers = _admin_headers(test_client)

    update_response = test_client.put(f'/orders/{order_id}', json={
        'total_amount': 150.0
    }, headers=admin_headers)
    assert update_response.status_code == 200
    assert update_response.get_json()['total_amount'] == 150.0

def test_delete_order(test_client):
    order_id, _owner_headers = _checkout_order(test_client)
    admin_headers = _admin_headers(test_client)

    delete_response = test_client.delete(f'/orders/{order_id}', headers=admin_headers)
    assert delete_response.status_code == 204

def test_order_listing_requires_admin(test_client):
    _checkout_order(test_client)
    user_headers = _user_headers(test_client)
    for path in ['/orders/list', '/orders/search?q=Order', '/orders/filter-options']:
        assert test_client.get(path).status_code == 401
        assert test_client.get(path, headers=user_headers).status_code == 403
    response = test_client.get('/orders/list', headers=_admin_headers(test_client))
    assert response.status_code == 200
    assert len(response.get_json()) >= 1
