from functools import wraps

import jwt
from flask import request, g, current_app, abort


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            abort(401)

        token = auth_header[7:]
        try:
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=['HS256'],
            )
            g.current_user_id = payload['sub']
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            abort(401)

        return f(*args, **kwargs)
    return decorated
