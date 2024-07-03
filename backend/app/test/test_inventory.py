def test_create_inventory(test_client, init_database):
    response = test_client.post('/inventory/', json={
        'card_id': 1,
        'quantity_available': 50
    })
    assert response.status_code == 201

def test_get_inventory(test_client, init_database):
    response = test_client.get('/inventory/1')
    assert response.status_code == 200
    assert b'50' in response.data

def test_update_inventory(test_client, init_database):
    response = test_client.put('/inventory/1', json={
        'quantity_available': 100
    })
    assert response.status_code == 200
    assert b'100' in response.data

def test_delete_inventory(test_client, init_database):
    response = test_client.delete('/inventory/1')
    assert response.status_code == 204
