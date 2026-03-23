from geoalchemy2.functions import ST_DWithin, ST_MakePoint, ST_Distance
from sqlalchemy import cast, func

from geoalchemy2 import Geography

from app.extensions import db
from app.models.bathroom import Bathroom
from app.models.review import Review


def get_nearby_bathrooms(lat: float, lng: float, radius_meters: float):
    """Find bathrooms within radius_meters of the given coordinates."""
    point = cast(ST_MakePoint(lng, lat), Geography)
    return Bathroom.query.filter(
        ST_DWithin(Bathroom.coordinates, point, radius_meters)
    ).order_by(
        ST_Distance(Bathroom.coordinates, point)
    ).all()


def get_bathroom_with_ratings(bathroom_id: str):
    """Get a bathroom and its aggregated review stats."""
    bathroom = Bathroom.query.get(bathroom_id)
    if not bathroom:
        return None, None

    stats = db.session.query(
        func.avg(Review.overall_rating).label('avg_overall'),
        func.avg(Review.cleanliness).label('avg_cleanliness'),
        func.count(Review.id).label('review_count'),
    ).filter(Review.bathroom_id == bathroom_id).first()

    return bathroom, stats
