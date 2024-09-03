# api tests on live db.
def test_daily_quote_get(client):
    response = client.get("/api/v1/daily/")
    assert response.status_code == 405


def test_daily_quote_put(client):
    response = client.put("/api/v1/daily/")
    assert response.status_code == 405


def test_random_quote(client):
    response = client.post("/api/v1/random/")
    assert response.status_code == 200
    assert len(response.json().get('quote')) > 0


def test_daily_quote(client):
    response = client.post("/api/v1/daily/")
    assert response.status_code == 200
    assert len(response.json().get('quote')) > 0


def test_quote_by_id(client):
    response = client.post("/api/v1/quote/817")
    assert response.status_code == 200
    assert len(response.json().get('quote')) > 0


def test_bad_id_quote(client):
    response = client.post("/api/v1/quote/999999")
    assert response.status_code == 404
    assert response.json().get('detail') == 'Quote not found'
