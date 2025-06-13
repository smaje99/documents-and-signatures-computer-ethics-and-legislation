from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, BeforeValidator, ConfigDict


IdentifierUUID = Annotated[
  UUID,
  BeforeValidator(lambda v: v if isinstance(v, UUID) else UUID(v, version=4))
]


class ConsentBase(BaseModel):
  '''Base model for consent data.'''
  user: str


class ConsentCreate(ConsentBase):
  '''Model for creating a new consent.'''
  id: UUID = uuid4()  # Automatically generate a UUID for the consent


class Consent(ConsentBase):
  '''Model for consent data returned by the API.'''
  id: IdentifierUUID
  timestamp: datetime

  model_config = ConfigDict(from_attributes=True)


class ContractBase(BaseModel):
  '''Base model for contract data.'''
  content: str


class ContractCreate(ContractBase):
  '''Model for creating a new contract.'''
  id: UUID = uuid4()  # Automatically generate a UUID for the contract


class Contract(ContractBase):
  '''Model for contract data returned by the API.'''
  id: IdentifierUUID
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)


class SignatureBase(BaseModel):
  '''Base model for signature data.'''
  contract_id: IdentifierUUID
  signature: bytes


class SignatureCreate(SignatureBase):
  '''Model for creating a new signature.'''
  id: UUID = uuid4()  # Automatically generate a UUID for the signature
  verified: bool = False  # Default to False


class Signature(SignatureBase):
  '''Model for signature data returned by the API.'''
  id: IdentifierUUID
  verified: bool
  verified_at: datetime

  model_config = ConfigDict(from_attributes=True)


class AuditLog(BaseModel):
    '''Model for audit log entries.'''
    id: IdentifierUUID
    action: str
    details: Optional[str]
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
