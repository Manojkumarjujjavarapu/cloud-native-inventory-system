def test_register_user(client):

    res = client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@test.com",
        "password": "123",
        "role": "user"
    })

    assert res.status_code == 201