from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=schemas.RestaurantOut, status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: schemas.RestaurantCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_restaurant(db, restaurant)

@router.get("/", response_model=List[schemas.RestaurantOut])
async def list_restaurants(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurants(db, skip=skip, limit=limit)

@router.get("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurant(db, restaurant_id)

@router.put("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_restaurant(db, restaurant_id, restaurant)

@router.delete("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def delete_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_restaurant(db, restaurant_id)

@router.get("/{restaurant_id}/menu", response_model=List[schemas.MenuItemOut])
async def get_menu_for_restaurant(restaurant_id: int, skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: AsyncSession = Depends(get_db)):
    return await crud.get_menu_for_restaurant(db, restaurant_id, skip=skip, limit=limit)

@router.get("/{restaurant_id}/with-menu", response_model=schemas.RestaurantWithMenu)
async def get_restaurant_with_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurant_with_menu(db, restaurant_id)

@router.get("/{restaurant_id}/average-menu-price", response_model=float)
async def average_menu_price(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_average_menu_price(db, restaurant_id)

@router.get("/with-menu", response_model=List[schemas.RestaurantWithMenu])
async def get_restaurants_with_menu(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurants_with_menu(db, skip=skip, limit=limit)