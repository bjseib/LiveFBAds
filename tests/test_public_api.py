from fastapi.testclient import TestClient

from app.main import create_app


def test_list_categories_returns_seed_data():
    client = TestClient(create_app())
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert any(category["id"] == "online_casino" for category in data)
    online_casino = next(category for category in data if category["id"] == "online_casino")
    assert online_casino["publisher_count"] == 1


def test_list_creatives_for_category_returns_cached_entries():
    client = TestClient(create_app())
    response = client.get("/api/categories/online_casino/ads")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert data[0]["publisher_id"] == "pub_0001"
