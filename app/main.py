from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# app = FastAPI(title="Sample FastAPI CI/CD App", version="1.0.0")
app = FastAPI(title="Sample FastAPI CI/CD App", version="1.1.0")


class Item(BaseModel):
    id: int
    name: str
    price: float


# in-memory "database" (just for demo purposes)
items_db: List[Item] = [
    Item(id=1, name="Laptop", price=57000.0),
    Item(id=2, name="Mouse", price=500.0),
]


@app.get("/")
def read_root():
    return {"message": "Welcome to the Sample FastAPI CI/CD App"}


@app.get("/health")
def health_check():
    """Used by Docker HEALTHCHECK and monitoring tools."""
    return {"status": "healthy"}


@app.get("/items", response_model=List[Item])
def get_items():
    return items_db


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    if any(existing.id == item.id for existing in items_db):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    items_db.append(item)
    return item
