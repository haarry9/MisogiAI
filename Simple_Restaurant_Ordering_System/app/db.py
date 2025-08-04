from typing import Dict
from .models import FoodItem, Order

menu_db: Dict[int, FoodItem] = {}
orders_db: Dict[int, Order] = {}

next_menu_id = 1
next_order_id = 1
