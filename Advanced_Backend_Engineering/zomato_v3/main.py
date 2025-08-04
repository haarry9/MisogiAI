from fastapi import FastAPI
from .database import init_db
from .routes import customers, orders, reviews, restaurants

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(reviews.router)
app.include_router(restaurants.router)

@app.get("/")
def root():
    return {"message": "Welcome to Zomato v3 Food Delivery API!"}