from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    BIND_IP: str = '0.0.0.0'
    BIND_PORT: int = 8081
    WEB_CONCURRENCY: int = 1

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 5
    DB_ECHO: bool = False
    DB_URL: str

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    ALEMBIC_MIGRATION_VERSION_TABLE: str

    WORKERS_NAME: List[str] = []

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    CELERY_TIMEOUT: int
    CELERY_TASK_LIMIT: int

    @validator('BACKEND_CORS_ORIGINS', pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        return cls.__assemle_list(v)

    @validator('WORKERS_NAME', pre=True)
    def assemble_workers_name(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        return cls.__assemle_list(v)

    @staticmethod
    def __assemle_list(v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith('['):
            return [i.strip() for i in v.split(',')]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


settings = Settings()
