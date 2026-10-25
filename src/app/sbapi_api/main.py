"""_summary_
    Entry point for SBAPI.
"""
from flask import Flask, jsonify
from sqlalchemy import text

from app.sbapi_api.database.connection import SessionLocal
from app.sbapi_api.routes.sbapi_flask_route_characters import characters_bp


def create_app() -> Flask:
    """__summary__
    creates the application entry point
    """
    app = Flask(__name__)
    app.register_blueprint(characters_bp)

    @app.get("/health")
    def health():
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
        return jsonify({"status": "ok"})

    return app
