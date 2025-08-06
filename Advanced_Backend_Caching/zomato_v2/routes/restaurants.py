from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, schemas
from ..database import get_db
from fastapi_cache2.decorator import cache

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=schemas.RestaurantOut, status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: schemas.RestaurantCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_restaurant(db, restaurant)

@router.get("/", response_model=List[schemas.RestaurantOut])
@cache(expire=600, namespace="restaurants")
async def list_restaurants(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurants(db, skip=skip, limit=limit)

@router.get("/{restaurant_id}", response_model=schemas.RestaurantOut)
@cache(expire=600, namespace="restaurants", key_builder=lambda func, *args, **kwargs: f"restaurant:{kwargs['restaurant_id']}")
async def get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurant(db, restaurant_id)

@router.put("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_restaurant(db, restaurant_id, restaurant)

@router.delete("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def delete_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_restaurant(db, restaurant_id)

@router.get("/{restaurant_id}/menu", response_model=List[schemas.MenuItemOut])
@cache(expire=480, namespace="menu-items", key_builder=lambda func, *args, **kwargs: f"menu:{kwargs['restaurant_id']}:{kwargs.get('skip',0)}:{kwargs.get('limit',100)}")
async def get_menu_for_restaurant(restaurant_id: int, skip: int = Query(0, ge=0), limit: int = Query(100, le=500), db: AsyncSession = Depends(get_db)):
    return await crud.get_menu_for_restaurant(db, restaurant_id, skip=skip, limit=limit)

@router.get("/{restaurant_id}/with-menu", response_model=schemas.RestaurantWithMenu)
@cache(expire=900, namespace="restaurant-menus", key_builder=lambda func, *args, **kwargs: f"restaurant-menu:{kwargs['restaurant_id']}")
async def get_restaurant_with_menu(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurant_with_menu(db, restaurant_id)

@router.get("/{restaurant_id}/average-menu-price", response_model=float)
@cache(expire=300, namespace="analytics", key_builder=lambda func, *args, **kwargs: f"avg-price:{kwargs['restaurant_id']}")
async def average_menu_price(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_average_menu_price(db, restaurant_id)

@router.get("/with-menu", response_model=List[schemas.RestaurantWithMenu])
@cache(expire=900, namespace="restaurant-menus")
async def get_restaurants_with_menu(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.get_restaurants_with_menu(db, skip=skip, limit=limit)