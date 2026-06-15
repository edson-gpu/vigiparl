from fastapi import APIRouter

from app.api.v1 import deputies, laws

router = APIRouter(prefix="/v1")
router.include_router(deputies.router)
router.include_router(laws.router)
