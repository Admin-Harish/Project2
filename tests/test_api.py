from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_item_lifecycle():
    assert client.get("/health").json()["status"] == "ok"
    created = client.post("/api/items", json={"name": "Widget", "quantity": 5})
    assert created.status_code == 201 and created.json()["in_stock"] is True
    assert client.post("/api/items", json={"name": "widget"}).status_code == 409
    assert client.get("/api/items", params={"q": "wid"}).json()["count"] == 1
    assert client.put("/api/items/1", json={"quantity": 0}).json()["in_stock"] is False
    assert client.delete("/api/items/1").status_code == 204
    assert client.get("/api/items/1").status_code == 404
