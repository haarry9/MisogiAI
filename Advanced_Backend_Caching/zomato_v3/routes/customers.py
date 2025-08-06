from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..database import SessionLocal
from ..cache import session_cache, invalidate_key

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/customers/", response_model=schemas.CustomerBase)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    return crud.create_customer(db, customer)

@router.get("/customers/", response_model=list[schemas.CustomerBase])
@session_cache(namespace="customers", expire=1800)
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

@router.get("/customers/{customer_id}", response_model=schemas.CustomerDetail)
@session_cache(namespace="customers", expire=1800, key_builder=lambda *a, **k: f"customer:{k['customer_id']}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.get_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

@router.put("/customers/{customer_id}", response_model=schemas.CustomerBase)
def update_customer(customer_id: int, update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = crud.update_customer(db, customer_id, update)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    # Invalidate cache
    import asyncio
    asyncio.create_task(invalidate_key("customers", f"customer:{customer_id}"))
    return db_customer

@router.delete("/customers/{customer_id}", response_model=schemas.CustomerBase)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    db_customer = crud.delete_customer(db, customer_id)
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    # Invalidate cache
    import asyncio
    asyncio.create_task(invalidate_key("customers", f"customer:{customer_id}"))
    return db_customer