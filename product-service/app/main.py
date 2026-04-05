from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="Product Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modèles ---
class Product(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    price: float
    stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None

# --- Base de données in-memory ---
db: dict[str, Product] = {
    "p1": Product(id="p1", name="Laptop Pro", description="Laptop haute performance", price=1299.99, stock=50),
    "p2": Product(id="p2", name="Souris sans fil", description="Souris ergonomique", price=29.99, stock=200),
    "p3": Product(id="p3", name="Clavier mécanique", description="Clavier RGB tactile", price=89.99, stock=100),
}

# --- Routes ---
@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}

@app.get("/products", response_model=List[Product])
def get_products():
    return list(db.values())

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: str):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return db[product_id]

@app.post("/products", response_model=Product, status_code=201)
def create_product(product: Product):
    product.id = str(uuid.uuid4())
    db[product.id] = product
    return product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: str, update: ProductUpdate):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    existing = db[product_id]
    updated_data = existing.dict()
    for field, value in update.dict(exclude_none=True).items():
        updated_data[field] = value
    db[product_id] = Product(**updated_data)
    return db[product_id]

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    del db[product_id]
    return {"message": "Produit supprimé"}

@app.patch("/products/{product_id}/stock")
def update_stock(product_id: str, quantity: int):
    if product_id not in db:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    product = db[product_id]
    if product.stock + quantity < 0:
        raise HTTPException(status_code=400, detail="Stock insuffisant")
    product.stock += quantity
    return {"product_id": product_id, "new_stock": product.stock}
