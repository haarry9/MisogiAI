from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db import models
from app.schemas import menu as schemas

async def get_menu(db: AsyncSession, menu_id: int):
    result = await db.execute(select(models.Menu).where(models.Menu.id == menu_id))
    return result.scalar_one_or_none()

async def get_menus(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Menu).offset(skip).limit(limit))
    return result.scalars().all()

async def create_menu(db: AsyncSession, menu: schemas.MenuCreate):
    db_menu = models.Menu(name=menu.name)
    db.add(db_menu)
    await db.commit()
    await db.refresh(db_menu)
    return db_menu

async def create_menu_item(db: AsyncSession, menu_id: int, item: schemas.MenuItemCreate):
    db_item = models.MenuItem(**item.dict(), menu_id=menu_id)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_menu_items(db: AsyncSession, menu_id: int):
    result = await db.execute(select(models.MenuItem).where(models.MenuItem.menu_id == menu_id))
    return result.scalars().all()

async def create_order(db: AsyncSession, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order

async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Order).offset(skip).limit(limit))
    return result.scalars().all()