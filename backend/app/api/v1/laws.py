from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Law

router = APIRouter(prefix="/laws", tags=["laws"])


@router.get("/")
def list_laws(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    statut: str | None = None,
    tag: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Law)
    if statut:
        query = query.filter(Law.statut == statut)
    if tag:
        query = query.filter(Law.tags.any(tag))
    total = query.count()
    laws = query.order_by(Law.date_vote.desc()).offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": [_serialize(l) for l in laws]}


@router.get("/{law_id}")
def get_law(law_id: UUID, db: Session = Depends(get_db)):
    law = db.query(Law).filter(Law.id == law_id).first()
    if not law:
        raise HTTPException(status_code=404, detail="Loi non trouvée")
    return _serialize(law)


def _serialize(law: Law) -> dict:
    return {
        "id": str(law.id),
        "an_ref": law.an_ref,
        "titre": law.titre,
        "type": law.type,
        "statut": law.statut,
        "date_vote": law.date_vote.isoformat() if law.date_vote else None,
        "resume_ai": law.resume_ai,
        "impact_citoyen": law.impact_citoyen,
        "tags": law.tags or [],
        "pour_count": law.pour_count,
        "contre_count": law.contre_count,
        "abstention_count": law.abstention_count,
    }
