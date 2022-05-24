from enum import Enum

from celery import states


class StatusType(str, Enum):
    NOT_RUN = 'NOT RUN YET'
    IN_FLIGHT = 'IN FLIGHT'
    FAILED = 'FAILED'
    DONE = 'DONE'


STATUS_MAP = {
    states.PENDING: StatusType.NOT_RUN,
    states.STARTED: StatusType.IN_FLIGHT,
    states.RETRY: StatusType.IN_FLIGHT,
    states.SUCCESS: StatusType.DONE,
    states.FAILURE: StatusType.FAILED,
    states.REVOKED: StatusType.FAILED,
}
