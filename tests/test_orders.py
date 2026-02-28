def test_create_order(client):
    response = client.post("/orders", json={
        "user_id": 1,
        "product_id": 1,
        "quantity": 2
    })

    assert response.status_code == 201


def test_get_orders(client):
    response = client.get("/orders")
    assert response.status_code == 200