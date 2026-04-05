from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import httpx
import os
import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", version="1.0.0")

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8000")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def check_and_reserve_stock(product_id: int, quantity: int) -> dict:
    """Call product service to check and reserve stock."""
    async with httpx.AsyncClient() as client:
        # Check product exists
        resp = await client.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        product = resp.json()

        if product["stock"] < quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {product_id}. Available: {product['stock']}"
            )

        # Reserve stock (decrease)
        stock_resp = await client.patch(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}/stock",
            params={"quantity": -quantity}
        )
        if stock_resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to reserve stock")

        return product


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "order-service"}


@app.get("/orders", response_model=List[schemas.Order])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_orders(db, skip=skip, limit=limit)


@app.get("/orders/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.post("/orders", response_model=schemas.Order, status_code=201)
async def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # Validate all items and reserve stock
    total = 0.0
    for item in order.items:
        product = await check_and_reserve_stock(item.product_id, item.quantity)
        total += product["price"] * item.quantity

    return crud.create_order(db, order, total)


@app.patch("/orders/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    order = crud.update_order_status(db, order_id, status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.delete("/orders/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
