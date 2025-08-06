from pydantic import BaseModel, Field, validator, condecimal
from typing import Optional, List
from datetime import time, datetime
import re

class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    price: condecimal(gt=0, max_digits=10, decimal_places=2)
    category: str
    is_vegetarian: Optional[bool] = False
    is_vegan: Optional[bool] = False
    is_available: Optional[bool] = True
    preparation_time: int = Field(..., ge=1)

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    price: Optional[condecimal(gt=0, max_digits=10, decimal_places=2)] = None
    category: Optional[str] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_available: Optional[bool] = None
    preparation_time: Optional[int] = Field(None, ge=1)

class MenuItemOut(MenuItemBase):
    id: int
    restaurant_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RestaurantBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: str
    address: str
    phone_number: str
    rating: Optional[float] = Field(0.0, ge=0.0, le=5.0)
    is_active: Optional[bool] = True
    opening_time: time
    closing_time: time

    @validator("phone_number")
    def validate_phone(cls, v):
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    cuisine_type: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0.0, le=5.0)
    is_active: Optional[bool] = None
    opening_time: Optional[time] = None
    closing_time: Optional[time] = None

    @validator("phone_number")
    def validate_phone(cls, v):
        if v is None:
            return v
        pattern = r"^\+?\d{10,15}$"
        if not re.match(pattern, v):
            raise ValueError("Invalid phone number format")
        return v

class RestaurantOut(RestaurantBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class RestaurantWithMenu(RestaurantOut):
    menu_items: List[MenuItemOut] = []

class MenuItemWithRestaurant(MenuItemOut):
    restaurant: RestaurantOut