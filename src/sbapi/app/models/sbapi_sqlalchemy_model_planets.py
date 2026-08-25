from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer
from typing import List, Optional


class Base(DeclarativeBase):
    """_summary_
    
    """
    pass


class Planets(Base):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[String] = mapped_column(String, primary_key=False)
    ruler: Mapped[String] = mapped_column(String, primary_key=False)
    affiliation: Mapped[String] = mapped_column(String, primary_key=False)
    residents: Mapped[String] = mapped_column(String, )
    films: Mapped[String] = mapped_column(String)
    parody_of: Mapped[String] = mapped_column(String, ForeignKey=True)