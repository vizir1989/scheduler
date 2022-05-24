FROM python:3.8.13-slim

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

RUN mkdir -p /var/log/celery && chmod -R 777 /var/log/celery

COPY . .
RUN pip install -r ./py38_requirements.txt
WORKDIR /code
