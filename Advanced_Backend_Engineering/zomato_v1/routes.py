from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, schemas
from .database import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=schemas.RestaurantOut, status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: schemas.RestaurantCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_restaurant(db, restaurant)

@router.get("/", response_model=List[schemas.RestaurantOut])
async def list_restaurants(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurants(db, skip=skip, limit=limit)

@router.get("/active", response_model=List[schemas.RestaurantOut])
async def list_active_restaurants(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.get_active_restaurants(db, skip=skip, limit=limit)

@router.get("/search", response_model=List[schemas.RestaurantOut])
async def search_by_cuisine(cuisine: str, skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.search_restaurants_by_cuisine(db, cuisine, skip=skip, limit=limit)

@router.get("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurant(db, restaurant_id)

@router.put("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_restaurant(db, restaurant_id, restaurant)

@router.delete("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def delete_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_restaurant(db, restaurant_id)