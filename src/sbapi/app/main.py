"""_summary_
    Entry point for SBAPI.
"""
from flask import Flask

from sbapi.app.routes.sbapi_flask_route_characters import characters_bp


def create_app() -> Flask:
    """__summary__
    creates the application entry point
    """
    app = Flask(__name__)
    app.register_blueprint(characters_bp)

    return app
