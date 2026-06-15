import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    law_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("laws.id"))
    deputy_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("deputies.id"))
    party_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("parties.id"))
    position: Mapped[str] = mapped_column(
        Enum("pour", "contre", "abstention", "absent", "non_votant", name="vote_position")
    )
    session_date: Mapped[date | None] = mapped_column(Date)
    scrutin_numero: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    law: Mapped["Law"] = relationship(back_populates="votes")  # type: ignore[name-defined]
    deputy: Mapped["Deputy"] = relationship(back_populates="votes")  # type: ignore[name-defined]
