import os
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.core.schema.dal import connect_to_db

# connect_args={"check_same_thread": False}
# TEST_DB_URL=sqlite:///./tests/test.db
os['TEST_DB_URL'] = 'sqlite:///./tests/test.db'
client = TestClient(app)


# open api calls
# def test_daily_quote():
#     response = client.post("/api/v1/daily/")
#     assert response.status_code == 200


# def test_random_quote():
#     response = client.post("/api/v1/random/")
#     assert response.status_code == 200
#     assert len(response.json().get('quote')) > 0


def test_daily_quote_get():
    response = client.get("/api/v1/daily/")
    assert response.status_code == 405


def test_daily_quote_put():
    response = client.put("/api/v1/daily/")
    assert response.status_code == 405
