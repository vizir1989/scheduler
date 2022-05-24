from typing import Generator

from webapp.db import async_session


async def get_db() -> Generator:
    async with async_session() as db:
        yield db
