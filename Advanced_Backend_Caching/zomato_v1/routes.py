from fastapi import APIRouter, Depends, Query, status, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from . import crud, schemas
from .database import get_db
from fastapi_cache2.decorator import cache
import time
from fastapi_cache2 import FastAPICache

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.post("/", response_model=schemas.RestaurantOut, status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: schemas.RestaurantCreate, db: AsyncSession = Depends(get_db)):
    result = await crud.create_restaurant(db, restaurant)
    # Invalidate all restaurant caches
    await FastAPICache.clear(namespace="restaurants")
    return result

@router.get("/", response_model=List[schemas.RestaurantOut])
@cache(namespace="restaurants", expire=300)
async def list_restaurants(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    start = time.perf_counter()
    result = await crud.get_restaurants(db, skip=skip, limit=limit)
    elapsed = (time.perf_counter() - start) * 1000
    cache_status = "CACHE HIT" if getattr(list_restaurants, "_fastapi_cache_hit", False) else "CACHE MISS"
    return {"data": result, "cache_status": cache_status, "response_time_ms": elapsed}

@router.get("/active", response_model=List[schemas.RestaurantOut])
@cache(namespace="restaurants", expire=240)
async def list_active_restaurants(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    start = time.perf_counter()
    result = await crud.get_active_restaurants(db, skip=skip, limit=limit)
    elapsed = (time.perf_counter() - start) * 1000
    cache_status = "CACHE HIT" if getattr(list_active_restaurants, "_fastapi_cache_hit", False) else "CACHE MISS"
    return {"data": result, "cache_status": cache_status, "response_time_ms": elapsed}

@router.get("/search", response_model=List[schemas.RestaurantOut])
@cache(namespace="restaurants", expire=180)
async def search_by_cuisine(cuisine: str, skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    start = time.perf_counter()
    result = await crud.search_restaurants_by_cuisine(db, cuisine, skip=skip, limit=limit)
    elapsed = (time.perf_counter() - start) * 1000
    cache_status = "CACHE HIT" if getattr(search_by_cuisine, "_fastapi_cache_hit", False) else "CACHE MISS"
    return {"data": result, "cache_status": cache_status, "response_time_ms": elapsed}

@router.get("/{restaurant_id}", response_model=schemas.RestaurantOut)
@cache(namespace="restaurants", expire=600)
async def get_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    start = time.perf_counter()
    result = await crud.get_restaurant(db, restaurant_id)
    elapsed = (time.perf_counter() - start) * 1000
    cache_status = "CACHE HIT" if getattr(get_restaurant, "_fastapi_cache_hit", False) else "CACHE MISS"
    return {"data": result, "cache_status": cache_status, "response_time_ms": elapsed}

@router.put("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def update_restaurant(restaurant_id: int, restaurant: schemas.RestaurantUpdate, db: AsyncSession = Depends(get_db)):
    result = await crud.update_restaurant(db, restaurant_id, restaurant)
    # Invalidate specific restaurant and list caches
    await FastAPICache.clear(namespace="restaurants")
    return result

@router.delete("/{restaurant_id}", response_model=schemas.RestaurantOut)
async def delete_restaurant(restaurant_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.delete_restaurant(db, restaurant_id)
    # Invalidate specific restaurant and list caches
    await FastAPICache.clear(namespace="restaurants")
    return result

cache_router = APIRouter(prefix="/cache", tags=["cache"])

@cache_router.get("/stats")
async def cache_stats():
    backend = FastAPICache.get_backend()
    if hasattr(backend, "redis"):
        redis_client = backend.redis
        keys = await redis_client.keys("*")
        stats = await redis_client.info()
        return {"keys": keys, "stats": stats}
    return {"error": "Not a Redis backend"}

@cache_router.delete("/clear")
async def clear_all_cache():
    await FastAPICache.clear()
    return {"message": "All cache cleared"}

@cache_router.delete("/clear/restaurants")
async def clear_restaurant_cache():
    await FastAPICache.clear(namespace="restaurants")
    return {"message": "Restaurant cache cleared"}

# Register the cache_router with the main app (FastAPI instance)
# This should be done in main.py, but for now, expose it here for clarity