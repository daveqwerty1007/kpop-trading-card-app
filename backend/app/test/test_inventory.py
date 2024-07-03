def test_create_inventory(test_client, init_database):
    # Ensure a card exists first
    card_response = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    })
    assert card_response.status_code == 201
    card_id = card_response.get_json()['id']

    # Now create inventory for the card
    response = test_client.post('/inventory/', json={
        'card_id': card_id,
        'quantity_available': 50
    })
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['card_id'] == card_id
    assert response_json['quantity_available'] == 50

def test_get_inventory(test_client, init_database):
    # Ensure a card and inventory item exist first
    card_response = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    })
    assert card_response.status_code == 201
    card_id = card_response.get_json()['id']

    inventory_response = test_client.post('/inventory/', json={
        'card_id': card_id,
        'quantity_available': 50
    })
    assert inventory_response.status_code == 201
    inventory_id = inventory_response.get_json()['id']

    # Now get the inventory item
    response = test_client.get(f'/inventory/{inventory_id}')
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['card_id'] == card_id
    assert response_json['quantity_available'] == 50

def test_update_inventory(test_client, init_database):
    # Ensure a card and inventory item exist first
    card_response = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    })
    assert card_response.status_code == 201
    card_id = card_response.get_json()['id']

    inventory_response = test_client.post('/inventory/', json={
        'card_id': card_id,
        'quantity_available': 50
    })
    assert inventory_response.status_code == 201
    inventory_id = inventory_response.get_json()['id']

    # Now update the inventory item
    response = test_client.put(f'/inventory/{inventory_id}', json={
        'quantity_available': 100
    })
    assert response.status_code == 200
    response_json = response.get_json()
    assert response_json['quantity_available'] == 100

def test_delete_inventory(test_client, init_database):
    # Ensure a card and inventory item exist first
    card_response = test_client.post('/cards/', json={
        'card_name': 'Test Card',
        'artist': 'Test Artist',
        'group': 'Test Group',
        'album': 'Test Album',
        'price': 10.0,
        'description': 'This is a test card.',
        'image_url': 'http://example.com/test.jpg'
    })
    assert card_response.status_code == 201
    card_id = card_response.get_json()['id']

    inventory_response = test_client.post('/inventory/', json={
        'card_id': card_id,
        'quantity_available': 50
    })
    assert inventory_response.status_code == 201
    inventory_id = inventory_response.get_json()['id']

    # Now delete the inventory item
    response = test_client.delete(f'/inventory/{inventory_id}')
    assert response.status_code == 204
