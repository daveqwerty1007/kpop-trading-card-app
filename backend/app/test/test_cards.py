def test_create_card(test_client, init_database, admin_headers):
    headers = admin_headers
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

def test_get_card(test_client, init_database, admin_headers):
    headers = admin_headers
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

def test_update_card(test_client, init_database, admin_headers):
    headers = admin_headers
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

def test_list_all_cards(test_client, init_database, admin_headers):
    headers = admin_headers
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

def test_delete_card(test_client, init_database, admin_headers):
    headers = admin_headers
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

def test_regular_user_cannot_modify_cards(test_client, init_database, auth_headers, admin_headers):
    card = {'card_name': 'C', 'artist': 'A', 'group': 'G', 'price': 10.0}
    assert test_client.post('/cards/', json=card, headers=auth_headers).status_code == 403

    card_id = test_client.post('/cards/', json=card, headers=admin_headers).get_json()['id']
    assert test_client.put(f'/cards/{card_id}', json={**card, 'id': card_id, 'price': 0.01},
                           headers=auth_headers).status_code == 403
    assert test_client.delete(f'/cards/{card_id}', headers=auth_headers).status_code == 403
    assert test_client.get(f'/cards/{card_id}').get_json()['price'] == 10.0
