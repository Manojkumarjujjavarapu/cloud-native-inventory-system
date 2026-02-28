def test_inventory_update(client):
    response = client.post("/inventory", json={
        "product_id": 1,
        "stock": 10
    })

    assert response.status_code == 201


def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200