FROM python:3.11-slim

EXPOSE 8000
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    && pip install --no-cache-dir --upgrade pip

RUN pip install poetry==1.6.1
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app
RUN poetry install --no-interaction --no-root --no-cache

COPY services/gateway/src /app/

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD uvicorn gateway.app:app --host=0.0.0.0 --port=8000
