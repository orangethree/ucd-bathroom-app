def test_my_reviews(client, auth_header, test_bathroom):
    # Create a review
    client.post(
        f'/api/v1/bathrooms/{test_bathroom.id}/reviews',
        json={
            'overall_rating': 5,
            'cleanliness': 5,
            'traffic_level': 'Empty',
            'review_text': 'Spotless!',
        },
        headers=auth_header,
    )

    resp = client.get('/api/v1/users/me/reviews', headers=auth_header)
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1
    assert data[0]['overall_rating'] == 5


def test_my_reviews_no_auth(client):
    resp = client.get('/api/v1/users/me/reviews')
    assert resp.status_code == 401
