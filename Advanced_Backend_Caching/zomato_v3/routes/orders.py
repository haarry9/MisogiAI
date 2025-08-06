from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal
from ..cache import dynamic_cache, conditional_cache, invalidate_key, invalidate_namespace

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/customers/{customer_id}/orders/", response_model=schemas.OrderBase)
def place_order(customer_id: int, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = crud.create_order(db, customer_id, order)
    if not db_order:
        raise HTTPException(status_code=400, detail="Order could not be created")
    # Invalidate customer, restaurant, analytics caches
    import asyncio
    asyncio.create_task(invalidate_key("customers", f"customer:{customer_id}"))
    asyncio.create_task(invalidate_key("restaurants", f"restaurant:{order.restaurant_id}"))
    asyncio.create_task(invalidate_namespace("analytics"))
    return db_order

@router.get("/orders/{order_id}", response_model=schemas.OrderDetail)
@conditional_cache(namespace="orders", expire=3600, condition=lambda o: o and o.order_status == "delivered", key_builder=lambda *a, **k: f"order:{k['order_id']}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.put("/orders/{order_id}/status", response_model=schemas.OrderBase)
def update_order_status(order_id: int, status: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    db_order = crud.update_order_status(db, order_id, status)
    if not db_order:
        raise HTTPException(status_code=400, detail="Invalid status transition or order not found")
    # Invalidate order, customer, analytics caches
    import asyncio
    asyncio.create_task(invalidate_key("orders", f"order:{order_id}"))
    asyncio.create_task(invalidate_key("customers", f"customer:{db_order.customer_id}"))
    asyncio.create_task(invalidate_namespace("analytics"))
    return db_order

@router.get("/customers/{customer_id}/orders", response_model=list[schemas.OrderBase])
def customer_order_history(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_orders(db, customer_id)

@router.get("/restaurants/{restaurant_id}/orders", response_model=list[schemas.OrderBase])
def restaurant_orders(restaurant_id: int, db: Session = Depends(get_db)):
    return crud.get_restaurant_orders(db, restaurant_id)