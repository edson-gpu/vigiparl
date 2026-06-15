import uuid
from datetime import date, datetime

from sqlalchemy import ARRAY, DateTime, Enum, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Law(Base):
    __tablename__ = "laws"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    an_ref: Mapped[str] = mapped_column(String(100), unique=True)
    titre: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Enum("PLF", "PJL", "PPL", "ORD", "AUTRE", name="law_type"), default="AUTRE")
    statut: Mapped[str] = mapped_column(
        Enum("en_discussion", "votee", "rejetee", "en_attente", name="law_status"),
        default="en_attente",
    )
    date_depot: Mapped[date | None]
    date_vote: Mapped[date | None]
    texte_complet: Mapped[str | None] = mapped_column(Text)
    resume_ai: Mapped[str | None] = mapped_column(Text)
    impact_citoyen: Mapped[str | None] = mapped_column(Text)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    pour_count: Mapped[int] = mapped_column(Integer, default=0)
    contre_count: Mapped[int] = mapped_column(Integer, default=0)
    abstention_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    votes: Mapped[list["Vote"]] = relationship(back_populates="law")  # type: ignore[name-defined]
    ai_summary: Mapped["AiSummary | None"] = relationship(back_populates="law", uselist=False)


class AiSummary(Base):
    __tablename__ = "ai_summaries"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    law_id: Mapped[uuid.UUID] = mapped_column(unique=True)
    resume: Mapped[str] = mapped_column(Text)
    impact_citoyen: Mapped[str] = mapped_column(Text)
    tags: Mapped[list[str]] = mapped_column(ARRAY(String))
    model_version: Mapped[str] = mapped_column(String(50))
    prompt_version: Mapped[str] = mapped_column(String(20))
    token_count: Mapped[int] = mapped_column(Integer)
    source_hash: Mapped[str] = mapped_column(String(64))
    generated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    law: Mapped["Law"] = relationship(back_populates="ai_summary")
