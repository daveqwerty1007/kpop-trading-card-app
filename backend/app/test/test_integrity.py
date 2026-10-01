import time


def _user(test_client):
    """Create a user and log in. Returns (user_id, headers)."""
    email = f'integrity.{time.time()}@example.com'
    test_client.post('/users/', json={'name': 'Integrity User', 'email': email, 'password': 'pw'})
    login = test_client.post('/users/login', json={'email': email, 'password': 'pw'}).get_json()
    return login['user_id'], {'Authorization': f'Bearer {login["access_token"]}'}


def _card(test_client, admin_headers, stock=None, name=None):
    card_id = test_client.post('/cards/', json={
        'card_name': name or f'Card {time.time()}', 'artist': 'A', 'group': 'G', 'price': 5.0
    }, headers=admin_headers).get_json()['id']
    if stock is not None:
        test_client.post('/inventory/', json={'card_id': card_id, 'quantity_available': stock},
                         headers=admin_headers)
    return card_id


def _buy(test_client, headers, card_id, quantity=1):
    test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': quantity}, headers=headers)
    response = test_client.post('/orders/checkout', json={'payment_method': 'paypal'}, headers=headers)
    assert response.status_code == 200
    return response.get_json()['order_id']


def test_delete_user_with_cart_items(test_client, admin_headers):
    user_id, headers = _user(test_client)
    test_client.post('/cart_items/', json={'card_id': _card(test_client, admin_headers), 'quantity': 1},
                     headers=headers)
    response = test_client.delete('/admin/delete_user', json={'id': user_id}, headers=admin_headers)
    assert response.status_code == 204


def test_delete_user_with_orders_is_refused(test_client, admin_headers):
    user_id, headers = _user(test_client)
    _buy(test_client, headers, _card(test_client, admin_headers))
    response = test_client.delete('/admin/delete_user', json={'id': user_id}, headers=admin_headers)
    assert response.status_code == 409
    assert 'orders' in response.get_json()['message']


def test_delete_card_with_stock_and_cart_entries(test_client, admin_headers):
    _, headers = _user(test_client)
    card_id = _card(test_client, admin_headers, stock=3)
    test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': 1}, headers=headers)

    assert test_client.delete(f'/cards/{card_id}', headers=admin_headers).status_code == 204
    assert test_client.get(f'/cards/{card_id}').status_code == 404
    assert test_client.get('/orders/cart', headers=headers).get_json()['cart_items'] == []
    assert [i for i in test_client.get('/inventory/').get_json() if i['card_id'] == card_id] == []


def test_delete_card_in_past_orders_is_refused(test_client, admin_headers):
    _, headers = _user(test_client)
    card_id = _card(test_client, admin_headers)
    _buy(test_client, headers, card_id)
    assert test_client.delete(f'/cards/{card_id}', headers=admin_headers).status_code == 409
    assert test_client.get('/users/orders', headers=headers).status_code == 200


def test_delete_order_removes_its_payment(test_client, admin_headers):
    _, headers = _user(test_client)
    order_id = _buy(test_client, headers, _card(test_client, admin_headers))
    payment_id = test_client.post('/payments/', json={
        'order_id': order_id, 'payment_date': '2026-01-01T00:00:00',
        'payment_method': 'paypal', 'payment_status': 'Completed'
    }, headers=admin_headers).get_json()['id']

    assert test_client.delete(f'/orders/{order_id}', headers=admin_headers).status_code == 204
    assert test_client.get(f'/payments/{payment_id}', headers=admin_headers).status_code == 404


def test_order_status_comes_from_payment(test_client, admin_headers):
    _, headers = _user(test_client)
    order_id = _buy(test_client, headers, _card(test_client, admin_headers))
    assert test_client.get(f'/orders/{order_id}', headers=headers).get_json()['status'] == 'Completed'
    statuses = {o['id']: o['status'] for o in test_client.get('/orders/list', headers=admin_headers).get_json()}
    assert statuses[order_id] == 'Completed'


def test_card_update_cannot_change_id(test_client, admin_headers):
    card_id = _card(test_client, admin_headers)
    response = test_client.put(f'/cards/{card_id}', json={
        'id': card_id + 1000, 'card_name': 'Renamed', 'artist': 'A', 'group': 'G', 'price': 7.0
    }, headers=admin_headers)
    assert response.status_code == 200
    assert response.get_json()['id'] == card_id
    assert test_client.get(f'/cards/{card_id}').get_json()['card_name'] == 'Renamed'


def test_card_update_missing_card(test_client, admin_headers):
    response = test_client.put('/cards/999999', json={
        'card_name': 'X', 'artist': 'A', 'group': 'G', 'price': 1.0
    }, headers=admin_headers)
    assert response.status_code == 404


def test_adding_same_card_twice_merges_quantity(test_client, admin_headers):
    _, headers = _user(test_client)
    card_id = _card(test_client, admin_headers)
    test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': 1}, headers=headers)
    test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': 4}, headers=headers)
    [item] = test_client.get('/orders/cart', headers=headers).get_json()['cart_items']
    assert item['quantity'] == 5


def test_cart_rejects_bad_input(test_client, admin_headers):
    _, headers = _user(test_client)
    card_id = _card(test_client, admin_headers)
    assert test_client.post('/cart_items/', json={'card_id': 999999, 'quantity': 1},
                            headers=headers).status_code == 404
    for bad in [{'card_id': card_id, 'quantity': 0}, {'card_id': card_id, 'quantity': -2}, {'quantity': 1}]:
        assert test_client.post('/cart_items/', json=bad, headers=headers).status_code == 400

    item_id = test_client.post('/cart_items/', json={'card_id': card_id, 'quantity': 1},
                               headers=headers).get_json()['id']
    for bad in [{}, {'quantity': -3}, {'quantity': 0}]:
        assert test_client.put(f'/cart_items/{item_id}', json=bad, headers=headers).status_code == 400
    assert test_client.get('/orders/cart', headers=headers).status_code == 200


def test_inventory_missing_item(test_client, admin_headers):
    assert test_client.put('/inventory/999999', json={'quantity_available': 1},
                           headers=admin_headers).status_code == 404
    assert test_client.delete('/inventory/999999', headers=admin_headers).status_code == 404


def test_duplicate_email(test_client, admin_headers):
    email = f'dupe.{time.time()}@example.com'
    assert test_client.post('/users/register', json={'name': 'A', 'email': email, 'password': 'pw'}).status_code == 200
    response = test_client.post('/users/register', json={'name': 'B', 'email': email, 'password': 'pw'})
    assert response.status_code == 409
    assert 'already registered' in response.get_json()['message']
    assert test_client.post('/users/', json={'name': 'B', 'email': email, 'password': 'pw'}).status_code == 409
    assert test_client.post('/admin/create_user', json={'name': 'B', 'email': email, 'password': 'pw'},
                            headers=admin_headers).status_code == 409

    _, headers = _user(test_client)
    assert test_client.post('/users/update_user', json={'name': 'B', 'email': email},
                            headers=headers).status_code == 409


def test_restock_list_puts_best_sellers_first(test_client, admin_headers):
    _, headers = _user(test_client)
    slow = _card(test_client, admin_headers, stock=2, name=f'Slow {time.time()}')
    fast = _card(test_client, admin_headers, stock=5, name=f'Fast {time.time()}')
    _buy(test_client, headers, slow, quantity=1)   # 1 sold, 1 left
    _buy(test_client, headers, fast, quantity=4)   # 4 sold, 1 left

    dashboard = test_client.get('/admin/dashboard', headers=admin_headers).get_json()
    names = [row['card_name'] for row in dashboard['restock_list']
             if row['card_name'].startswith(('Slow', 'Fast'))]
    assert [n.split()[0] for n in names] == ['Fast', 'Slow']
    assert 'sales_data_last_30_days' in dashboard
