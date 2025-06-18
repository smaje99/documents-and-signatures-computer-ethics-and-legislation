from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import session
from app.models import Signature
from app.schemas import SignatureCreate, SignatureOut
from app.utils.audit import log_action


router = APIRouter()

DatabaseDependency = Annotated[AsyncSession, Depends(session)]


@router.post('/')
async def create_signature(
  signature: Annotated[SignatureCreate, Body(alias='signatureIn')],
  *,
  db: DatabaseDependency,
) -> SignatureOut:
  '''Create a new signature.'''
  signature_in = Signature(**signature.model_dump())
  db.add(signature_in)
  await db.commit()
  await db.refresh(signature_in)

  signature_out = SignatureOut.model_validate(signature_in)

  await log_action(db, 'Signature Created', str(signature_out))

  return signature_out
