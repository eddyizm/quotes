FROM python:3.10.1-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt
COPY . .
# RUN alembic upgrade head
CMD ["uvicorn" , "main:app" , "--host", "0.0.0.0", "--port", "8000"]