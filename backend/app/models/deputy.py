import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Party(Base):
    __tablename__ = "parties"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    an_id: Mapped[str] = mapped_column(String(50), unique=True)
    nom: Mapped[str] = mapped_column(String(200))
    sigle: Mapped[str] = mapped_column(String(20))
    couleur: Mapped[str | None] = mapped_column(String(7))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    deputies: Mapped[list["Deputy"]] = relationship(back_populates="party")


class Deputy(Base):
    __tablename__ = "deputies"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    an_id: Mapped[str] = mapped_column(String(50), unique=True)
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(100))
    party_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("parties.id"))
    circonscription: Mapped[str | None] = mapped_column(String(200))
    departement: Mapped[str | None] = mapped_column(String(100))
    mandat_debut: Mapped[date | None] = mapped_column(Date)
    mandat_fin: Mapped[date | None] = mapped_column(Date)
    photo_url: Mapped[str | None] = mapped_column(String(500))
    score_presence: Mapped[float | None] = mapped_column(Numeric(5, 2))
    score_coherence: Mapped[float | None] = mapped_column(Numeric(5, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    party: Mapped["Party | None"] = relationship(back_populates="deputies")
    votes: Mapped[list["Vote"]] = relationship(back_populates="deputy")  # type: ignore[name-defined]
