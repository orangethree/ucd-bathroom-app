import pytest
import jwt as pyjwt
from datetime import datetime, timedelta, timezone

from app import create_app
from app.extensions import db as _db
from app.models.user import User
from app.models.bathroom import Bathroom


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(autouse=True)
def db_session(app):
    """Wrap each test in a transaction that rolls back."""
    with app.app_context():
        connection = _db.engine.connect()
        transaction = connection.begin()

        session = _db.session
        old_bind = session.get_bind()

        yield session

        transaction.rollback()
        connection.close()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_user(app):
    user = User(username='testuser', email='test@ucdavis.edu')
    _db.session.add(user)
    _db.session.commit()
    return user


@pytest.fixture
def auth_header(app, test_user):
    token = pyjwt.encode(
        {
            'sub': test_user.id,
            'exp': datetime.now(timezone.utc) + timedelta(days=1),
        },
        app.config['JWT_SECRET_KEY'],
        algorithm='HS256',
    )
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def test_bathroom(app):
    bathroom = Bathroom(
        building_name='Test Hall',
        floor_level='1st Floor',
        coordinates='SRID=4326;POINT(-121.7490 38.5395)',
        gender_type='Gender-Neutral',
        is_accessible=True,
    )
    _db.session.add(bathroom)
    _db.session.commit()
    return bathroom
