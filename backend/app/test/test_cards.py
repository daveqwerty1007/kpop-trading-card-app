import time


def _auth_headers(test_client):
    unique_email = f'card.tester.{time.time()}@example.com'
    test_client.post('/users/', json={
        'name': 'Card Tester',
        'email': unique_email,
        'password': 'password123'
    })
    login_resp = test_client.post('/users/login', json={
        'email': unique_email,
        'password': 'password123'
    })
    token = login_resp.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_create_card(test_client, init_database):
    headers = _auth_headers(test_client)
    response = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    }, headers=headers)
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_get_card(test_client, init_database):
    headers = _auth_headers(test_client)
    create_resp = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    }, headers=headers)
    card_id = create_resp.get_json()['id']

    response = test_client.get(f'/cards/{card_id}')
    assert response.status_code == 200
    assert b'Test Card' in response.data

def test_update_card(test_client, init_database):
    headers = _auth_headers(test_client)
    create_resp = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    }, headers=headers)
    card_id = create_resp.get_json()['id']

    response = test_client.put(f'/cards/{card_id}', json={
        'id': card_id,
        'card_name': 'Test Card Updated',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 15.0,
        'description': 'This is an updated test card.',
        'image_url': 'http://example.com/test.jpg'
    }, headers=headers)
    assert response.status_code == 200
    assert b'Test Card Updated' in response.data

def test_list_all_cards(test_client, init_database):
    headers = _auth_headers(test_client)
    create_resp = test_client.post('/cards/', json={
        'card_name': 'Listable Card',
        'artist': 'List Artist',
        'group': 'List Group',
        'album': 'List Album',
        'price': 20.0,
        'description': 'A card that should show up in the list.',
        'image_url': 'http://example.com/list.jpg'
    }, headers=headers)
    card_id = create_resp.get_json()['id']

    response = test_client.get('/cards/list')
    assert response.status_code == 200
    matching = [c for c in response.json if c['id'] == card_id]
    assert len(matching) == 1
    assert matching[0]['card_name'] == 'Listable Card'

def test_delete_card(test_client, init_database):
    headers = _auth_headers(test_client)
    create_resp = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    }, headers=headers)
    card_id = create_resp.get_json()['id']

    response = test_client.delete(f'/cards/{card_id}', headers=headers)
    assert response.status_code == 204
