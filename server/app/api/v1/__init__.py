from flask import Blueprint

v1_bp = Blueprint('v1', __name__)

from app.api.v1 import auth, bathrooms, reviews, users  # noqa: E402, F401
