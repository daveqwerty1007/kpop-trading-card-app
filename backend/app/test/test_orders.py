import time

def test_create_order(test_client, init_database):
    # Ensure a user exists first
    user_response = test_client.post('/users/', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert user_response.status_code == 201
    user_id = user_response.get_json()['id']
    
    response = test_client.post('/orders/', json={
        'user_id': user_id,
        'order_date': '2022-01-01T00:00:00Z',
        'total_amount': 100.0
    })
    assert response.status_code == 201

import time

def test_get_order(test_client, init_database):
    # Ensure a user and order exist first
    unique_email = f'john.doe{time.time()}@example.com'
    user_response = test_client.post('/users/', json={
        'name': 'John Doe',
        'email': unique_email,
        'password': 'password123'
    })
    assert user_response.status_code == 201
    user_id = user_response.get_json()['id']

    order_response = test_client.post('/orders/', json={
        'user_id': user_id,
        'order_date': '2022-01-01T00:00:00Z',
        'total_amount': 100.0
    })
    assert order_response.status_code == 201
    order_id = order_response.get_json()['id']

    response = test_client.get(f'/orders/{order_id}')
    assert response.status_code == 200

def test_update_order(test_client, init_database):
    unique_email = f'john.doe{time.time()}@example.com'
    user_response = test_client.post('/users/', json={
        'name': 'John Doe',
        'email': unique_email,
        'password': 'password123'
    })
    assert user_response.status_code == 201
    user_id = user_response.get_json()['id']

    order_response = test_client.post('/orders/', json={
        'user_id': user_id,
        'order_date': '2022-01-01T00:00:00Z',
        'total_amount': 100.0
    })
    assert order_response.status_code == 201
    order_id = order_response.get_json()['id']

    update_response = test_client.put(f'/orders/{order_id}', json={
        'total_amount': 150.0
    })
    assert update_response.status_code == 200
    assert update_response.get_json()['total_amount'] == 150.0

def test_delete_order(test_client, init_database):
    unique_email = f'john.doe{time.time()}@example.com'
    user_response = test_client.post('/users/', json={
        'name': 'John Doe',
        'email': unique_email,
        'password': 'password123'
    })
    assert user_response.status_code == 201
    user_id = user_response.get_json()['id']

    order_response = test_client.post('/orders/', json={
        'user_id': user_id,
        'order_date': '2022-01-01T00:00:00Z',
        'total_amount': 100.0
    })
    assert order_response.status_code == 201
    order_id = order_response.get_json()['id']

    delete_response = test_client.delete(f'/orders/{order_id}')
    assert delete_response.status_code == 204
