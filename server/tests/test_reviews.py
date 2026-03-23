def test_create_review(client, auth_header, test_bathroom):
    resp = client.post(
        f'/api/v1/bathrooms/{test_bathroom.id}/reviews',
        json={
            'overall_rating': 4,
            'cleanliness': 3,
            'traffic_level': 'Moderate',
            'review_text': 'Pretty clean!',
        },
        headers=auth_header,
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['overall_rating'] == 4
    assert data['cleanliness'] == 3


def test_create_review_no_auth(client, test_bathroom):
    resp = client.post(
        f'/api/v1/bathrooms/{test_bathroom.id}/reviews',
        json={
            'overall_rating': 4,
            'cleanliness': 3,
            'traffic_level': 'Moderate',
        },
    )
    assert resp.status_code == 401


def test_create_review_invalid_rating(client, auth_header, test_bathroom):
    resp = client.post(
        f'/api/v1/bathrooms/{test_bathroom.id}/reviews',
        json={
            'overall_rating': 6,
            'cleanliness': 3,
            'traffic_level': 'Moderate',
        },
        headers=auth_header,
    )
    assert resp.status_code == 422


def test_get_reviews_paginated(client, auth_header, test_bathroom):
    # Create two reviews
    for i in range(2):
        client.post(
            f'/api/v1/bathrooms/{test_bathroom.id}/reviews',
            json={
                'overall_rating': i + 1,
                'cleanliness': i + 1,
                'traffic_level': 'Empty',
            },
            headers=auth_header,
        )

    resp = client.get(
        f'/api/v1/bathrooms/{test_bathroom.id}/reviews',
        query_string={'limit': 1, 'offset': 0},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1


def test_delete_own_review(client, auth_header, test_bathroom):
    # Create a review
    resp = client.post(
        f'/api/v1/bathrooms/{test_bathroom.id}/reviews',
        json={
            'overall_rating': 3,
            'cleanliness': 3,
            'traffic_level': 'Low',
        },
        headers=auth_header,
    )
    review_id = resp.get_json()['id']

    # Delete it
    resp = client.delete(f'/api/v1/reviews/{review_id}', headers=auth_header)
    assert resp.status_code == 200


def test_delete_review_not_owner(client, auth_header, test_bathroom, test_user):
    import jwt as pyjwt
    from datetime import datetime, timedelta, timezone
    from flask import current_app
    from app.extensions import db
    from app.models.user import User

    # Create review as test_user
    resp = client.post(
        f'/api/v1/bathrooms/{test_bathroom.id}/reviews',
        json={
            'overall_rating': 3,
            'cleanliness': 3,
            'traffic_level': 'Low',
        },
        headers=auth_header,
    )
    review_id = resp.get_json()['id']

    # Create a different user and try to delete
    other_user = User(username='other', email='other@ucdavis.edu')
    db.session.add(other_user)
    db.session.commit()

    other_token = pyjwt.encode(
        {'sub': other_user.id, 'exp': datetime.now(timezone.utc) + timedelta(days=1)},
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256',
    )

    resp = client.delete(
        f'/api/v1/reviews/{review_id}',
        headers={'Authorization': f'Bearer {other_token}'},
    )
    assert resp.status_code == 403
