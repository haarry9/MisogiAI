from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal
from ..utils.business_logic import search_restaurants
from ..cache import static_cache, analytics_cache, invalidate_namespace

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/restaurants/{restaurant_id}/analytics")
@analytics_cache(namespace="analytics:restaurants", expire=900, key_builder=lambda *a, **k: f"restaurant:{k['restaurant_id']}")
def restaurant_analytics(restaurant_id: int, db: Session = Depends(get_db)):
    return crud.get_restaurant_analytics(db, restaurant_id)

@router.get("/restaurants/search", response_model=list[schemas.RestaurantBase])
@static_cache(namespace="search", expire=1800)
def search(cuisine: str = Query(None), rating: float = Query(None), location: str = Query(None), db: Session = Depends(get_db)):
    return search_restaurants(db, cuisine=cuisine, rating=rating, location=location)