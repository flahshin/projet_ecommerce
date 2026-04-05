# 🛒 ShopMicro — E-Commerce Microservices

Projet microservices Python/FastAPI + Docker + Kubernetes + PostgreSQL + RBAC

---

## 📁 Structure du projet

```text
.
├── product-service/
├── order-service/
├── frontend/
├── k8s-global/
├── k8s/
│   └── database/
├── docker-compose.yml
└── README.md
```

---

<<<<<<< HEAD
## 🚀 Étape 1 — Lancer en local
- Docker + Docker Compose installés

```bash
cd ecommerce-microservices
docker-compose up --build
```

| Service         | URL                          |
|-----------------|------------------------------|
| Product Service | http://localhost:8000/docs   |
| Order Service   | http://localhost:8001/docs   |
| Frontend        | http://localhost:3000        |
=======

## 🚀 Lancer en local

```bash
docker compose up --build
```

### URLs

- Frontend : `http://localhost:3000`
- Product service : `http://localhost:8000/docs`
- Order service : `http://localhost:8001/docs`

---

## 🐳 Publier sur Docker Hub

```bash
docker build -t votre-dockerhub/product-service:latest ./product-service
docker build -t votre-dockerhub/order-service:latest ./order-service
docker build -t votre-dockerhub/frontend:latest ./frontend

docker push votre-dockerhub/product-service:latest
docker push votre-dockerhub/order-service:latest
docker push votre-dockerhub/frontend:latest
```

Pense à remplacer `votre-dockerhub` dans :
- `product-service/k8s/deployment.yaml`
- `order-service/k8s/deployment.yaml`
- `frontend/k8s/deployment.yaml`

---

<<<<<<< HEAD
## ☸️ Étape 3 — Déployer sur Kubernetes (Minikube) 

### Démarrer Minikube avec l'Ingress
=======
## ☸️ Déploiement Kubernetes
>>>>>>> b429136 (projet cube V2)

```bash
minikube start
minikube addons enable ingress

kubectl apply -f k8s-global/rbac.yaml
kubectl apply -f k8s/database/postgres-secret.yaml
kubectl apply -f k8s/database/postgres-products.yaml
kubectl apply -f k8s/database/postgres-orders.yaml
kubectl apply -f product-service/k8s/deployment.yaml
kubectl apply -f order-service/k8s/deployment.yaml
kubectl apply -f frontend/k8s/deployment.yaml
kubectl apply -f k8s-global/ingress.yaml
```

Ajouter ensuite dans `/etc/hosts` :

```bash
sudo tee -a /etc/hosts
```

Application : `http://ecommerce.local`

---

<<<<<<< HEAD
## 🔐 RBAC — Sécurité Kubernetes —
=======
## 🔐 Sécurité / RBAC
>>>>>>> b429136 (projet cube V2)

Le namespace, les `ServiceAccount`, les `Role`, `RoleBinding` et le `ClusterRole` sont dans `k8s-global/rbac.yaml`.

---

## 🌐 API

### Product Service

- `GET /products`
- `GET /products/{id}`
- `POST /products`
- `PUT /products/{id}`
- `DELETE /products/{id}`
- `PATCH /products/{id}/stock?quantity=N`
- `GET /health`

### Order Service

- `GET /orders`
- `GET /orders/{id}`
- `POST /orders`
- `PATCH /orders/{id}/status`
- `DELETE /orders/{id}`
- `GET /health`

Exemple body pour le statut :

```json
{
  "status": "shipped"
}
```

---

