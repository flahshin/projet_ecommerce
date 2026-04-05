from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import httpx
import os

app = FastAPI(title="Order Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL du product-service (configurée via variable d'environnement)
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product-service:8000")

# --- Modèles ---
class OrderItem(BaseModel):
    product_id: str
    quantity: int
    unit_price: Optional[float] = None

class Order(BaseModel):
    id: Optional[str] = None
    customer_name: str
    customer_email: str
    items: List[OrderItem]
    total_price: Optional[float] = None
    status: Optional[str] = "pending"

class OrderStatusUpdate(BaseModel):
    status: str  # pending, confirmed, shipped, delivered, cancelled

# --- Base de données in-memory ---
orders_db: dict[str, Order] = {}

# --- Routes ---
@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}

@app.get("/orders", response_model=List[Order])
def get_orders():
    return list(orders_db.values())

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return orders_db[order_id]

@app.post("/orders", response_model=Order, status_code=201)
async def create_order(order: Order):
    total = 0.0
    enriched_items = []

    async with httpx.AsyncClient() as client:
        for item in order.items:
            try:
                # Appel inter-service vers le product-service
                resp = await client.get(f"{PRODUCT_SERVICE_URL}/products/{item.product_id}")
                if resp.status_code == 404:
                    raise HTTPException(status_code=404, detail=f"Produit {item.product_id} non trouvé")
                product = resp.json()

                if product["stock"] < item.quantity:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Stock insuffisant pour le produit {product['name']}"
                    )

                unit_price = product["price"]
                total += unit_price * item.quantity

                # Mise à jour du stock
                await client.patch(
                    f"{PRODUCT_SERVICE_URL}/products/{item.product_id}/stock",
                    params={"quantity": -item.quantity}
                )

                enriched_items.append(OrderItem(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=unit_price
                ))
            except httpx.ConnectError:
                raise HTTPException(status_code=503, detail="Product service indisponible")

    order.id = str(uuid.uuid4())
    order.items = enriched_items
    order.total_price = round(total, 2)
    order.status = "confirmed"
    orders_db[order.id] = order
    return order

@app.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: str, update: OrderStatusUpdate):
    valid_statuses = ["pending", "confirmed", "shipped", "delivered", "cancelled"]
    if update.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Statut invalide. Valeurs: {valid_statuses}")
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    orders_db[order_id].status = update.status
    return orders_db[order_id]

@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    del orders_db[order_id]
    return {"message": "Commande supprimée"}
