from unittest.mock import patch


def test_login_creates_new_user(client):
    mock_payload = {
        'email': 'newuser@ucdavis.edu',
        'name': 'New User',
    }
    with patch('app.services.auth_service.verify_google_token', return_value=mock_payload):
        resp = client.post('/api/v1/auth/login', json={
            'google_id_token': 'fake-token',
        })

    assert resp.status_code == 200
    data = resp.get_json()
    assert 'token' in data
    assert data['user']['email'] == 'newuser@ucdavis.edu'
    assert data['user']['username'] == 'New User'


def test_login_returns_existing_user(client, test_user):
    mock_payload = {
        'email': test_user.email,
        'name': test_user.username,
    }
    with patch('app.services.auth_service.verify_google_token', return_value=mock_payload):
        resp = client.post('/api/v1/auth/login', json={
            'google_id_token': 'fake-token',
        })

    assert resp.status_code == 200
    data = resp.get_json()
    assert data['user']['id'] == test_user.id


def test_login_invalid_token(client):
    with patch('app.services.auth_service.verify_google_token', side_effect=ValueError('bad token')):
        resp = client.post('/api/v1/auth/login', json={
            'google_id_token': 'bad-token',
        })

    assert resp.status_code == 401


def test_login_missing_token(client):
    resp = client.post('/api/v1/auth/login', json={})
    assert resp.status_code == 400
