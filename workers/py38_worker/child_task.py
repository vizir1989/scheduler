import os
from pathlib import Path

import dill as pickle

from celery_app.celeryapp import app

dir_path = os.path.dirname(os.path.realpath(__file__))


@app.task(name='scheduler.tasks.py38.run', bind=True, queue='py38')
def run(self, **kwargs):
    with open(Path(dir_path) / 'py38_task.dill', 'rb') as f:
        run = pickle.loads(f.read())
        return run(**kwargs)
