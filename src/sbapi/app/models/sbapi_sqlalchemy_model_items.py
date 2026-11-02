from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Item(Base):
    """items database table model (The Schwartz, the ring, merchandise, ...)"""

    __tablename__ = "items"
    __table_args__ = (
        CheckConstraint("item_type IN ('weapon', 'artifact', 'tech', 'merchandise', 'other')"),
        Index("idx_items_owner_character_id", "owner_character_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_name: Mapped[str] = mapped_column(String)
    item_type: Mapped[str] = mapped_column(String)
    description: Mapped[str | None] = mapped_column(Text)
    parody_of: Mapped[str | None] = mapped_column(String)
    owner_character_id: Mapped[int | None] = mapped_column(
        ForeignKey("characters.id", ondelete="SET NULL")
    )
    image_url: Mapped[str | None] = mapped_column(String)
    source_url: Mapped[str | None] = mapped_column(String)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


    owner: Mapped[Character | None] = relationship(back_populates="items")
    trivia: Mapped[list[Trivia]] = relationship(foreign_keys="Trivia.item_id")
    citations: Mapped[list[Citation]] = relationship(foreign_keys="Citation.item_id")
