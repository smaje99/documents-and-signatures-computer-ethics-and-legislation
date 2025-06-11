from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


__all__ = ('app',)


app = FastAPI(
  title='Microservicio Deontología Informática',
  description='Prototipo para la actividad de refuerzo',
  version='0.1.0'
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)
