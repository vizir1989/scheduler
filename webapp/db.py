from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from conf.config import settings


def create_engine() -> AsyncEngine:
    return create_async_engine(
        settings.DB_URL,
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
    )


def create_session(engine=None):
    return sessionmaker(
        bind=engine or create_engine(),
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )


engine = create_engine()
async_session = create_session(engine)
