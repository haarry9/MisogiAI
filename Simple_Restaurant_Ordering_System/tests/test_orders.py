from fastapi.testclient import TestClient
from app.main import app
from decimal import Decimal

client = TestClient(app)

# Helper to create a valid order payload
def valid_order_payload():
    return {
        "customer": {
            "name": "Alice Smith",
            "phone": "5551234567"
        },
        "items": [
            {
                "menu_item_id": 1,
                "menu_item_name": "Margherita Pizza",
                "quantity": 1,
                "unit_price": "15.99"
            },
            {
                "menu_item_id": 2,
                "menu_item_name": "Spicy Chicken Wings",
                "quantity": 2,
                "unit_price": "12.50"
            }
        ]
    }

def test_valid_order():
    resp = client.post("/orders", json=valid_order_payload())
    assert resp.status_code == 201
    data = resp.json()
    assert data["customer"]["name"] == "Alice Smith"
    assert data["items_total"] == 15.99 + 2 * 12.50
    assert data["total_items_count"] == 3

def test_empty_items():
    payload = valid_order_payload()
    payload["items"] = []
    resp = client.post("/orders", json=payload)
    assert resp.status_code == 422

def test_invalid_phone():
    payload = valid_order_payload()
    payload["customer"]["phone"] = "123"
    resp = client.post("/orders", json=payload)
    assert resp.status_code == 422

def test_large_quantity():
    payload = valid_order_payload()
    payload["items"][0]["quantity"] = 15
    resp = client.post("/orders", json=payload)
    assert resp.status_code == 422

def test_status_update():
    # Create order
    resp = client.post("/orders", json=valid_order_payload())
    order_id = resp.json()["id"]
    # Update status
    resp2 = client.put(f"/orders/{order_id}/status?status=confirmed")
    assert resp2.status_code == 200
    assert resp2.json()["status"] == "confirmed"
