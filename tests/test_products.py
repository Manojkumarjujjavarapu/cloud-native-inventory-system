def test_create_product(client):
    response = client.post("/products", json={
        "name": "Laptop",
        "price": 50000
    })

    assert response.status_code == 201


def test_get_products(client):
    response = client.get("/products")
    assert response.status_code == 200