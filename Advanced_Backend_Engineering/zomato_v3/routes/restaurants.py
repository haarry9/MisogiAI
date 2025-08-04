from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal
from ..utils.business_logic import search_restaurants

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/restaurants/{restaurant_id}/analytics")
def restaurant_analytics(restaurant_id: int, db: Session = Depends(get_db)):
    return crud.get_restaurant_analytics(db, restaurant_id)

@router.get("/restaurants/search", response_model=list[schemas.RestaurantBase])
def search(cuisine: str = Query(None), rating: float = Query(None), location: str = Query(None), db: Session = Depends(get_db)):
    return search_restaurants(db, cuisine=cuisine, rating=rating, location=location)