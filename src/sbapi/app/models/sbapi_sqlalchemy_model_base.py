"""Shared declarative Base for every SBAPI model."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """single metadata registry for all tables"""
    pass
