from flask import Flask
from flask_cors import CORS

from app.extensions import db, migrate
from app.api import register_blueprints
from app.utils.errors import register_error_handlers
from config import config


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Blueprints
    register_blueprints(app)

    # Error handlers
    register_error_handlers(app)

    # CLI commands
    register_cli(app)

    # Import models so Alembic sees them
    from app import models  # noqa: F401

    return app


def register_cli(app):
    @app.cli.command('seed')
    def seed_command():
        """Seed the database with UC Davis bathroom data."""
        from seeds.seed_bathrooms import run_seed
        run_seed()
        print('Database seeded.')
