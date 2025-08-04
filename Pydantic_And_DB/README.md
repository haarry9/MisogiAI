# Restaurant Food Ordering System (Menu Management API)

This project is a simple Restaurant Food Menu Management API built with FastAPI and Pydantic.  
It allows restaurant staff to manage menu items and customers to view available food items.  
All data is stored in-memory using Python dictionaries (no external database required).

---

## Features

- **Add, update, delete, and view menu items**
- **Filter menu items by category**
- **Custom validation for food items (name, price, category rules, etc.)**
- **Computed properties for price category and dietary info**

---

## Folder Structure

```
Pydantic_And_DB/
│
├── main.py         # FastAPI app with all endpoints
├── models.py       # FoodCategory enum and FoodItem Pydantic model
├── database.py     # In-memory menu_db dictionary
└── sample_data.py  # Sample menu items for testing
```

---

## How to Run

1. **Install dependencies:**
    ```bash
    pip install fastapi uvicorn pydantic
    ```

2. **Start the API server:**
    ```bash
    uvicorn main:app --reload
    ```

3. **API will be available at:**  
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)

---

## API Endpoints

- `GET /menu` — Get all menu items
- `GET /menu/{item_id}` — Get a specific menu item by ID
- `POST /menu` — Add a new menu item
- `PUT /menu/{item_id}` — Update an existing menu item
- `DELETE /menu/{item_id}` — Remove a menu item
- `GET /menu/category/{category}` — Get items by category

---

## Data Model

See `models.py` for full details.  
Key fields:
- `id`: Integer (auto-generated)
- `name`: String (3-100 chars, only letters/spaces)
- `description`: String (10-500 chars)
- `category`: Enum (appetizer, main_course, dessert, beverage, salad)
- `price`: Decimal ($1.00-$100.00, max 2 decimals)
- `is_available`: Boolean (default True)
- `preparation_time`: Integer (1-120, beverages ≤ 10)
- `ingredients`: List of strings (at least 1)
- `calories`: Optional integer (if provided, must be positive)
- `is_vegetarian`: Boolean (default False)
- `is_spicy`: Boolean (default False, not allowed for dessert/beverage)
- **Custom validation and computed properties included**

---

## Sample Data

See `sample_data.py` for example menu items.

---

## Notes

- All data is lost when the server restarts (in-memory only).
- To pre-load sample data, you can manually insert items from `sample_data.py` into `menu_db` at startup.

---

