from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatusEnum(str, Enum):
    placed = "placed"
    confirmed = "confirmed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"

class MenuItemBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    is_available: bool
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    id: int
    menu_item: MenuItemBase
    quantity: int
    item_price: float
    special_requests: Optional[str]
    class Config:
        orm_mode = True

class CustomerBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str
    address: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True

class RestaurantBase(BaseModel):
    id: int
    name: str
    cuisine: Optional[str]
    location: Optional[str]
    rating: float
    created_at: datetime
    class Config:
        orm_mode = True

class ReviewBase(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    order_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    id: int
    customer_id: int
    restaurant_id: int
    order_status: OrderStatusEnum
    total_amount: float
    delivery_address: str
    special_instructions: Optional[str]
    order_date: datetime
    delivery_time: Optional[datetime]
    order_items: List[OrderItemBase]
    class Config:
        orm_mode = True

class CustomerDetail(CustomerBase):
    orders: List[OrderBase] = []
    reviews: List[ReviewBase] = []

class RestaurantDetail(RestaurantBase):
    menu_items: List[MenuItemBase] = []
    orders: List[OrderBase] = []
    reviews: List[ReviewBase] = []

class OrderDetail(OrderBase):
    customer: CustomerBase
    restaurant: RestaurantBase
    order_items: List[OrderItemBase]
    review: Optional[ReviewBase]

class ReviewDetail(ReviewBase):
    customer: CustomerBase
    restaurant: RestaurantBase
    order: OrderBase

# Create/Update Schemas
class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str
    address: str

class CustomerUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    address: Optional[str]
    is_active: Optional[bool]

class OrderCreate(BaseModel):
    restaurant_id: int
    delivery_address: str
    special_instructions: Optional[str]
    order_items: List[dict]  # Each dict: {menu_item_id, quantity, special_requests}

class OrderStatusUpdate(BaseModel):
    order_status: OrderStatusEnum

class ReviewCreate(BaseModel):
    rating: int
    comment: Optional[str]

class ReviewUpdate(BaseModel):
    rating: Optional[int]
    comment: Optional[str]