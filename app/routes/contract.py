from typing import Annotated

from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import session
from app.models import Contract
from app.schemas import ContractCreate, ContractOut
from app.utils.audit import log_action


__all__ = ('router',)


router = APIRouter()

DatabaseDependency = Annotated[AsyncSession, Depends(session)]


@router.post('/')
async def create_contract(
  contract: Annotated[ContractCreate, Body(alias='contractIn')],
  *,
  db: DatabaseDependency,
) -> ContractOut:
    '''Create a new contract.'''
    contract_in = Contract(**contract.model_dump())
    db.add(contract_in)
    await db.commit()
    await db.refresh(contract_in)

    contract_out = ContractOut.model_validate(contract_in)

    await log_action(db, 'Contract Created', str(contract_out))

    return contract_out
