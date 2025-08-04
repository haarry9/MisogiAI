from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func
from datetime import datetime

# --- Customer CRUD ---
def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: int):
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customers(db: Session, skip=0, limit=100):
    return db.query(models.Customer).offset(skip).limit(limit).all()

def update_customer(db: Session, customer_id: int, update: schemas.CustomerUpdate):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    for k, v in update.dict(exclude_unset=True).items():
        setattr(db_customer, k, v)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if not db_customer:
        return None
    db.delete(db_customer)
    db.commit()
    return db_customer

# --- Order CRUD & Business Logic ---
def create_order(db: Session, customer_id: int, order: schemas.OrderCreate):
    db_order = models.Order(
        customer_id=customer_id,
        restaurant_id=order.restaurant_id,
        delivery_address=order.delivery_address,
        special_instructions=order.special_instructions,
        order_status=models.OrderStatusEnum.placed,
        order_date=datetime.utcnow(),
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    total = 0.0
    for item in order.order_items:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item["menu_item_id"]).first()
        if not menu_item:
            continue
        item_price = menu_item.price
        order_item = models.OrderItem(
            order_id=db_order.id,
            menu_item_id=menu_item.id,
            quantity=item["quantity"],
            item_price=item_price,
            special_requests=item.get("special_requests"),
        )
        db.add(order_item)
        total += item_price * item["quantity"]
    db_order.total_amount = total
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order_status(db: Session, order_id: int, status: schemas.OrderStatusUpdate):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    # Enforce valid status transitions
    valid_transitions = {
        "placed": ["confirmed", "cancelled"],
        "confirmed": ["preparing", "cancelled"],
        "preparing": ["out_for_delivery", "cancelled"],
        "out_for_delivery": ["delivered", "cancelled"],
        "delivered": [],
        "cancelled": [],
    }
    current = db_order.order_status.value
    new = status.order_status.value
    if new not in valid_transitions[current]:
        return None
    db_order.order_status = status.order_status
    if new == "delivered":
        db_order.delivery_time = datetime.utcnow()
    db.commit()
    db.refresh(db_order)
    return db_order

def get_customer_orders(db: Session, customer_id: int):
    return db.query(models.Order).filter(models.Order.customer_id == customer_id).all()

def get_restaurant_orders(db: Session, restaurant_id: int):
    return db.query(models.Order).filter(models.Order.restaurant_id == restaurant_id).all()

# --- Review CRUD & Business Logic ---
def create_review(db: Session, order_id: int, review: schemas.ReviewCreate):
    db_order = get_order(db, order_id)
    if not db_order or db_order.order_status != models.OrderStatusEnum.delivered:
        return None
    if db.query(models.Review).filter(models.Review.order_id == order_id).first():
        return None
    db_review = models.Review(
        customer_id=db_order.customer_id,
        restaurant_id=db_order.restaurant_id,
        order_id=order_id,
        rating=review.rating,
        comment=review.comment,
        created_at=datetime.utcnow(),
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def get_restaurant_reviews(db: Session, restaurant_id: int):
    return db.query(models.Review).filter(models.Review.restaurant_id == restaurant_id).all()

def get_customer_reviews(db: Session, customer_id: int):
    return db.query(models.Review).filter(models.Review.customer_id == customer_id).all()

# --- Analytics ---
def get_restaurant_analytics(db: Session, restaurant_id: int):
    total_orders = db.query(models.Order).filter(models.Order.restaurant_id == restaurant_id).count()
    total_revenue = db.query(func.sum(models.Order.total_amount)).filter(models.Order.restaurant_id == restaurant_id).scalar() or 0.0
    avg_rating = db.query(func.avg(models.Review.rating)).filter(models.Review.restaurant_id == restaurant_id).scalar() or 0.0
    popular_items = db.query(models.MenuItem.name, func.count(models.OrderItem.id).label('count')).join(models.OrderItem).join(models.Order).filter(models.Order.restaurant_id == restaurant_id).group_by(models.MenuItem.name).order_by(func.count(models.OrderItem.id).desc()).limit(5).all()
    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "avg_rating": avg_rating,
        "popular_items": [item[0] for item in popular_items],
    }

def get_customer_analytics(db: Session, customer_id: int):
    total_orders = db.query(models.Order).filter(models.Order.customer_id == customer_id).count()
    total_spent = db.query(func.sum(models.Order.total_amount)).filter(models.Order.customer_id == customer_id).scalar() or 0.0
    avg_rating = db.query(func.avg(models.Review.rating)).filter(models.Review.customer_id == customer_id).scalar() or 0.0
    return {
        "total_orders": total_orders,
        "total_spent": total_spent,
        "avg_rating_given": avg_rating,
    }