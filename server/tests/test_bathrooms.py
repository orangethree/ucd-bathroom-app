def test_nearby_returns_bathrooms(client, test_bathroom):
    resp = client.get('/api/v1/bathrooms/nearby', query_string={
        'lat': 38.5395,
        'lng': -121.7490,
        'radius': 500,
    })
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) >= 1
    assert data[0]['building_name'] == 'Test Hall'


def test_nearby_missing_params(client):
    resp = client.get('/api/v1/bathrooms/nearby')
    assert resp.status_code == 400


def test_nearby_no_results_far_away(client, test_bathroom):
    resp = client.get('/api/v1/bathrooms/nearby', query_string={
        'lat': 0.0,
        'lng': 0.0,
        'radius': 100,
    })
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_bathroom_detail(client, test_bathroom):
    resp = client.get(f'/api/v1/bathrooms/{test_bathroom.id}')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['building_name'] == 'Test Hall'
    assert data['review_count'] == 0
    assert data['avg_overall_rating'] is None


def test_get_bathroom_not_found(client):
    resp = client.get('/api/v1/bathrooms/nonexistent-id')
    assert resp.status_code == 404
