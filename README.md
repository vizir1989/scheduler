# Task for Behavox

## Description
Scheduler for Behavox based on FastAPI + Celery + Docker.

## Running project
``` shell
docker-compose up -d
curl 127.0.0.1:8081/health_checker
```


## Settings
See `conf/env.example` for available options.

## Examples

### Add task
Request:
```shell
curl -X 'POST' \
  'http://localhost:8081/v0/tasks?worker_name=py36&x=4&y=4' \
  -H 'accept: application/json' \
  -d ''
```
Response:
```json
{
  "version": "0.1.0",
  "data": {
    "task_uuid": "858bc5a7-bd9d-4715-9dd8-01b705b170be"
  }
}
```

### Status
Request:
```shell
curl -X 'POST' \
  'http://localhost:8081/v0/tasks/858bc5a7-bd9d-4715-9dd8-01b705b170be/status' \
  -H 'accept: application/json' \
  -d ''
```
Response:
```json
{
  "version": "0.1.0",
  "data": {
    "task_uuid": "858bc5a7-bd9d-4715-9dd8-01b705b170be",
    "status": "DONE"
  }
}
```

### Result
Request:
```shell
curl -X 'POST' \
  'http://localhost:8081/v0/tasks/858bc5a7-bd9d-4715-9dd8-01b705b170be/result' \
  -H 'accept: application/json' \
  -d ''
```
Response:
```json
{
  "version": "0.1.0",
  "data": {
    "task_uuid": "858bc5a7-bd9d-4715-9dd8-01b705b170be",
    "result": "17.38629436111989",
    "log": null
  }
}
```

### Health checker
Request:
```shell
curl -X 'GET' \
  'http://localhost:8081/health_checker' \
  -H 'accept: application/json'
```
Response:
```json
{
  "db": "ok",
  "migrations": "ok",
  "workers": "ok"
}
```

### Addition endpoints

1. http://localhost:8081/metrics - Metrics for graphana
2. http://localhost:8081/docs - Swagger

## Services

### Flower
Address: http://localhost:5555

### Rabbitmq
Address: http://localhost:15672


## Additional Information

I've added alembic and empty db models for future using. 

I've also added scripts/cicd/test.py and folder tests for tests, but unfortunately I didn't have enough time for this.
