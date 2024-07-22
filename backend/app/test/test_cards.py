def test_create_card(test_client, init_database):
    response = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    })
    assert response.status_code == 201

def test_get_card(test_client, init_database):
    response = test_client.get('/cards/1')
    assert response.status_code == 200
    assert b'Test Card' in response.data

def test_update_card(test_client, init_database):
    response = test_client.put('/cards/1', json={
        'card_name': 'Test Card Updated',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 15.0,
        'description': 'This is an updated test card.',
        'image_url': 'http://example.com/test.jpg'
    })
    assert response.status_code == 200
    assert b'Test Card Updated' in response.data

def test_list_all_cards(test_client, init_database):
    response = test_client.get('/cards/')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['card_name'] == "Test Card Updated"
    assert response.json[0]['artist'] == "Test Artist"
    assert response.json[0]['group'] == "Test Group"
    assert response.json[0]['album'] == "Test Album"
    assert response.json[0]['price'] == 15.0
    assert response.json[0]['description'] == "This is an updated test card."
    assert response.json[0]['image_url'] == "http://example.com/test.jpg"

def test_delete_card(test_client, init_database):
    response = test_client.delete('/cards/1')
    assert response.status_code == 204
