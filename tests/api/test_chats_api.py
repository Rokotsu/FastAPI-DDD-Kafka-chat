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


def test_chat_messages_flow(client):
    chat_response = client.post("/api/chats", json={"title": "Website"})
    chat_oid = chat_response.json()["oid"]

    message_response = client.post(
        f"/api/chats/{chat_oid}/messages",
        json={"text": "Hello from widget"},
    )
    detail_response = client.get(f"/api/chats/{chat_oid}")

    assert message_response.status_code == 201
    assert message_response.json()["text"] == "Hello from widget"
    assert detail_response.status_code == 200
    assert detail_response.json()["messages"][0]["text"] == "Hello from widget"


def test_create_message_for_missing_chat_returns_404(client):
    response = client.post(
        "/api/chats/missing-chat/messages",
        json={"text": "Hello"},
    )

    assert response.status_code == 404
