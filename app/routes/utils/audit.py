from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AuditLog
from app.schemas import AuditLogCreate


async def log_action(db: AsyncSession, action: str, detail: str) -> None:
  '''Log an action in the audit log.'''
  log_entry = AuditLogCreate(action=action, details=detail)
  db.add(AuditLog(**log_entry.model_dump()))
  await db.commit()
