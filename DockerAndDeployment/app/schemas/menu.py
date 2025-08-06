from pydantic import BaseModel
from typing import List, Optional

class MenuItemBase(BaseModel):
    name: str
    price: float

class MenuItemCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int
    class Config:
        orm_mode = True

class MenuBase(BaseModel):
    name: str

class MenuCreate(MenuBase):
    pass

class Menu(MenuBase):
    id: int
    items: List[MenuItem] = []
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    item_id: int
    quantity: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: Optional[str]
    class Config:
        orm_mode = True