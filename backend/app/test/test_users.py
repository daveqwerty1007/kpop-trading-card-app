def test_create_user(test_client, init_database):
    response = test_client.post('/users/', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201

def test_get_user(test_client, init_database):
    response = test_client.get('/users/1')
    assert response.status_code == 200
    assert b'John Doe' in response.data

def test_update_user(test_client, init_database):
    response = test_client.put('/users/1', json={
        'name': 'John Doe Updated',
        'email': 'john.doe.updated@example.com',
        'address': '123 Main St',
        'phone_number': '1234567890'
    })
    assert response.status_code == 200
    assert b'John Doe Updated' in response.data

def test_delete_user(test_client, init_database):
    response = test_client.delete('/users/1')
    assert response.status_code == 204
