from typing import Literal

from pydantic import BaseModel

Status = Literal['ok', 'error']


class Health(BaseModel):
    db: Status
    migrations: Status
    workers: Status
