def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Sample FastAPI CI/CD App"}


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_single_item(client):
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_create_item(client):
    new_item = {"id": 3, "name": "Keyboard", "price": 1200.0}
    response = client.post("/items", json=new_item)
    assert response.status_code == 201
    assert response.json()["name"] == "Keyboard"

    # confirm it's now retrievable too
    get_response = client.get("/items/3")
    assert get_response.status_code == 200


def test_create_duplicate_item(client):
    duplicate_item = {"id": 1, "name": "Laptop 2", "price": 60000.0}
    response = client.post("/items", json=duplicate_item)
    assert response.status_code == 400
    assert response.json()["detail"] == "Item with this ID already exists"
