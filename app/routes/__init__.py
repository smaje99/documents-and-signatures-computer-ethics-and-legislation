from fastapi import APIRouter

from app.routes.consent import router as consent_router
from app.routes.contract import router as contract_router
from app.routes.signature import router as signature_router


__all__ = ('router',)


router = APIRouter()

router.include_router(consent_router, prefix='/consents', tags=['consents'])
router.include_router(contract_router, prefix='/contracts', tags=['contracts'])
router.include_router(signature_router, prefix='/signatures', tags=['signatures'])
