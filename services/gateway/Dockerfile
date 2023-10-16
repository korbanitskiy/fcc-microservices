FROM python:3.10-slim

EXPOSE 8000
WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends --no-install-suggests \
    build-essential \
    && pip install --no-cache-dir --upgrade pip

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./src /app/

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD uvicorn gateway.app:app --host=0.0.0.0 --port=8000
