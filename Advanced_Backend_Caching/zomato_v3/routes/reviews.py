from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal
from ..cache import dynamic_cache, invalidate_namespace

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/orders/{order_id}/review", response_model=schemas.ReviewBase)
def add_review(order_id: int, review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    db_review = crud.create_review(db, order_id, review)
    if not db_review:
        raise HTTPException(status_code=400, detail="Cannot review incomplete order or review already exists")
    # Invalidate analytics and reviews caches
    import asyncio
    asyncio.create_task(invalidate_namespace("analytics"))
    asyncio.create_task(invalidate_namespace("reviews"))
    return db_review

@router.get("/restaurants/{restaurant_id}/reviews", response_model=list[schemas.ReviewBase])
@dynamic_cache(namespace="reviews", expire=300, key_builder=lambda *a, **k: f"restaurant:{k['restaurant_id']}")
def restaurant_reviews(restaurant_id: int, db: Session = Depends(get_db)):
    return crud.get_restaurant_reviews(db, restaurant_id)

@router.get("/customers/{customer_id}/reviews", response_model=list[schemas.ReviewBase])
def customer_reviews(customer_id: int, db: Session = Depends(get_db)):
    return crud.get_customer_reviews(db, customer_id)