from datetime import datetime
from typing import Annotated, Optional, override
from uuid import UUID, uuid4

from pydantic import BaseModel, BeforeValidator, ConfigDict


__all__ = (
  'ConsentCreate',
  'ConsentOut',
  'ContractCreate',
  'ContractOut',
  'SignatureCreate',
  'SignatureOut',
  'AuditLogCreate',
  'AuditLogOut',
)


IdentifierUUID = Annotated[
  UUID, BeforeValidator(lambda v: v if isinstance(v, UUID) else UUID(v, version=4))
]


class ConsentBase(BaseModel):
  '''Base model for consent data.'''

  user: str


class ConsentCreate(ConsentBase):
  '''Model for creating a new consent.'''

  id: UUID = uuid4()  # Automatically generate a UUID for the consent


class ConsentOut(ConsentBase):
  '''Model for consent data returned by the API.'''

  id: IdentifierUUID
  timestamp: datetime

  model_config = ConfigDict(from_attributes=True)

  @override
  def __str__(self) -> str:
    return f'Consent(id={self.id}, user={self.user}, timestamp={self.timestamp})'


class ContractBase(BaseModel):
  '''Base model for contract data.'''

  content: str


class ContractCreate(ContractBase):
  '''Model for creating a new contract.'''

  id: UUID = uuid4()  # Automatically generate a UUID for the contract


class ContractOut(ContractBase):
  '''Model for contract data returned by the API.'''

  id: IdentifierUUID
  created_at: datetime
  signatures: Optional[list['SignatureOut']] = None

  model_config = ConfigDict(from_attributes=True)

  @override
  def __str__(self) -> str:
    return f'Contract(id={self.id}, content={self.content}, created_at={self.created_at})'


class SignatureBase(BaseModel):
  '''Base model for signature data.'''

  contract_id: IdentifierUUID
  signature: bytes


class SignatureCreate(SignatureBase):
  '''Model for creating a new signature.'''

  id: UUID = uuid4()  # Automatically generate a UUID for the signature
  verified: bool = False  # Default to False


class SignatureOut(SignatureBase):
  '''Model for signature data returned by the API.'''

  id: IdentifierUUID
  verified: bool
  verified_at: datetime

  model_config = ConfigDict(from_attributes=True)

  @override
  def __str__(self) -> str:
    return (
      f'Signature(id={self.id}, '
      f'contract_id={self.contract_id}, '
      f'verified={self.verified}, '
      f'verified_at={self.verified_at})'
    )


class AuditLogBase(BaseModel):
  '''Base model for audit log entries.'''

  action: str
  details: Optional[str] = None


class AuditLogCreate(AuditLogBase):
  '''Model for creating a new audit log entry.'''

  id: UUID = uuid4()  # Automatically generate a UUID for the audit log entry


class AuditLogOut(AuditLogBase):
  '''Model for audit log entries.'''

  id: IdentifierUUID
  timestamp: datetime

  model_config = ConfigDict(from_attributes=True)
