def test_create_payment(test_client, init_database, create_order):
    order_id, headers = create_order
    response = test_client.post('/payments/', json={
        'order_id': order_id,
        'payment_date': '2022-01-01T00:00:00Z',
        'payment_method': 'credit_card',
        'payment_status': 'Completed'
    }, headers=headers)
    assert response.status_code == 201

def test_get_payment(test_client, init_database, create_payment):
    payment_id, headers = create_payment
    response = test_client.get(f'/payments/{payment_id}', headers=headers)
    assert response.status_code == 200

def test_update_payment(test_client, init_database, create_payment):
    payment_id, headers = create_payment
    response = test_client.put(f'/payments/{payment_id}', json={
        'payment_status': 'Pending'
    }, headers=headers)
    assert response.status_code == 200

def test_delete_payment(test_client, init_database, create_payment):
    payment_id, headers = create_payment
    response = test_client.delete(f'/payments/{payment_id}', headers=headers)
    assert response.status_code == 204
