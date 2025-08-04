from pydantic import BaseModel, Field, validator
from typing import List, Optional
from decimal import Decimal
from enum import Enum

class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SALAD = "salad"

class FoodItem(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10, max_length=500)
    category: FoodCategory
    price: Decimal = Field(..., gt=0)
    is_available: bool = True
    preparation_time: int = Field(..., ge=1, le=120)
    ingredients: List[str] = Field(..., min_items=1)
    calories: Optional[int] = Field(None, gt=0)
    is_vegetarian: bool = False
    is_spicy: bool = False

    @validator('name')
    def name_must_be_letters_and_spaces(cls, v):
        if not v.replace(' ', '').isalpha():
            raise ValueError('Name must contain only letters and spaces')
        return v

    @validator('price')
    def price_must_be_in_range(cls, v):
        if not (Decimal('1.00') <= v <= Decimal('100.00')):
            raise ValueError('Price must be between $1.00 and $100.00')
        if v.as_tuple().exponent < -2:
            raise ValueError('Price must have at most 2 decimal places')
        return v

    @validator('is_spicy')
    def dessert_beverage_not_spicy(cls, v, values):
        category = values.get('category')
        if v and category in [FoodCategory.DESSERT, FoodCategory.BEVERAGE]:
            raise ValueError('Desserts and beverages cannot be spicy')
        return v

    @validator('ingredients')
    def must_have_ingredients(cls, v):
        if not v or len(v) < 1:
            raise ValueError('At least one ingredient is required')
        return v

    @validator('calories')
    def calories_positive_and_veg_limit(cls, v, values):
        is_veg = values.get('is_vegetarian', False)
        if v is not None:
            if v <= 0:
                raise ValueError('Calories must be positive')
            if is_veg and v >= 800:
                raise ValueError('Vegetarian items must have less than 800 calories')
        return v

    @validator('preparation_time')
    def beverage_prep_time_limit(cls, v, values):
        category = values.get('category')
        if category == FoodCategory.BEVERAGE and v > 10:
            raise ValueError('Preparation time for beverages must be 10 minutes or less')
        return v

    @property
    def price_category(self):
        if self.price < 10:
            return "Budget"
        elif self.price <= 25:
            return "Mid-range"
        else:
            return "Premium"

    @property
    def dietary_info(self):
        info = []
        if self.is_vegetarian:
            info.append("Vegetarian")
        if self.is_spicy:
            info.append("Spicy")
        return info