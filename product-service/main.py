from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def seed_products() -> None:
    db = SessionLocal()
    try:
        if db.query(models.Product).count() == 0:
            defaults = [
                models.Product(
                    name="Laptop Pro",
                    description="Laptop haute performance",
                    price=1299.99,
                    stock=50,
                    category="Informatique",
                ),
                models.Product(
                    name="Souris sans fil",
                    description="Souris ergonomique",
                    price=29.99,
                    stock=200,
                    category="Accessoires",
                ),
                models.Product(
                    name="Clavier mécanique",
                    description="Clavier RGB tactile",
                    price=89.99,
                    stock=100,
                    category="Accessoires",
                ),
            ]
            db.add_all(defaults)
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    seed_products()
    yield


app = FastAPI(title="Product Service", version="1.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "product-service"}


@app.get("/products", response_model=list[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)


@app.get("/products/{product_id}", response_model=schemas.Product)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products", response_model=schemas.Product, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    updated = crud.update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")


@app.patch("/products/{product_id}/stock")
def update_stock(product_id: int, quantity: int, db: Session = Depends(get_db)):
    product = crud.update_stock(db, product_id, quantity)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product == "insufficient":
        raise HTTPException(status_code=400, detail="Insufficient stock")
    return {"message": "Stock updated", "product_id": product_id, "new_stock": product.stock}
