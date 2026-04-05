from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    customer_email: str = Field(..., min_length=3)
    items: list[OrderItem] = Field(..., min_length=1)


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float


class OrderStatusUpdate(BaseModel):
    status: str


class Order(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    status: str
    total_price: float
    items: list[OrderItemOut]
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
