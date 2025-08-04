# Zomato Restaurant-Menu System API (v2)

This version extends the basic restaurant management system to support menu item management and advanced restaurant-menu relationships.

## Features
- Restaurant CRUD (as before)
- Menu item CRUD (add, update, delete, list)
- One-to-many relationship: Each restaurant can have multiple menu items
- Advanced queries: filter/search menu items, get restaurant with menu, get menu item with restaurant, etc.
- Cascade delete: Deleting a restaurant deletes its menu items
- Efficient relationship loading (selectinload)
- Nested Pydantic schemas for complex responses

## Setup

1. **Install dependencies**
   ```bash
   conda activate llm
   pip install -r requirements.txt
   ```

2. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

3. **API Docs**
   - Swagger UI: http://localhost:8000/docs
   - Redoc: http://localhost:8000/redoc

## Endpoints

- Restaurant endpoints: CRUD, get with menu, etc.
- Menu item endpoints: CRUD, search, get with restaurant, etc.

