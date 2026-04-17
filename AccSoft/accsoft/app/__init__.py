import os
from flask import Flask
from config import config
from app.extensions import db, migrate, login_manager


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import models so Flask-Migrate can detect them
    with app.app_context():
        from app import models  # noqa: F401

    from app.blueprints.auth import auth_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.accounts import accounts_bp
    from app.blueprints.transactions import transactions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(accounts_bp)
    app.register_blueprint(transactions_bp)

    return app
