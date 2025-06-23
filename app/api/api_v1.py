from fastapi import APIRouter

from app.context.users.infrastructure.http.api_v1 import user_router


__all__ = ('api_router',)


api_router = APIRouter()

api_router.include_router(user_router, prefix='/users', tags=['Users'])
