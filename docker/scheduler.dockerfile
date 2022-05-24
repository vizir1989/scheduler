FROM python:3.10-slim

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code

RUN mkdir -p /var/log/celery && chmod -R 777 /var/log/celery

WORKDIR /code

RUN apt-get update && \
    apt-get -y install netcat dnsutils tcpdump nmap && \
    apt-get clean

COPY pyproject.toml poetry.lock /code/

RUN python -m pip install --upgrade pip
RUN pip install poetry==1.1.11

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

COPY . .

RUN chown -R 1001:0 /code

USER 1001

