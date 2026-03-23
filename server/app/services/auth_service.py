from datetime import datetime, timedelta, timezone

import jwt
from flask import current_app
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from app.extensions import db
from app.models.user import User


def verify_google_token(token: str) -> dict:
    """Verify a Google OAuth ID token and return the user info payload."""
    return id_token.verify_oauth2_token(
        token,
        google_requests.Request(),
        current_app.config['GOOGLE_CLIENT_ID'],
    )


def create_jwt(user_id: str) -> str:
    """Create a JWT session token for the given user."""
    payload = {
        'sub': user_id,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm='HS256',
    )


def login_with_google(google_id_token: str) -> tuple[User, str]:
    """Verify Google token, create or fetch user, and return (user, jwt)."""
    google_info = verify_google_token(google_id_token)
    email = google_info['email']
    name = google_info.get('name', email.split('@')[0])

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(username=name, email=email)
        db.session.add(user)
        db.session.commit()

    token = create_jwt(user.id)
    return user, token
