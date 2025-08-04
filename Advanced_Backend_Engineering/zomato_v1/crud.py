from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .models import Restaurant
from .schemas import RestaurantCreate, RestaurantUpdate

async def create_restaurant(db: AsyncSession, restaurant: RestaurantCreate):
    # Check for duplicate name
    result = await db.execute(select(Restaurant).where(Restaurant.name == restaurant.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Restaurant name already exists")
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    try:
        await db.commit()
        await db.refresh(db_restaurant)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error")
    return db_restaurant

async def get_restaurant(db: AsyncSession, restaurant_id: int):
    result = await db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

async def get_restaurants(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    return result.scalars().all()

async def update_restaurant(db: AsyncSession, restaurant_id: int, restaurant_update: RestaurantUpdate):
    db_restaurant = await get_restaurant(db, restaurant_id)
    if restaurant_update.name and restaurant_update.name != db_restaurant.name:
        # Check for duplicate name
        result = await db.execute(select(Restaurant).where(Restaurant.name == restaurant_update.name))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Restaurant name already exists")
    for field, value in restaurant_update.dict(exclude_unset=True).items():
        setattr(db_restaurant, field, value)
    try:
        await db.commit()
        await db.refresh(db_restaurant)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error")
    return db_restaurant

async def delete_restaurant(db: AsyncSession, restaurant_id: int):
    db_restaurant = await get_restaurant(db, restaurant_id)
    await db.delete(db_restaurant)
    await db.commit()
    return db_restaurant

async def search_restaurants_by_cuisine(db: AsyncSession, cuisine_type: str, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Restaurant).where(Restaurant.cuisine_type.ilike(f"%{cuisine_type}%")).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_active_restaurants(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Restaurant).where(Restaurant.is_active == True).offset(skip).limit(limit)
    )
    return result.scalars().all()