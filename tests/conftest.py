import pytest
from src.main import app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def client():
    with TestClient(app) as c:
        yield c

# TODO create temp db and seed.
# @pytest.fixture()
# def seed_quotes(construct_db):
#     with engine.connect() as conn:
#         conn.execute('''
#             INSERT INTO quotes (id, quote, author, category, date_added)
#             VALUES
#                 (1029, 'The only way to do great work is to love what you do.', 'Steve Jobs', 'motivation', '2024-09-02'),
#                 (1030, 'Live life to the fullest and focus on the positive.', 'Unknown', 'inspiration', '2024-09-02'),
#                 (1031, 'The greatest glory in living lies not in never falling, but in rising every time we fall.', 'Nelson Mandela', 'encouragement', '2024-09-02'),
#                 (1032, "Believe you can and you're halfway there.", 'Theodore Roosevelt', 'belief', '2024-09-02');
#         ''')


# @pytest.fixture()
# def construct_db():
#     print('creating schema...')
#     metadata.create_all(engine)


# def clean_up():
#     # remove db
#     pass
