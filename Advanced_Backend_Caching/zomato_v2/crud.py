from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from .models import Restaurant, MenuItem
from .schemas import RestaurantCreate, RestaurantUpdate, MenuItemCreate, MenuItemUpdate
from typing import Optional

# --- Restaurant CRUD ---
async def create_restaurant(db: AsyncSession, restaurant: RestaurantCreate):
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

async def get_restaurant_with_menu(db: AsyncSession, restaurant_id: int):
    result = await db.execute(
        select(Restaurant).options(selectinload(Restaurant.menu_items)).where(Restaurant.id == restaurant_id)
    )
    restaurant = result.scalar_one_or_none()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

async def get_restaurants_with_menu(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(Restaurant).options(selectinload(Restaurant.menu_items)).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def get_average_menu_price(db: AsyncSession, restaurant_id: int):
    result = await db.execute(
        select(func.avg(MenuItem.price)).where(MenuItem.restaurant_id == restaurant_id)
    )
    avg_price = result.scalar()
    return float(avg_price) if avg_price is not None else 0.0

# --- MenuItem CRUD ---
async def create_menu_item(db: AsyncSession, restaurant_id: int, item: MenuItemCreate):
    restaurant = await get_restaurant(db, restaurant_id)
    db_item = MenuItem(**item.dict(), restaurant_id=restaurant_id)
    db.add(db_item)
    try:
        await db.commit()
        await db.refresh(db_item)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error")
    return db_item

async def get_menu_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

async def get_menu_items(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(MenuItem).offset(skip).limit(limit))
    return result.scalars().all()

async def update_menu_item(db: AsyncSession, item_id: int, item_update: MenuItemUpdate):
    db_item = await get_menu_item(db, item_id)
    for field, value in item_update.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    try:
        await db.commit()
        await db.refresh(db_item)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Integrity error")
    return db_item

async def delete_menu_item(db: AsyncSession, item_id: int):
    db_item = await get_menu_item(db, item_id)
    await db.delete(db_item)
    await db.commit()
    return db_item

async def get_menu_item_with_restaurant(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(MenuItem).options(selectinload(MenuItem.restaurant)).where(MenuItem.id == item_id)
    )
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

async def get_menu_for_restaurant(db: AsyncSession, restaurant_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(MenuItem).where(MenuItem.restaurant_id == restaurant_id).offset(skip).limit(limit)
    )
    return result.scalars().all()

async def search_menu_items(db: AsyncSession, category: Optional[str] = None, vegetarian: Optional[bool] = None, skip: int = 0, limit: int = 10):
    query = select(MenuItem)
    if category:
        query = query.where(MenuItem.category.ilike(f"%{category}%"))
    if vegetarian is not None:
        query = query.where(MenuItem.is_vegetarian == vegetarian)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()