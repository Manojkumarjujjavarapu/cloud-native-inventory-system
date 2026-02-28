def test_create_user(client):
    response = client.post("/users", json={
        "name": "Test User",
        "email": "test@example.com"
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test User"


def test_get_users(client):
    response = client.get("/users")
    assert response.status_code == 200