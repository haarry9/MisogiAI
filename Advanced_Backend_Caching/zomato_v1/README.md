# Zomato Restaurant Management API (v1)

A basic FastAPI-based backend for managing restaurant listings. Supports full CRUD, search, filtering, and pagination.

## Features
- Async SQLite with SQLAlchemy
- Complete CRUD for restaurants
- Validation (name, phone, rating, times)
- Search by cuisine
- List active restaurants
- Pagination (skip, limit)
- OpenAPI docs

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
   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Endpoints

- `POST   /restaurants/`         - Create new restaurant
- `GET    /restaurants/`         - List all restaurants (pagination)
- `GET    /restaurants/{id}`     - Get specific restaurant
- `PUT    /restaurants/{id}`     - Update restaurant
- `DELETE /restaurants/{id}`     - Delete restaurant
- `GET    /restaurants/search?cuisine=TYPE` - Search by cuisine
- `GET    /restaurants/active`   - List only active restaurants

## Model Fields
- `id`: int
- `name`: str (3-100 chars, unique)
- `description`: str (optional)
- `cuisine_type`: str
- `address`: str
- `phone_number`: str (validated)
- `rating`: float (0.0-5.0)
- `is_active`: bool
- `opening_time`: time
- `closing_time`: time
- `created_at`: datetime
- `updated_at`: datetime

---

**Enjoy building your food delivery platform foundation!**