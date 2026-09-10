import pytest
from fastapi.testclient import TestClient

from app.main import app, items_db, Item


@pytest.fixture()
def client():
    """A fresh TestClient for each test."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_items_db():
    """
    Reset the in-memory 'database' before every test so tests are
    isolated and don't leak state into each other (order-independent).
    """
    original = [
        Item(id=1, name="Laptop", price=55000.0),
        Item(id=2, name="Mouse", price=500.0),
    ]
    items_db.clear()
    items_db.extend(original)
    yield
    items_db.clear()
    items_db.extend(original)
