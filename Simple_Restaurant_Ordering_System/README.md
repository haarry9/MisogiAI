# Simple Restaurant Ordering System

A FastAPI-based assignment project to demonstrate nested models, validation, and basic API design for a restaurant order management system.

## Features
- In-memory database for menu and orders
- Nested models: Orders contain customer info and order items
- Computed properties for totals
- Validation at all levels (Pydantic)
- Custom error handling
- Test cases for all main scenarios

## Folder Structure
```
app/
  main.py         # FastAPI app and endpoints
  models.py       # Pydantic models (Order, Customer, etc.)
  schemas.py      # Response/request schemas
  db.py           # In-memory DB and counters
  exceptions.py   # Custom exception handler
  utils.py        # Utility functions

tests/
  test_orders.py  # Test cases for order endpoints
```

## How to Run
1. Install dependencies (in your conda env):
   ```bash
   pip install fastapi uvicorn
   ```
2. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```
3. Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## API Endpoints
- `POST /orders` - Create a new order
- `GET /orders` - List all orders (summary)
- `GET /orders/{order_id}` - Get details of a specific order
- `PUT /orders/{order_id}/status` - Update order status

## Testing
Run the test cases with:
```bash
pytest tests/test_orders.py
```

## Assignment Focus
- Nested Pydantic models
- Validation and error handling
- Computed properties
- JSON serialization of nested data