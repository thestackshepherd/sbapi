from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Quotes(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote: Mapped[str] = mapped_column(String)
    character: Mapped[str] = mapped_column(String, nullable=True)
    film: Mapped[str] = mapped_column(String, nullable=True)
    context: Mapped[str] = mapped_column(String, nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime)
    edited: Mapped[datetime] = mapped_column(DateTime)
    url: Mapped[str] = mapped_column(String, unique=True)
