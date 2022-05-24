from workers.py36_worker.child_task import run as py36_run
from workers.py38_worker.child_task import run as py38_run

WORKERS = {
    'py36': py36_run,
    'py38': py38_run,
}
