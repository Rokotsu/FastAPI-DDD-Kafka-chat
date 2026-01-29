def test_create_chat_returns_201(client):
    response = client.post("/api/chats", json={"title": "Support"})

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "Support"
    assert payload["oid"]
    assert payload["created_at"]


def test_create_chat_duplicate_returns_409(client):
    payload = {"title": "General"}

    first_response = client.post("/api/chats", json=payload)
    second_response = client.post("/api/chats", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409
    assert "detail" in second_response.json()
