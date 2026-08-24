"""_summary_
    Entry point for SBAPI.
"""
from flask import Flask


def create_app() -> Flask:
    """__summary__
    creates the application entry point
    """
    app = Flask(__name__)

    return app
