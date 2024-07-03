def test_create_admin(test_client, init_database):
    response = test_client.post('/admin/', json={
        'name': 'Admin User',
        'email': 'admin@example.com',
        'password': 'adminpassword'
    })
    assert response.status_code == 201

def test_get_admin(test_client, init_database):
    response = test_client.get('/admin/1')
    assert response.status_code == 200
    assert b'Admin User' in response.data

def test_update_admin(test_client, init_database):
    response = test_client.put('/admin/1', json={
        'name': 'Updated Admin',
        'email': 'admin.updated@example.com'
    })
    assert response.status_code == 200
    assert b'Updated Admin' in response.data

def test_delete_admin(test_client, init_database):
    response = test_client.delete('/admin/1')
    assert response.status_code == 204
