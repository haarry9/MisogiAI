from fastapi import FastAPI, HTTPException
from typing import List
from decimal import Decimal
from models import FoodItem, FoodCategory
from database import menu_db

app = FastAPI()

# Helper to auto-increment IDs
def get_next_id():
    if menu_db:
        return max(menu_db.keys()) + 1
    return 1

@app.get("/menu", response_model=List[FoodItem])
def get_menu():
    return list(menu_db.values())

@app.get("/menu/{item_id}", response_model=FoodItem)
def get_menu_item(item_id: int):
    item = menu_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/menu", response_model=FoodItem)
def add_menu_item(item: FoodItem):
    item_id = get_next_id()
    item.id = item_id
    menu_db[item_id] = item
    return item

@app.put("/menu/{item_id}", response_model=FoodItem)
def update_menu_item(item_id: int, item: FoodItem):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item.id = item_id
    menu_db[item_id] = item
    return item

@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int):
    if item_id not in menu_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del menu_db[item_id]
    return {"detail": "Item deleted"}

@app.get("/menu/category/{category}", response_model=List[FoodItem])
def get_items_by_category(category: FoodCategory):
    return [item for item in menu_db.values() if item.category == category]