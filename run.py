import uvicorn


__all__ = ('run',)


def run():
  '''Run application.'''
  uvicorn.run('app.app:app', reload=True)
