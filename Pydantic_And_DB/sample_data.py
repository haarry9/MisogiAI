from models import FoodItem, FoodCategory
from decimal import Decimal

sample_menu_items = [
    FoodItem(
        id=1,
        name="Margherita Pizza",
        description="Classic pizza with tomato sauce, mozzarella cheese, and fresh basil",
        category=FoodCategory.MAIN_COURSE,
        price=Decimal("15.99"),
        preparation_time=20,
        ingredients=["pizza dough", "tomato sauce", "mozzarella", "basil", "olive oil"],
        calories=650,
        is_vegetarian=True,
        is_spicy=False
    ),
    FoodItem(
        id=2,
        name="Spicy Chicken Wings",
        description="Crispy chicken wings tossed in our signature hot sauce",
        category=FoodCategory.APPETIZER,
        price=Decimal("12.50"),
        preparation_time=15,
        ingredients=["chicken wings", "hot sauce", "butter", "celery salt"],
        calories=420,
        is_vegetarian=False,
        is_spicy=True
    ),
    # Add 3 more items as needed
]