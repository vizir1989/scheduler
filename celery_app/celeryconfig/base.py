class Config:
    worker_prefetch_multiplier = 1
    task_track_started = True
    accept_content = ['json', 'pickle']
    task_serializer = 'pickle'

    imports = (
        'workers.py36_worker.child_task',
        'workers.py38_worker.child_task',
    )

    database_table_schemas = {
        'task': 'scheduler',
        'group': 'scheduler',
    }
