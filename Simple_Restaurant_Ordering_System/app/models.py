from pydantic import BaseModel, Field, validator
from typing import List, Optional
from decimal import Decimal
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY = "ready"
    DELIVERED = "delivered"

class FoodItem(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal

class OrderItem(BaseModel):
    menu_item_id: int
    menu_item_name: str
    quantity: int = Field(..., gt=0, le=10)
    unit_price: Decimal

    @property
    def item_total(self) -> Decimal:
        return self.quantity * self.unit_price

class Customer(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    phone: str = Field(..., regex=r'^\d{10}$')

class Order(BaseModel):
    id: int
    customer: Customer
    items: List[OrderItem]
    status: OrderStatus = OrderStatus.PENDING

    @property
    def items_total(self) -> Decimal:
        return sum(item.item_total for item in self.items)

    @property
    def total_items_count(self) -> int:
        return sum(item.quantity for item in self.items)

    @validator('items')
    def must_have_items(cls, v):
        if not v or len(v) == 0:
            raise ValueError("Order must have at least one item.")
        return v
