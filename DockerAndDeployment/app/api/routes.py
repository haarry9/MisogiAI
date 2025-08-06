from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas import menu as schemas
from app.crud import menu as crud
from typing import List

router = APIRouter()

@router.post("/menus/", response_model=schemas.Menu)
async def create_menu(menu: schemas.MenuCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_menu(db, menu)

@router.get("/menus/", response_model=List[schemas.Menu])
async def read_menus(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_menus(db, skip=skip, limit=limit)

@router.post("/menus/{menu_id}/items/", response_model=schemas.MenuItem)
async def create_menu_item(menu_id: int, item: schemas.MenuItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_menu_item(db, menu_id, item)

@router.get("/menus/{menu_id}/items/", response_model=List[schemas.MenuItem])
async def read_menu_items(menu_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_menu_items(db, menu_id)

@router.post("/orders/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_order(db, order)

@router.get("/orders/", response_model=List[schemas.Order])
async def read_orders(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_orders(db, skip=skip, limit=limit)