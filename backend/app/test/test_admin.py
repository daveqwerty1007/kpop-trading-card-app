import time
from werkzeug.security import generate_password_hash
from app.database import db
from app.models import User


def _create_admin(email, password):
    admin = User(
        name='Admin User',
        email=email,
        password=generate_password_hash(password, method='pbkdf2:sha256'),
        role='admin'
    )
    db.session.add(admin)
    db.session.commit()
    return admin


def _admin_token(test_client, email='admin@example.com', password='adminpassword'):
    _create_admin(email, password)
    response = test_client.post('/admin/login', json={'email': email, 'password': password})
    assert response.status_code == 200
    return response.get_json()['access_token']


def test_admin_login_success(test_client):
    token = _admin_token(test_client, email='login-success@example.com')
    assert token


def test_admin_login_invalid_credentials(test_client):
    response = test_client.post('/admin/login', json={
        'email': 'nonexistent@example.com',
        'password': 'wrong'
    })
    assert response.status_code == 401


def test_admin_profile(test_client):
    token = _admin_token(test_client, email='profile@example.com')
    response = test_client.get('/admin/profile', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.get_json()['email'] == 'profile@example.com'


def test_admin_dashboard(test_client):
    token = _admin_token(test_client, email='dashboard@example.com')
    response = test_client.get('/admin/dashboard', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'user_count' in response.get_json()


def test_admin_create_user(test_client):
    token = _admin_token(test_client, email='creator@example.com')
    response = test_client.post('/admin/create_user', json={
        'name': 'New User', 'email': 'newuser@example.com', 'password': 'password123'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert 'user_id' in response.get_json()


def test_admin_update_user(test_client):
    token = _admin_token(test_client, email='updater@example.com')
    create_resp = test_client.post('/admin/create_user', json={
        'name': 'Target User', 'email': 'target@example.com', 'password': 'password123'
    }, headers={'Authorization': f'Bearer {token}'})
    user_id = create_resp.get_json()['user_id']

    response = test_client.put('/admin/update_user', json={
        'id': user_id, 'name': 'Updated Name', 'email': 'target@example.com'
    }, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200


def test_admin_delete_user(test_client):
    token = _admin_token(test_client, email='deleter@example.com')
    create_resp = test_client.post('/admin/create_user', json={
        'name': 'To Delete', 'email': 'todelete@example.com', 'password': 'password123'
    }, headers={'Authorization': f'Bearer {token}'})
    user_id = create_resp.get_json()['user_id']

    response = test_client.delete('/admin/delete_user', json={'id': user_id},
                                   headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 204


def test_admin_routes_reject_non_admin(test_client):
    register_resp = test_client.post('/users/', json={
        'name': 'Regular User', 'email': 'regular@example.com', 'password': 'password123'
    })
    assert register_resp.status_code == 201

    login_resp = test_client.post('/users/login', json={
        'email': 'regular@example.com', 'password': 'password123'
    })
    token = login_resp.get_json()['access_token']

    response = test_client.get('/admin/dashboard', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403


def test_token_signed_with_old_fallback_key_is_rejected(test_client):
    # The app used to fall back to this fixed key when SECRET_KEY was unset,
    # letting anyone mint admin tokens.
    import jwt
    now = int(time.time())
    forged = jwt.encode({'sub': '1', 'role': 'admin', 'type': 'access', 'fresh': False,
                         'jti': 'forged', 'iat': now, 'nbf': now, 'exp': now + 600},
                        'dev-only-insecure-secret-key', algorithm='HS256')
    response = test_client.get('/admin/dashboard', headers={'Authorization': f'Bearer {forged}'})
    assert response.status_code in (401, 422)


def test_admin_profile_requires_admin(test_client):
    test_client.post('/users/', json={'name': 'Plain', 'email': 'plain@example.com', 'password': 'pw'})
    token = test_client.post('/users/login', json={'email': 'plain@example.com', 'password': 'pw'}).get_json()['access_token']
    response = test_client.get('/admin/profile', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 403
