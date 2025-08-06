from fastapi import FastAPI
from .database import init_db
from .routes import customers, orders, reviews, restaurants
from . import cache as cache_utils
from fastapi import BackgroundTasks
from fastapi import Request
from .cache import cache_stats, invalidate_namespace, warm_cache

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    init_db()
    await cache_utils.init_cache(app)
    await warm_cache()

async def warm_cache():
    # Example: warm popular restaurants, trending menu items
    from .crud import get_restaurant_analytics
    from .database import SessionLocal
    db = SessionLocal()
    try:
        # Warm top 5 restaurants analytics
        for rid in range(1, 6):
            try:
                get_restaurant_analytics(db, rid)
            except Exception:
                pass
    finally:
        db.close()

@app.on_event("shutdown")
async def on_shutdown():
    await cache_utils.close_cache_connection()

app.include_router(customers.router)
app.include_router(orders.router)
app.include_router(reviews.router)
app.include_router(restaurants.router)

@app.get("/")
def root():
    return {"message": "Welcome to Zomato v3 Food Delivery API!"}

@app.get("/cache/health")
async def cache_health():
    try:
        client = get_redis_client()
        pong = await client.ping()
        return {"status": "ok" if pong else "fail"}
    except Exception as e:
        return {"status": "fail", "error": str(e)}

@app.get("/cache/stats/namespaces")
async def cache_stats_namespaces():
    return await cache_stats()

@app.get("/cache/memory-usage")
async def cache_memory():
    stats = await cache_stats()
    return {"memory": stats.get("memory")}

@app.delete("/cache/clear/expired")
async def cache_clear_expired():
    client = get_redis_client()
    await client.bgrewriteaof()  # Not a true clear, but triggers cleanup
    return {"status": "cleanup triggered"}

@app.post("/cache/warm/{namespace}")
async def cache_warm_namespace(namespace: str):
    await warm_cache()
    return {"status": f"warmed {namespace}"}

@app.get("/analytics/cache-performance")
async def analytics_cache_performance():
    stats = await cache_stats()
    return {"hits": stats.get("hits"), "misses": stats.get("misses")}