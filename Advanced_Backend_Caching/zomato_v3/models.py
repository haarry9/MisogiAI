from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum
from datetime import datetime

Base = declarative_base()

class OrderStatusEnum(enum.Enum):
    placed = "placed"
    confirmed = "confirmed"
    preparing = "preparing"
    out_for_delivery = "out_for_delivery"
    delivered = "delivered"
    cancelled = "cancelled"

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    orders = relationship('Order', back_populates='customer')
    reviews = relationship('Review', back_populates='customer')

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    cuisine = Column(String)
    location = Column(String)
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    menu_items = relationship('MenuItem', back_populates='restaurant')
    orders = relationship('Order', back_populates='restaurant')
    reviews = relationship('Review', back_populates='restaurant')

class MenuItem(Base):
    __tablename__ = 'menu_items'
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)

    restaurant = relationship('Restaurant', back_populates='menu_items')
    order_items = relationship('OrderItem', back_populates='menu_item')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    order_status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.placed)
    total_amount = Column(Float, default=0.0)
    delivery_address = Column(String, nullable=False)
    special_instructions = Column(Text)
    order_date = Column(DateTime, default=datetime.utcnow)
    delivery_time = Column(DateTime)

    customer = relationship('Customer', back_populates='orders')
    restaurant = relationship('Restaurant', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")
    review = relationship('Review', back_populates='order', uselist=False)

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    menu_item_id = Column(Integer, ForeignKey('menu_items.id'))
    quantity = Column(Integer, nullable=False)
    item_price = Column(Float, nullable=False)
    special_requests = Column(Text)

    order = relationship('Order', back_populates='order_items')
    menu_item = relationship('MenuItem', back_populates='order_items')

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    order_id = Column(Integer, ForeignKey('orders.id'), unique=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship('Customer', back_populates='reviews')
    restaurant = relationship('Restaurant', back_populates='reviews')
    order = relationship('Order', back_populates='review')