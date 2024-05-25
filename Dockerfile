FROM python:3.10.13-alpine3.18
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apk update \
    && apk add libpq-dev gcc musl-dev \
    && pip install psycopg2
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
COPY ./src . 
CMD ["uvicorn" , "main:app" , "--proxy-headers", "--host", "0.0.0.0", "--port", "8000", "--workers", "3", "--timeout-keep-alive", "300"]
# CMD ["uvicorn", "app:app", "--proxy-headers","--host", "0.0.0.0", "--port", "5000","--workers", "3", "--timeout-keep-alive", "300"]