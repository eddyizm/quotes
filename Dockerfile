FROM python:3.10.13-alpine3.18
WORKDIR /usr/src/app
COPY . .
RUN apk update \
    && apk add libpq-dev gcc musl-dev \
    && pip install psycopg2
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn" , "src.main:app" , "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--workers", "3", "--log-level", "debug", "--timeout-keep-alive", "300"]
