import pytest
import app as app_module

@pytest.fixture
def client():
    original_inventory = [item.copy() for item in app_module.inventory]
    original_next_id = app_module.next_id

    app_module.inventory[:] = [
        {   "id": 1,
            "name": "Organic Almond Milk",
            "brand": "Silk",
            "price": 350.0,
            "stock": 20,
            "barcode": "1234567890123"
        },
        {   "id": 2,
            "name": "Oats",
            "brand": "Quaker",
            "price": 250.0,
            "stock": 15,
            "barcode": "9876543210987"
        }
    ]
    app_module.next_id = 3
    app_module.app.config["TESTING"] = True
    with app_module.app.test_client() as test_client:
        yield test_client
    app_module.inventory[:] = original_inventory
    app_module.next_id = original_next_id

def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_existing_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Organic Almond Milk"

def test_get_missing_item(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404

def test_add_item(client):
    response = client.post(
        "/inventory",
        json={
            "name": "Rice",
            "brand": "Pishori",
            "price": 180,
            "stock": 30,
            "barcode": "4567890123456"
        }
    )
    assert response.status_code == 201
    assert response.get_json()["name"] == "Rice"

def test_update_item(client):
    response = client.patch(
        "/inventory/1",
        json={"stock": 50}
    )
    assert response.status_code == 200
    assert response.get_json()["stock"] == 50

def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert len(app_module.inventory) == 1

def test_delete_missing_item(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404
