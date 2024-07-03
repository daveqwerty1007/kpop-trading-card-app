def test_create_order(test_client, init_database):
    response = test_client.post('/orders/', json={
        'user_id': 1,
        'order_date': '2022-01-01T00:00:00Z',
        'total_amount': 100.0
    })
    assert response.status_code == 201

def test_get_order(test_client, init_database):
    response = test_client.get('/orders/1')
    assert response.status_code == 200
    assert b'100.0' in response.data

def test_update_order(test_client, init_database):
    response = test_client.put('/orders/1', json={
        'total_amount': 150.0
    })
    assert response.status_code == 200
    assert b'150.0' in response.data

def test_delete_order(test_client, init_database):
    response = test_client.delete('/orders/1')
    assert response.status_code == 204
