from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/menu-items", tags=["menu-items"])

@router.post("/restaurants/{restaurant_id}/menu-items/", response_model=schemas.MenuItemOut, status_code=status.HTTP_201_CREATED)
async def add_menu_item(restaurant_id: int, item: schemas.MenuItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_menu_item(db, restaurant_id, item)

@router.get("/", response_model=List[schemas.MenuItemOut])
async def list_menu_items(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    return await crud.get_menu_items(db, skip=skip, limit=limit)

@router.get("/{item_id}", response_model=schemas.MenuItemOut)
async def get_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_menu_item(db, item_id)

@router.get("/{item_id}/with-restaurant", response_model=schemas.MenuItemWithRestaurant)
async def get_menu_item_with_restaurant(item_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_menu_item_with_restaurant(db, item_id)

@router.put("/{item_id}", response_model=schemas.MenuItemOut)
async def update_menu_item(item_id: int, item: schemas.MenuItemUpdate, db: AsyncSession = Depends(get_db)):
    return await crud.update_menu_item(db, item_id, item)

@router.delete("/{item_id}", response_model=schemas.MenuItemOut)
async def delete_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_menu_item(db, item_id)

@router.get("/search", response_model=List[schemas.MenuItemOut])
async def search_menu_items(
    category: Optional[str] = None,
    vegetarian: Optional[bool] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db)
):
    return await crud.search_menu_items(db, category=category, vegetarian=vegetarian, skip=skip, limit=limit)