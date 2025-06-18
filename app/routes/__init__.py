from fastapi import APIRouter

from app.routes.consent import router as consent_router


__all__ = ('router',)


router = APIRouter()

router.include_router(consent_router, prefix='/consents', tags=['consents'])
