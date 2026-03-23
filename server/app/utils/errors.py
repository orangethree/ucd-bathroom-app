from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(error=str(e.description), status=400), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify(error='Unauthorized', status=401), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify(error='Forbidden', status=403), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error='Not found', status=404), 404

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify(error=str(e.description), status=422), 422

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify(error='Internal server error', status=500), 500
