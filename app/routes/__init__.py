from fastapi import APIRouter

from app.routes.consent import router as consent_router
from app.routes.contract import router as contract_router


__all__ = ('router',)


router = APIRouter()

router.include_router(consent_router, prefix='/consents', tags=['consents'])
router.include_router(contract_router, prefix='/contracts', tags=['contracts'])
