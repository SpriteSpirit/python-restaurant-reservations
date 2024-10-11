FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache, artifacts}

COPY . .

RUN apt-get update && apt-get install -y procps netcat curl && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y netcat
