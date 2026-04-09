from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import Base, engine, get_db

# Create tables (for demo; in prod use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Products & Categories API")

# Pagination helper
def paginate(query, page: int = 1, page_size: int = 10):
    if page < 1: page = 1
    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()

# Category endpoints
@app.get("/api/categories", response_model=List[schemas.CategoryRead])
def list_categories(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    q = db.query(models.Category).order_by(models.Category.id)
    return paginate(q, page, page_size)

@app.post("/api/categories", response_model=schemas.CategoryRead, status_code=201)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    cat = models.Category(**payload.dict())
    db.add(cat); db.commit(); db.refresh(cat)
    return cat

@app.get("/api/categories/{id}", response_model=schemas.CategoryRead)
def get_category(id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Category).get(id)
    if not cat: raise HTTPException(404, "Category not found")
    return cat

@app.put("/api/categories/{id}", response_model=schemas.CategoryRead)
def update_category(id: int, payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    cat = db.query(models.Category).get(id)
    if not cat: raise HTTPException(404, "Category not found")
    for k,v in payload.dict().items(): setattr(cat, k, v)
    db.commit(); db.refresh(cat)
    return cat

@app.delete("/api/categories/{id}", status_code=204)
def delete_category(id: int, db: Session = Depends(get_db)):
    cat = db.query(models.Category).get(id)
    if not cat: raise HTTPException(404, "Category not found")
    db.delete(cat); db.commit()
    return

# Product endpoints
@app.get("/api/products", response_model=List[schemas.ProductRead])
def list_products(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    q = db.query(models.Product).order_by(models.Product.id).join(models.Category).options()
    return paginate(q, page, page_size)

@app.post("/api/products", response_model=schemas.ProductRead, status_code=201)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    # ensure category exists
    cat = db.query(models.Category).get(payload.category_id)
    if not cat: raise HTTPException(400, "Category does not exist")
    prod = models.Product(**payload.dict())
    db.add(prod); db.commit(); db.refresh(prod)
    return prod

@app.get("/api/products/{id}", response_model=schemas.ProductRead)
def get_product(id: int, db: Session = Depends(get_db)):
    prod = db.query(models.Product).get(id)
    if not prod: raise HTTPException(404, "Product not found")
    return prod

@app.put("/api/products/{id}", response_model=schemas.ProductRead)
def update_product(id: int, payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    prod = db.query(models.Product).get(id)
    if not prod: raise HTTPException(404, "Product not found")
    if not db.query(models.Category).get(payload.category_id): raise HTTPException(400, "Category does not exist")
    for k,v in payload.dict().items(): setattr(prod, k, v)
    db.commit(); db.refresh(prod)
    return prod

@app.delete("/api/products/{id}", status_code=204)
def delete_product(id: int, db: Session = Depends(get_db)):
    prod = db.query(models.Product).get(id)
    if not prod: raise HTTPException(404, "Product not found")
    db.delete(prod); db.commit()
    return
