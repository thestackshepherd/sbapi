from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Quote(Base):
    """quotes database table model (lines of dialogue)"""

    __tablename__ = "quotes"
    __table_args__ = (Index("idx_quotes_character_id", "character_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote_text: Mapped[str] = mapped_column(Text)
    character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("characters.id", ondelete="SET NULL")
    )
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    character: Mapped[Optional["Character"]] = relationship(back_populates="quotes")
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.quote_id")
