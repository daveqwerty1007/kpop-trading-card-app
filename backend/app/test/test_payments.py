def test_create_payment(test_client, init_database):
    response = test_client.post('/payments/', json={
        'order_id': 1,
        'payment_date': '2022-01-01T00:00:00Z',
        'payment_method': 'credit_card',
        'payment_status': 'Completed'
    })
    assert response.status_code == 201

def test_get_payment(test_client, init_database):
    response = test_client.get('/payments/1')
    assert response.status_code == 200
    assert b'credit_card' in response.data

def test_update_payment(test_client, init_database):
    response = test_client.put('/payments/1', json={
        'payment_status': 'Pending'
    })
    assert response.status_code == 200
    assert b'Pending' in response.data

def test_delete_payment(test_client, init_database):
    response = test_client.delete('/payments/1')
    assert response.status_code == 204
