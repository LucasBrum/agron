"""Adapter de banco: implementa o port FieldRepository com SQLAlchemy."""
from collections.abc import Iterator
from datetime import date
from uuid import UUID

from sqlalchemy import Date, Float, String, Uuid, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from agron.domain.models import Field

DATABASE_URL = "sqlite:///./agron.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class FieldRow(Base):
    __tablename__ = "fields"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    crop: Mapped[str] = mapped_column(String(50))
    area_ha: Mapped[float] = mapped_column(Float)
    planting_date: Mapped[date] = mapped_column(Date)


def get_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


class SqlAlchemyFieldRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, field: Field) -> Field:
        self.session.add(
            FieldRow(
                id=field.id,
                name=field.name,
                crop=field.crop,
                area_ha=field.area_ha,
                planting_date=field.planting_date,
            )
        )
        self.session.commit()
        return field

    def get(self, field_id: UUID) -> Field | None:
        row = self.session.get(FieldRow, field_id)
        if row is None:
            return None
        return Field(row.name, row.crop, row.area_ha, row.planting_date, row.id)