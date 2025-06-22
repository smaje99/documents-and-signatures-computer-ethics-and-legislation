from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router_v1
from app.containers import ApplicationContainer
from app.core.settings import Settings


__all__ = ('app',)

settings = Settings()  # type: ignore[call-arg]
container = ApplicationContainer()
container.config.from_dict(settings.model_dump())

app = FastAPI(
  title=container.config.project.name(),
  description=container.config.project.description(),
  version=container.config.project.version(),
  openapi_url=f'{container.config.domain.api_version()}/openapi.json',
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=[str(origin) for origin in container.config.domain.cors_origins()],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(api_router_v1, prefix=container.config.domain.api_version())
