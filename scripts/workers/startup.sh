#!/bin/bash

set -o nounset
set -o pipefail
set -o errexit

worker_name=$1
concurrency=$2

celery_worker() {
    log_file="/var/log/celery/${1}.log"
    touch "$log_file"
    WORKER_TYPE="${1}" celery \
      --app celery_app.celeryapp \
      worker \
      --loglevel INFO \
      --task-events \
      --hostname "${1}"@%h \
      --queues "${1}" \
      --concurrency "${2}" \
      --pidfile="/tmp/${1}" &> $log_file &
}

celery_worker "$worker_name" "$concurrency"

tail -f /var/log/celery/*.log
