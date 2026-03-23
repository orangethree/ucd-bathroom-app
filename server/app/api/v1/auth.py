from flask import request, jsonify, abort

from app.api.v1 import v1_bp
from app.schemas.auth import LoginRequestSchema
from app.schemas.user import UserSchema
from app.services.auth_service import login_with_google

login_schema = LoginRequestSchema()
user_schema = UserSchema()


@v1_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    if errors:
        abort(400, description=errors)

    try:
        user, token = login_with_google(data['google_id_token'])
    except ValueError:
        abort(401)

    return jsonify(token=token, user=user_schema.dump(user))
