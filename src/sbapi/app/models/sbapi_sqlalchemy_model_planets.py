from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Planets(Base):
    __tablename__ = 'planets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)