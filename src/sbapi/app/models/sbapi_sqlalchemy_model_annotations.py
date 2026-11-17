"""Annotation tables shared by every entity.

Each row points at exactly one entity: one nullable FK per entity type, with a
CHECK that exactly one is set.
"""

from sqlalchemy import CheckConstraint, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from sbapi.app.models.sbapi_sqlalchemy_model_base import Base


class EntityRefMixin:
    """Nullable FK columns shared by the annotation tables, one per entity type.

    Every annotation row points at exactly one entity; each table's CHECK
    constraint enforces that.
    """

    character_id: Mapped[int | None] = mapped_column(
        ForeignKey("characters.id", ondelete="CASCADE")
    )
    planet_id: Mapped[int | None] = mapped_column(
        ForeignKey("planets.id", ondelete="CASCADE")
    )
    vehicle_id: Mapped[int | None] = mapped_column(
        ForeignKey("vehicles.id", ondelete="CASCADE")
    )
    item_id: Mapped[int | None] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE")
    )
    actor_id: Mapped[int | None] = mapped_column(
        ForeignKey("actors.id", ondelete="CASCADE")
    )


class Trivia(EntityRefMixin, Base):
    """trivia database table model (trivia and behind-the-scenes notes)"""

    __tablename__ = "trivia"
    __table_args__ = (
        CheckConstraint("trivia_kind IN ('trivia', 'behind_the_scenes')"),
        CheckConstraint(
            "num_nonnulls(character_id, planet_id, vehicle_id, item_id, actor_id) = 1"
        ),
        Index("idx_trivia_character_id", "character_id"),
        Index("idx_trivia_planet_id", "planet_id"),
        Index("idx_trivia_vehicle_id", "vehicle_id"),
        Index("idx_trivia_item_id", "item_id"),
        Index("idx_trivia_actor_id", "actor_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    trivia_kind: Mapped[str] = mapped_column(String(2048), server_default="trivia")
    trivia_text: Mapped[str] = mapped_column(Text)


class Citation(EntityRefMixin, Base):
    """citations database table model (numbered sources backing an entity's data)"""

    __tablename__ = "citations"
    __table_args__ = (
        CheckConstraint(
            "num_nonnulls(character_id, planet_id, vehicle_id, "
            "item_id, actor_id, quote_id) = 1"
        ),
        Index("idx_citations_character_id", "character_id"),
        Index("idx_citations_planet_id", "planet_id"),
        Index("idx_citations_vehicle_id", "vehicle_id"),
        Index("idx_citations_item_id", "item_id"),
        Index("idx_citations_actor_id", "actor_id"),
        Index("idx_citations_quote_id", "quote_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    citation_number: Mapped[int] = mapped_column(Integer)
    source_text: Mapped[str] = mapped_column(Text)
    source_url: Mapped[str | None] = mapped_column(String(2048))
    quote_id: Mapped[int | None] = mapped_column(
        ForeignKey("quotes.id", ondelete="CASCADE")
    )
