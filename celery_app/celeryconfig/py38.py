from .base import Config as BaseConfig

WORKER = 'py38'


class Config(BaseConfig):
    task_queues = {
        f'{WORKER}': {
            'exchange': 'workflow',
            'routing_key': f'#.{WORKER}',
        }
    }
