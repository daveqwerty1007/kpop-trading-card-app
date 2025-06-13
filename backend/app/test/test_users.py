def test_create_user(test_client, init_database):
    response = test_client.post('/users/', json={
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    response_json = response.get_json()
    assert 'message' in response_json
    assert 'user_id' in response_json

def test_get_user(test_client, init_database):
    response = test_client.get('/users/1')
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['name'] == 'John Doe'
    assert response_json['email'] == 'john.doe@example.com'

def test_update_user(test_client, init_database):
    response = test_client.put('/users/1', json={
        'name': 'John Doe Updated',
        'email': 'john.doe.updated@example.com',
        'address': '123 Main St',
        'phone_number': '1234567890'
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['name'] == 'John Doe Updated'
    assert response_json['email'] == 'john.doe.updated@example.com'

def test_delete_user(test_client, init_database):
    # First, create a user to delete
    user_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password'
    }
    response = test_client.post('/users/', json=user_data)
    assert response.status_code == 201
    response_json = response.get_json()
    user_id = response_json['user_id']

    # Now, delete the user
    response = test_client.delete(f'/users/{user_id}')
    assert response.status_code == 204
