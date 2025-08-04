from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from ..models import Restaurant, Order, Review, MenuItem, OrderStatusEnum
from datetime import datetime

def search_restaurants(db: Session, cuisine=None, rating=None, location=None):
    q = db.query(Restaurant)
    if cuisine:
        q = q.filter(Restaurant.cuisine.ilike(f"%{cuisine}%"))
    if rating:
        q = q.filter(Restaurant.rating >= rating)
    if location:
        q = q.filter(Restaurant.location.ilike(f"%{location}%"))
    return q.all()

def filter_orders(db: Session, status=None, start_date=None, end_date=None):
    q = db.query(Order)
    if status:
        q = q.filter(Order.order_status == status)
    if start_date:
        q = q.filter(Order.order_date >= start_date)
    if end_date:
        q = q.filter(Order.order_date <= end_date)
    return q.all()

def get_popular_menu_items(db: Session, restaurant_id: int, limit=5):
    return db.query(MenuItem.name, func.count(MenuItem.id).label('count')).join(Order.order_items).filter(Order.restaurant_id == restaurant_id).group_by(MenuItem.name).order_by(func.count(MenuItem.id).desc()).limit(limit).all()

def review_sentiment(comment: str):
    # Stub: In real world, use NLP. Here, just a placeholder.
    if not comment:
        return "neutral"
    if any(word in comment.lower() for word in ["bad", "terrible", "awful"]):
        return "negative"
    if any(word in comment.lower() for word in ["good", "great", "excellent", "amazing"]):
        return "positive"
    return "neutral"