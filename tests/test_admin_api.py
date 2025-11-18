from fastapi.testclient import TestClient

from app.main import create_app


def test_admin_can_create_and_archive_publisher():
    client = TestClient(create_app())

    create_payload = {
        "name": "Test Publisher",
        "category_ids": ["online_casino"],
        "country": "US",
        "notes": "QA test",
    }
    create_response = client.post("/api/admin/publishers", json=create_payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["publisher"]["name"] == "Test Publisher"

    publisher_id = created["publisher"]["id"]
    archive_response = client.delete(f"/api/admin/publishers/{publisher_id}")
    assert archive_response.status_code == 200
    archived = archive_response.json()
    assert archived["publisher"]["status"] == "inactive"


def test_admin_update_publisher():
    client = TestClient(create_app())
    create_payload = {
        "name": "Another Publisher",
        "category_ids": ["dfs"],
        "country": "US",
    }
    response = client.post("/api/admin/publishers", json=create_payload)
    publisher_id = response.json()["publisher"]["id"]

    update_payload = {"name": "Another Publisher Updated", "status": "active"}
    update_response = client.put(f"/api/admin/publishers/{publisher_id}", json=update_payload)
    assert update_response.status_code == 200
    assert update_response.json()["publisher"]["name"] == "Another Publisher Updated"
