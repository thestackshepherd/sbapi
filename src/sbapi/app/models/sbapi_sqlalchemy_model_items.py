from datetime import datetime
from typing import Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class Item(Base):
    """items database table model (The Schwartz, the ring, merchandise, ...)"""

    __tablename__ = "items"
    __table_args__ = (
        CheckConstraint("item_type IN ('weapon', 'artifact', 'tech', 'merchandise', 'other')"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item_name: Mapped[str] = mapped_column(String)
    item_type: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    parody_of: Mapped[Optional[str]] = mapped_column(String)
    owner_character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("characters.id", ondelete="SET NULL"), index=True
    )
    image_url: Mapped[Optional[str]] = mapped_column(String)
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    owner: Mapped[Optional["Character"]] = relationship(back_populates="items")
    trivia: Mapped[list["Trivia"]] = relationship(foreign_keys="Trivia.item_id")
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.item_id")
