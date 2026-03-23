from flask import request, jsonify, abort

from geoalchemy2.shape import to_shape

from app.api.v1 import v1_bp
from app.schemas.bathroom import BathroomSchema, BathroomDetailSchema
from app.services.bathroom_service import get_nearby_bathrooms, get_bathroom_with_ratings

bathroom_schema = BathroomSchema()
bathroom_detail_schema = BathroomDetailSchema()


def _serialize_bathroom(bathroom):
    """Convert a Bathroom model to a dict with lat/lng extracted from PostGIS."""
    point = to_shape(bathroom.coordinates)
    return {
        'id': bathroom.id,
        'building_name': bathroom.building_name,
        'floor_level': bathroom.floor_level,
        'latitude': point.y,
        'longitude': point.x,
        'gender_type': bathroom.gender_type,
        'is_accessible': bathroom.is_accessible,
        'created_at': bathroom.created_at.isoformat(),
    }


@v1_bp.route('/bathrooms/nearby', methods=['GET'])
def nearby_bathrooms():
    try:
        lat = float(request.args['lat'])
        lng = float(request.args['lng'])
        radius = float(request.args.get('radius', 500))
    except (KeyError, ValueError):
        abort(400, description='lat, lng are required and must be numbers')

    bathrooms = get_nearby_bathrooms(lat, lng, radius)
    return jsonify([_serialize_bathroom(b) for b in bathrooms])


@v1_bp.route('/bathrooms/<bathroom_id>', methods=['GET'])
def get_bathroom(bathroom_id):
    bathroom, stats = get_bathroom_with_ratings(bathroom_id)
    if not bathroom:
        abort(404)

    data = _serialize_bathroom(bathroom)
    data['avg_overall_rating'] = (
        round(float(stats.avg_overall), 2) if stats.avg_overall else None
    )
    data['avg_cleanliness'] = (
        round(float(stats.avg_cleanliness), 2) if stats.avg_cleanliness else None
    )
    data['review_count'] = stats.review_count
    return jsonify(data)
