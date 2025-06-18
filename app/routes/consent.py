from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import session
from app.models import Consent
from app.schemas import ConsentCreate, ConsentOut
from app.utils.audit import log_action


__all__ = ('router',)


router = APIRouter()

DatabaseDependency = Annotated[AsyncSession, Depends(session)]


@router.post('/')
async def create_consent(consent: ConsentCreate, db: DatabaseDependency) -> ConsentOut:
  '''Create a new consent.'''
  consent_in = Consent(**consent.model_dump())
  db.add(consent_in)
  await db.commit()
  await db.refresh(consent_in)
  await log_action(db, 'Consent Created', str(consent_in))

  return ConsentOut.model_validate(consent_in)
