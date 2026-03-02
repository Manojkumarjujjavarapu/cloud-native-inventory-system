def test_get_products(client):

    res = client.get("/products")

    assert res.status_code == 200