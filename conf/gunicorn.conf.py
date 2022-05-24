import os
import shutil
import tempfile

from conf.config import settings

bind = f'{settings.BIND_IP}:{settings.BIND_PORT}'
worker_class = 'uvicorn.workers.UvicornWorker'
workers = settings.WEB_CONCURRENCY
proc_name = 'web'
wsgi_app = 'webapp.main:create_app'
logger_class = 'webapp.logger.UniformLogger'

prom_path = '{}/scheduler-prometheus'.format(tempfile.gettempdir())
raw_env = [f'prometheus_multiproc_dir={prom_path}']


def when_ready(server):
    os.makedirs(prom_path, exist_ok=True)


def post_fork(server, worker):
    from webapp import metrics

    metrics.register()


def child_exit(server, worker):
    from prometheus_client import multiprocess as prom_mp

    prom_mp.mark_process_dead(worker.pid, prom_path)


def on_exit(server):
    shutil.rmtree(prom_path)
