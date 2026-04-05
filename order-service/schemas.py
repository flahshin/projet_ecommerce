from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    customer_email: str
    items: List[OrderItem] = Field(..., min_length=1)


class OrderItemOut(BaseModel):
    product_id: int
    quantity: int
    price: float


class Order(BaseModel):
    id: int
    customer_name: str
    customer_email: str
    status: str
    total_price: float
    items: list
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
