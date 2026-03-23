from flask import jsonify, g

from app.api.v1 import v1_bp
from app.models.review import Review
from app.schemas.review import ReviewSchema
from app.utils.decorators import jwt_required

review_schema = ReviewSchema()


@v1_bp.route('/users/me/reviews', methods=['GET'])
@jwt_required
def my_reviews():
    reviews = (
        Review.query
        .filter_by(user_id=g.current_user_id)
        .order_by(Review.created_at.desc())
        .all()
    )
    return jsonify([review_schema.dump(r) for r in reviews])
