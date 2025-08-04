from pydantic import BaseModel
from typing import List, Optional
from decimal import Decimal
from .models import OrderStatus

class FoodItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Decimal

class OrderItemResponse(BaseModel):
    menu_item_id: int
    menu_item_name: str
    quantity: int
    unit_price: Decimal
    item_total: Decimal

class CustomerResponse(BaseModel):
    name: str
    phone: str

class OrderResponse(BaseModel):
    id: int
    customer: CustomerResponse
    items: List[OrderItemResponse]
    status: OrderStatus
    items_total: Decimal
    total_items_count: int

class OrderSummaryResponse(BaseModel):
    id: int
    customer_name: str
    status: OrderStatus
    items_total: Decimal

class ErrorResponse(BaseModel):
    detail: str
