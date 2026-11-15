"""_summary_
Entry point for SBAPI.
"""

from flask import Flask, jsonify
from sqlalchemy import text

from sbapi.app.database.connection import SbapiDbConnection
from sbapi.app.routes.sbapi_flask_route_characters import characters_bp


def create_app() -> Flask:
    """__summary__
    creates the application entry point
    """
    app = Flask(__name__)
    app.extensions["sbapidb_connection"] = SbapiDbConnection()
    app.register_blueprint(characters_bp)

    @app.get("/health")
    def health():
        with app.extensions["sbapidb_connection"].get_session() as session:
            session.execute(text("SELECT 1"))
        return jsonify({"status": "ok"})

    return app
