from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base

if TYPE_CHECKING:
    from sbapi.app.models.sbapi_sqlalchemy_model_annotations import Citation
    from sbapi.app.models.sbapi_sqlalchemy_model_characters import Character


class Quote(Base):
    """quotes database table model (lines of dialogue)"""

    __tablename__ = "quotes"
    __table_args__ = (Index("idx_quotes_character_id", "character_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote_text: Mapped[str] = mapped_column(Text)
    character_id: Mapped[int | None] = mapped_column(
        ForeignKey("characters.id", ondelete="SET NULL")
    )
    source_url: Mapped[str | None] = mapped_column(String(2048))
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    character: Mapped[Character | None] = relationship(back_populates="quotes")
    citations: Mapped[list[Citation]] = relationship(
        foreign_keys="Citation.quote_id", passive_deletes=True
    )
