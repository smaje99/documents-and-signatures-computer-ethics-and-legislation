from pydantic import (
  AnyHttpUrl,
  Field,
  PostgresDsn,
  SecretStr,
  ValidationInfo,
  field_validator,
)
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ('Settings',)


class PostgresSettings(BaseSettings):
  '''Settings for the PostgreSQL database connection.'''

  host: str
  port: int
  uid: str
  pwd: SecretStr
  database: str

  echo: bool

  uri: PostgresDsn | None = None

  model_config = SettingsConfigDict(extra='ignore', frozen=True)

  @field_validator('uri', mode='before')
  @classmethod
  def assemble_uri(cls, _: str, info: ValidationInfo) -> PostgresDsn:
    '''Assemble the PostgreSQL URI from the individual components.'''
    data = info.data

    password = data.get('pwd', '')
    password = (
      password.get_secret_value() if isinstance(password, SecretStr) else password
    )

    required_fields = ['host', 'port', 'uid', 'database']
    assert all(field in data for field in required_fields), (
      f'Missing required fields: {", ".join(required_fields)} and pwd in PostgresSettings'
    )

    url = MultiHostUrl.build(
      scheme='postgresql+asyncpg',
      username=data.get('uid', ''),
      password=password,
      host=data.get('host', ''),
      port=data.get('port', 5432),
      path=data.get('database', ''),
    )

    return PostgresDsn(url)


class ProjectSettings(BaseSettings):
  '''Settings for the project.'''

  name: str
  version: str
  description: str


class DomainSettings(BaseSettings):
  '''Settings for the domain.'''

  api_version: str
  server_host: str
  cors_origins: list[AnyHttpUrl]


class Settings(BaseSettings):
  '''Settings for the application.'''

  domain: DomainSettings = Field()
  postgres: PostgresSettings = Field()
  project: ProjectSettings = Field()

  model_config = SettingsConfigDict(
    env_file='.env',
    env_file_encoding='utf-8',
    env_nested_delimiter='__',
    env_prefix='',
    case_sensitive=False,
    frozen=True,
  )
