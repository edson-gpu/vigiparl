from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Deputy

router = APIRouter(prefix="/deputies", tags=["deputies"])


@router.get("/")
def list_deputies(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=200),
    groupe: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Deputy)
    if q:
        query = query.filter(
            (Deputy.nom.ilike(f"%{q}%")) | (Deputy.prenom.ilike(f"%{q}%"))
        )
    if groupe:
        query = query.join(Deputy.party).filter_by(sigle=groupe)
    total = query.count()
    deputies = query.order_by(Deputy.nom).offset((page - 1) * size).limit(size).all()
    return {"total": total, "page": page, "size": size, "items": [_serialize(d) for d in deputies]}


@router.get("/{deputy_id}")
def get_deputy(deputy_id: UUID, db: Session = Depends(get_db)):
    deputy = db.query(Deputy).filter(Deputy.id == deputy_id).first()
    if not deputy:
        raise HTTPException(status_code=404, detail="Député non trouvé")
    return _serialize(deputy)


def _serialize(d: Deputy) -> dict:
    return {
        "id": str(d.id),
        "an_id": d.an_id,
        "nom": d.nom,
        "prenom": d.prenom,
        "circonscription": d.circonscription,
        "departement": d.departement,
        "photo_url": d.photo_url,
        "score_presence": float(d.score_presence) if d.score_presence else None,
        "score_coherence": float(d.score_coherence) if d.score_coherence else None,
        "parti": {"sigle": d.party.sigle, "nom": d.party.nom, "couleur": d.party.couleur} if d.party else None,
    }
