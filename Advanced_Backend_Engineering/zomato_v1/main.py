from fastapi import FastAPI
from .routes import router as restaurant_router
from .database import engine, Base

app = FastAPI(
    title="Zomato Restaurant Management API",
    description="API for managing restaurants (CRUD, search, filter, pagination)",
    version="1.0.0"
)

app.include_router(restaurant_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)