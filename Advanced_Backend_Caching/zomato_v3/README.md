# Zomato v3 - Food Delivery Backend

A complete food delivery backend system built with FastAPI and SQLAlchemy, supporting complex relationships, analytics, and advanced business logic.

## Features
- Customer, Restaurant, Menu, Order, and Review management
- Many-to-many and one-to-many relationships
- Order status workflow and validation
- Analytics for restaurants and customers
- Search and filter endpoints
- Review sentiment stub
- SQLite database (easy to swap for Postgres)

## Directory Structure
```
zomato_v3/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── routes/
│   ├── customers.py
│   ├── orders.py
│   ├── reviews.py
│   ├── restaurants.py
├── utils/
│   └── business_logic.py
├── requirements.txt
└── README.md
```

## Setup & Run

1. **Install dependencies**
   ```bash
   conda activate llm
   pip install -r requirements.txt
   ```

2. **Run the server**
   ```bash
   uvicorn zomato_v3.main:app --reload
   ```

3. **API docs**
   Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints (Summary)

### Customers
- `POST   /customers/` — Create customer
- `GET    /customers/` — List customers
- `GET    /customers/{customer_id}` — Get customer details
- `PUT    /customers/{customer_id}` — Update customer
- `DELETE /customers/{customer_id}` — Delete customer
- `GET    /customers/{customer_id}/orders` — Customer's order history
- `GET    /customers/{customer_id}/reviews` — Customer's reviews
- `GET    /customers/{customer_id}/analytics` — Customer analytics

### Orders
- `POST   /customers/{customer_id}/orders/` — Place new order
- `GET    /orders/{order_id}` — Get order with full details
- `PUT    /orders/{order_id}/status` — Update order status
- `GET    /restaurants/{restaurant_id}/orders` — Restaurant's orders

### Reviews
- `POST   /orders/{order_id}/review` — Add review after order completion
- `GET    /restaurants/{restaurant_id}/reviews` — Get restaurant reviews

### Restaurants
- `GET    /restaurants/search` — Search by cuisine, rating, location
- `GET    /restaurants/{restaurant_id}/analytics` — Restaurant analytics

## Example: Place an Order
```json
POST /customers/1/orders/
{
  "restaurant_id": 2,
  "delivery_address": "123 Main St",
  "special_instructions": "Leave at door",
  "order_items": [
    {"menu_item_id": 5, "quantity": 2, "special_requests": "extra spicy"},
    {"menu_item_id": 7, "quantity": 1}
  ]
}
```

## Example: Add a Review
```json
POST /orders/10/review
{
  "rating": 5,
  "comment": "Amazing food and fast delivery!"
}
```

## Notes
- Order status must follow workflow: placed → confirmed → preparing → out_for_delivery → delivered/cancelled
- Reviews can only be added for delivered orders
- Analytics endpoints return stats like total orders, revenue, average rating, and popular items

## Caching System (Enterprise)

This project uses Redis and fastapi-cache2 for advanced, production-style caching:

- **Static Data**: 30+ min TTL (restaurant details, menu, customer profiles)
- **Dynamic Data**: 2-5 min TTL (order status, live reviews)
- **Real-time Data**: 30 sec TTL (delivery slots, capacity)
- **Analytics Data**: 15 min TTL (popular items, revenue)
- **Session Caching**: 30 min TTL (customer sessions)
- **Conditional Caching**: e.g., only cache completed orders
- **Write-through & Cache-aside**: Used for analytics, ratings, etc.
- **Background Warming**: Popular data is pre-cached on startup
- **Monitoring**: Endpoints for health, stats, memory, performance

### Redis Config
- `REDIS_URL` (default: redis://localhost:6379)
- `CACHE_PREFIX` (default: zomato-cache)
- TTLs are set per data type (see `zomato_v3/cache.py`)

### Cache Management Endpoints
- `GET /cache/health` — Redis health check
- `GET /cache/stats/namespaces` — Stats by namespace
- `GET /cache/memory-usage` — Memory consumption
- `DELETE /cache/clear/expired` — Remove expired keys
- `POST /cache/warm/{namespace}` — Warm specific cache

### Performance Monitoring
- `GET /analytics/cache-performance` — Hit/miss ratios

### Invalidation
- Caches are invalidated on order placement, status update, review, and menu update.

---

**Enjoy building with Zomato v3!**