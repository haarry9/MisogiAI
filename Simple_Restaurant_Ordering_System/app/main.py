from fastapi import FastAPI, HTTPException, status, Path
from fastapi.exceptions import RequestValidationError
from .models import FoodItem, Order, OrderStatus, OrderItem, Customer
from .db import menu_db, orders_db
from .schemas import (
    FoodItemResponse, OrderResponse, OrderSummaryResponse, ErrorResponse
)
from .exceptions import validation_exception_handler

app = FastAPI(
    title="Restaurant Ordering System",
    description="API for managing restaurant menu and orders",
    version="1.0.0"
)

# Register custom exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.post("/orders", response_model=OrderResponse, status_code=201)
def create_order(order: Order):
    order.id = get_next_order_id()
    orders_db[order.id] = order
    return order_to_response(order)

@app.get("/orders", response_model=list[OrderSummaryResponse])
def get_orders():
    return [
        OrderSummaryResponse(
            id=o.id,
            customer_name=o.customer.name,
            status=o.status,
            items_total=o.items_total
        )
        for o in orders_db.values()
    ]

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int = Path(..., gt=0)):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order_to_response(order)

@app.put("/orders/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: int, status: OrderStatus):
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = status
    return order_to_response(order)

# Helper to convert Order to OrderResponse
def order_to_response(order: Order) -> OrderResponse:
    return OrderResponse(
        id=order.id,
        customer=order.customer,
        items=[
            {
                **item.dict(),
                "item_total": item.item_total
            }
            for item in order.items
        ],
        status=order.status,
        items_total=order.items_total,
        total_items_count=order.total_items_count
    )

# Import get_next_order_id from utils
def get_next_order_id():
    from .utils import get_next_order_id as _get_next_order_id
    return _get_next_order_id()
