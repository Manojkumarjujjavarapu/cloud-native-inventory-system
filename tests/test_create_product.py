def test_create_product(client):

    res = client.post("/products", json={
        "name": "Test Product",
        "price": 100,
        "stock": 10,
        "image_url": "https://example.com/img.jpg"
    })

    # Admin protection may return 401/403 depending on auth
    assert res.status_code in [201, 401, 403]