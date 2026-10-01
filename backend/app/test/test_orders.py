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


def _card_with_stock(test_client, admin_headers, price, stock):
    card_id = test_client.post('/cards/', json={
        'card_name': f'Stock Card {time.time()}', 'artist': 'A', 'group': 'G', 'price': price
    }, headers=admin_headers).get_json()['id']
    inventory_id = None
    if stock is not None:
        inventory_id = test_client.post('/inventory/', json={
            'card_id': card_id, 'quantity_available': stock
        }, headers=admin_headers).get_json()['id']
    return card_id, inventory_id


def _stock(test_client, inventory_id):
    return test_client.get(f'/inventory/{inventory_id}').get_json()['quantity_available']


def test_checkout_records_items_and_takes_stock(test_client):
    admin = _admin_headers(test_client)
    headers = _user_headers(test_client)
    card_a, inv_a = _card_with_stock(test_client, admin, price=10.0, stock=5)
    card_b, inv_b = _card_with_stock(test_client, admin, price=3.0, stock=2)
    test_client.post('/cart_items/', json={'card_id': card_a, 'quantity': 3}, headers=headers)
    test_client.post('/cart_items/', json={'card_id': card_b, 'quantity': 2}, headers=headers)

    response = test_client.post('/orders/checkout', json={'payment_method': 'paypal'}, headers=headers)
    assert response.status_code == 200
    order_id = response.get_json()['order_id']

    orders = test_client.get('/users/orders', headers=headers).get_json()
    [order] = [o for o in orders if o['order_id'] == order_id]
    assert order['total_amount'] == 36.0
    assert sorted((i['card_name'].startswith('Stock Card'), i['quantity']) for i in order['items']) == [(True, 2), (True, 3)]
    assert _stock(test_client, inv_a) == 2
    assert _stock(test_client, inv_b) == 0
    assert test_client.get('/orders/cart', headers=headers).get_json()['cart_items'] == []


def test_checkout_out_of_stock_changes_nothing(test_client):
    admin = _admin_headers(test_client)
    headers = _user_headers(test_client)
    card_ok, inv_ok = _card_with_stock(test_client, admin, price=1.0, stock=10)
    card_low, inv_low = _card_with_stock(test_client, admin, price=1.0, stock=1)
    test_client.post('/cart_items/', json={'card_id': card_ok, 'quantity': 4}, headers=headers)
    test_client.post('/cart_items/', json={'card_id': card_low, 'quantity': 2}, headers=headers)

    response = test_client.post('/orders/checkout', json={'payment_method': 'paypal'}, headers=headers)
    assert response.status_code == 400
    assert 'left in stock' in response.get_json()['message']
    assert test_client.get('/users/orders', headers=headers).get_json() == []
    assert len(test_client.get('/orders/cart', headers=headers).get_json()['cart_items']) == 2
    assert _stock(test_client, inv_ok) == 10
    assert _stock(test_client, inv_low) == 1


def test_checkout_requires_payment_method(test_client):
    admin = _admin_headers(test_client)
    headers = _user_headers(test_client)
    card_id, _ = _card_with_stock(test_client, admin, price=1.0, stock=None)
    test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': 1}, headers=headers)

    for body in [{}, {'payment_method': ''}]:
        response = test_client.post('/orders/checkout', json=body, headers=headers)
        assert response.status_code == 400
    assert test_client.get('/users/orders', headers=headers).get_json() == []
    assert len(test_client.get('/orders/cart', headers=headers).get_json()['cart_items']) == 1


def test_checkout_card_without_inventory_row(test_client):
    admin = _admin_headers(test_client)
    headers = _user_headers(test_client)
    card_id, _ = _card_with_stock(test_client, admin, price=2.5, stock=None)
    test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': 4}, headers=headers)
    response = test_client.post('/orders/checkout', json={'payment_method': 'paypal'}, headers=headers)
    assert response.status_code == 200
    [order] = test_client.get('/users/orders', headers=headers).get_json()
    assert order['total_amount'] == 10.0 and order['items'][0]['quantity'] == 4
