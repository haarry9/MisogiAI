from fastapi import FastAPI
from .routes import router as restaurant_router
from .database import engine, Base
from fastapi_cache2 import FastAPICache
from fastapi_cache2.backends.redis import RedisCacheBackend
import redis.asyncio as redis
from .routes import cache_router

app = FastAPI(
    title="Zomato Restaurant Management API",
    description="API for managing restaurants (CRUD, search, filter, pagination)",
    version="1.0.0"
)

app.include_router(restaurant_router)
app.include_router(cache_router)

@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Redis and FastAPICache setup
    redis_client = redis.from_url("redis://localhost:6379/0", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisCacheBackend(redis_client), prefix="zomato-cache")