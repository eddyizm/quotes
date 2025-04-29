FROM python:3.11-alpine
WORKDIR /usr/src/app
COPY . .
RUN apk update \
    && apk add libpq-dev gcc musl-dev cmake libffi \
    && apk add --no-cache g++ python3-dev py3-pip openblas-dev \
    && pip install psycopg2
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
CMD ["granian", \
    "--interface", "asgi", \
    "src.main:app" , \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--workers", "1", \
    "--log-level", "info", \
    "--backlog", "1024", \
    "--no-access-log", \
    "--http2-keep-alive-timeout", "30" ]
