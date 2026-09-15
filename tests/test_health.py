def test_get_articles(base_client):
    endpoint = "/api/articles"
    res = base_client.get(endpoint=endpoint)

    assert res.status_code == 200
