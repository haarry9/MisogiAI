from fastapi import FastAPI
from .database import engine, Base
from .routes import restaurants, menu_items
from fastapi_cache2 import FastAPICache
from fastapi_cache2.backends.inmemory import InMemoryBackend

app = FastAPI(
    title="Zomato Restaurant-Menu System API",
    description="API for managing restaurants and menu items (CRUD, relationships, advanced queries)",
    version="2.0.0"
)

app.include_router(restaurants.router)
app.include_router(menu_items.router)

@app.on_event("startup")
async def on_startup():
    FastAPICache.init(InMemoryBackend())
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)