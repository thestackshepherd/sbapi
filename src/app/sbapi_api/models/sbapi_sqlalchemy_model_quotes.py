from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.sbapi_api.models.sbapi_sqlalchemy_model_base import Base


class Quote(Base):
    """quotes database table model (lines of dialogue)"""

    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quote_text: Mapped[str] = mapped_column(Text)
    character_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("characters.id", ondelete="SET NULL"), index=True
    )
    media_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("media.id", ondelete="SET NULL"), index=True
    )
    episode_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("episodes.id", ondelete="SET NULL"), index=True
    )
    source_url: Mapped[Optional[str]] = mapped_column(String)
    last_updated: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    character: Mapped[Optional["Character"]] = relationship(back_populates="quotes")
    media: Mapped[Optional["Media"]] = relationship()
    episode: Mapped[Optional["Episode"]] = relationship()
    citations: Mapped[list["Citation"]] = relationship(foreign_keys="Citation.quote_id")
