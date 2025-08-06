import os
from fastapi_cache2 import FastAPICache, cache, close_cache
from fastapi_cache2.backends.redis import RedisBackend
import redis.asyncio as redis
from functools import wraps
from typing import Callable, Any, Optional
import logging

# --- Config ---
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
CACHE_PREFIX = os.getenv("CACHE_PREFIX", "zomato-cache")
DEFAULT_TTL = int(os.getenv("DEFAULT_TTL", 300))  # 5 min default

# TTLs (seconds)
TTL = {
    "static": 1800,      # 30 min
    "dynamic": 300,      # 5 min
    "real_time": 30,     # 30 sec
    "analytics": 900,    # 15 min
    "session": 1800,     # 30 min
    "order_delivered": 3600, # 1 hour for completed orders
}

# --- Redis Setup ---
redis_client: Optional[redis.Redis] = None

def get_redis_client():
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    return redis_client

async def init_cache(app=None):
    backend = RedisBackend(get_redis_client())
    FastAPICache.init(backend, prefix=CACHE_PREFIX)

async def close_cache_connection():
    await close_cache()
    if redis_client:
        await redis_client.close()

# --- Key Builders ---
def build_key(namespace: str, *args, **kwargs):
    # Example: customers:123, orders:456, analytics:restaurants
    if 'id' in kwargs:
        return f"{namespace}:{kwargs['id']}"
    if 'customer_id' in kwargs:
        return f"{namespace}:{kwargs['customer_id']}"
    if 'restaurant_id' in kwargs:
        return f"{namespace}:{kwargs['restaurant_id']}"
    if 'order_id' in kwargs:
        return f"{namespace}:{kwargs['order_id']}"
    return f"{namespace}:*"

# --- Decorators ---
def static_cache(namespace: str, expire: int = TTL["static"], key_builder: Optional[Callable] = None):
    def decorator(func):
        return cache(namespace=namespace, expire=expire, key_builder=key_builder or build_key)(func)
    return decorator

def dynamic_cache(namespace: str, expire: int = TTL["dynamic"], key_builder: Optional[Callable] = None):
    def decorator(func):
        return cache(namespace=namespace, expire=expire, key_builder=key_builder or build_key)(func)
    return decorator

def real_time_cache(namespace: str, expire: int = TTL["real_time"], key_builder: Optional[Callable] = None):
    def decorator(func):
        return cache(namespace=namespace, expire=expire, key_builder=key_builder or build_key)(func)
    return decorator

def analytics_cache(namespace: str, expire: int = TTL["analytics"], key_builder: Optional[Callable] = None):
    def decorator(func):
        return cache(namespace=namespace, expire=expire, key_builder=key_builder or build_key)(func)
    return decorator

def session_cache(namespace: str, expire: int = TTL["session"], key_builder: Optional[Callable] = None):
    def decorator(func):
        return cache(namespace=namespace, expire=expire, key_builder=key_builder or build_key)(func)
    return decorator

def conditional_cache(namespace: str, expire: int, condition: Callable[[Any], bool], key_builder: Optional[Callable] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            if condition(result):
                return await cache(namespace=namespace, expire=expire, key_builder=key_builder or build_key)(func)(*args, **kwargs)
            return result
        return wrapper
    return decorator

# --- Invalidation Utilities ---
async def invalidate_namespace(namespace: str, pattern: str = "*"):
    client = get_redis_client()
    keys = await client.keys(f"{CACHE_PREFIX}:{namespace}:{pattern}")
    if keys:
        await client.delete(*keys)

async def invalidate_key(namespace: str, key: str):
    client = get_redis_client()
    await client.delete(f"{CACHE_PREFIX}:{namespace}:{key}")

# --- Write-through Example ---
async def write_through(namespace: str, key: str, value: Any, expire: int = DEFAULT_TTL):
    client = get_redis_client()
    await client.set(f"{CACHE_PREFIX}:{namespace}:{key}", value, ex=expire)

# --- Cache-aside Example ---
async def cache_aside(namespace: str, key: str, fallback: Callable, expire: int = DEFAULT_TTL):
    client = get_redis_client()
    cache_key = f"{CACHE_PREFIX}:{namespace}:{key}"
    cached = await client.get(cache_key)
    if cached:
        return cached
    value = await fallback()
    await client.set(cache_key, value, ex=expire)
    return value

# --- Monitoring ---
async def cache_stats():
    client = get_redis_client()
    info = await client.info()
    return {
        "memory": info.get("used_memory_human"),
        "keys": info.get("db0", {}).get("keys", 0),
        "hits": info.get("keyspace_hits"),
        "misses": info.get("keyspace_misses"),
    }

# --- Logging ---
logger = logging.getLogger("zomato.cache")
logger.setLevel(logging.INFO)