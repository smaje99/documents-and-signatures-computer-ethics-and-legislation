from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.containers import ApplicationContainer
from app.core.settings import Settings
from app.routes import router


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
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)

app.include_router(router, prefix='/api', tags=['API'])
