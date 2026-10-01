import time

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
def _register(test_client, name='John Doe'):
    """Create a user and log in. Returns (user_id, headers)."""
    email = f'user.{time.time()}@example.com'
    test_client.post('/users/', json={'name': name, 'email': email, 'password': 'password123'})
    login = test_client.post('/users/login', json={'email': email, 'password': 'password123'}).get_json()
    return login['user_id'], {'Authorization': f'Bearer {login["access_token"]}'}

def test_get_user(test_client, init_database):
    user_id, headers = _register(test_client)

    response = test_client.get(f'/users/{user_id}', headers=headers)
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['name'] == 'John Doe'
    assert response_json['id'] == user_id

def test_get_other_user_forbidden(test_client, init_database):
    other_id, _ = _register(test_client)
    _, headers = _register(test_client)
    assert test_client.get(f'/users/{other_id}').status_code == 401
    assert test_client.get(f'/users/{other_id}', headers=headers).status_code == 403

def test_update_user(test_client, init_database):
    user_id, headers = _register(test_client)
    new_email = f'john.updated.{time.time()}@example.com'
    response = test_client.post('/users/update_user', json={
        'id': user_id,
        'name': 'John Doe Updated',
        'email': new_email,
    }, headers=headers)
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['name'] == 'John Doe Updated'
    assert response_json['email'] == new_email

def test_update_user_requires_login(test_client, init_database):
    user_id, _ = _register(test_client)
    response = test_client.post('/users/update_user', json={
        'id': user_id, 'name': 'x', 'email': 'x@example.com', 'role': 'admin'
    })
    assert response.status_code == 401

def test_update_user_only_changes_own_name_and_email(test_client, init_database):
    victim_id, victim_headers = _register(test_client, name='Victim')
    _, attacker_headers = _register(test_client, name='Attacker')
    response = test_client.post('/users/update_user', json={
        'id': victim_id,
        'name': 'Attacker',
        'email': f'attacker.{time.time()}@example.com',
        'role': 'admin',
        'password': 'not-a-hash',
    }, headers=attacker_headers)
    assert response.status_code == 200
    assert response.get_json()['role'] == 'user'

    victim = test_client.get(f'/users/{victim_id}', headers=victim_headers).get_json()
    assert victim['name'] == 'Victim'
    assert victim['role'] == 'user'

def test_user_listing_requires_admin(test_client, init_database, admin_headers):
    _, headers = _register(test_client)
    for path in ['/users/list', '/users/search?q=John', '/users/filter-options']:
        assert test_client.get(path).status_code == 401
        assert test_client.get(path, headers=headers).status_code == 403
    assert test_client.get('/users/list', headers=admin_headers).status_code == 200

def test_regular_user_cannot_delete_other_user(test_client, init_database, admin_headers):
    other_id, _ = _register(test_client)
    _, headers = _register(test_client)
    assert test_client.delete(f'/users/{other_id}', headers=headers).status_code == 403
    assert test_client.delete(f'/users/{other_id}', headers=admin_headers).status_code == 204

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
    assert response.status_code == 401
