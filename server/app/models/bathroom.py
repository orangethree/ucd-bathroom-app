from datetime import datetime, timezone
from uuid import uuid4

from geoalchemy2 import Geography

from app.extensions import db


class Bathroom(db.Model):
    __tablename__ = 'bathrooms'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    building_name = db.Column(db.String(100), nullable=False)
    floor_level = db.Column(db.String(20), nullable=False)
    coordinates = db.Column(
        Geography(geometry_type='POINT', srid=4326), nullable=False
    )
    gender_type = db.Column(db.String(50), nullable=False)
    is_accessible = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    reviews = db.relationship('Review', backref='bathroom', lazy='dynamic')
