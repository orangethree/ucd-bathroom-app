from datetime import datetime, timezone
from uuid import uuid4

from app.extensions import db


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    bathroom_id = db.Column(db.String(36), db.ForeignKey('bathrooms.id'), nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)
    cleanliness = db.Column(db.Integer, nullable=False)
    traffic_level = db.Column(db.String(50), nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
