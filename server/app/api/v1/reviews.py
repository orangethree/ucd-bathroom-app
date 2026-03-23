from flask import request, jsonify, abort, g

from app.api.v1 import v1_bp
from app.extensions import db
from app.models.bathroom import Bathroom
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewSchema
from app.utils.decorators import jwt_required

review_schema = ReviewSchema()


@v1_bp.route('/bathrooms/<bathroom_id>/reviews', methods=['GET'])
def get_reviews(bathroom_id):
    bathroom = Bathroom.query.get(bathroom_id)
    if not bathroom:
        abort(404)

    limit = request.args.get('limit', 20, type=int)
    offset = request.args.get('offset', 0, type=int)

    reviews = (
        Review.query
        .filter_by(bathroom_id=bathroom_id)
        .order_by(Review.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    result = []
    for r in reviews:
        data = review_schema.dump(r)
        user = User.query.get(r.user_id)
        data['username'] = user.username if user else None
        result.append(data)

    return jsonify(result)


@v1_bp.route('/bathrooms/<bathroom_id>/reviews', methods=['POST'])
@jwt_required
def create_review(bathroom_id):
    bathroom = Bathroom.query.get(bathroom_id)
    if not bathroom:
        abort(404)

    data = request.get_json()
    errors = review_schema.validate(data)
    if errors:
        abort(422, description=errors)

    review = Review(
        user_id=g.current_user_id,
        bathroom_id=bathroom_id,
        overall_rating=data['overall_rating'],
        cleanliness=data['cleanliness'],
        traffic_level=data['traffic_level'],
        review_text=data.get('review_text'),
    )
    db.session.add(review)
    db.session.commit()

    return jsonify(review_schema.dump(review)), 201


@v1_bp.route('/reviews/<review_id>', methods=['DELETE'])
@jwt_required
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        abort(404)
    if review.user_id != g.current_user_id:
        abort(403)

    db.session.delete(review)
    db.session.commit()

    return jsonify(message='Review deleted'), 200
