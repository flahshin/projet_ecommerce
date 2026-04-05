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
## ✅ Corrections apportées

- les deux microservices utilisent maintenant la **même logique de code principale**
- le `product-service` tourne bien sur la version **SQLAlchemy/PostgreSQL**
- le `order-service` accepte le **body JSON** pour la mise à jour du statut
- le frontend est aligné avec les **ID numériques** des produits et commandes
- le frontend fonctionne en **local** et derrière l'**Ingress Kubernetes**
- ajout du **frontend en Kubernetes**
- ajout du **Secret PostgreSQL** et du branchement DB dans les deployments
- ajout d'un **seed automatique** de produits pour la démo
>>>>>>> b429136 (projet cube V2)

---

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
echo "$(minikube ip) ecommerce.local" | sudo tee -a /etc/hosts
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

## 📌 Barème visé

- 2 microservices + communication inter-services
- Docker
- Kubernetes
- Ingress
- PostgreSQL
- RBAC
- Frontend

<<<<<<< HEAD
| Méthode | Endpoint                         | Description              |
|---------|----------------------------------|--------------------------|
| GET     | /products                        | Liste tous les produits  |
| GET     | /products/{id}                   | Détail d'un produit      |
| POST    | /products                        | Créer un produit         |
| PUT     | /products/{id}                   | Modifier un produit      |
| DELETE  | /products/{id}                   | Supprimer un produit     |
| PATCH   | /products/{id}/stock?quantity=N  | Modifier le stock        |
| GET     | /health                          | Health check             |

### Order Service (port 8001)

| Méthode | Endpoint                          | Description              |
|---------|-----------------------------------|--------------------------|
| GET     | /orders                           | Liste toutes les commandes |
| GET     | /orders/{id}                      | Détail d'une commande    |
| POST    | /orders                           | Créer une commande       |
| PATCH   | /orders/{id}/status               | Changer le statut        |
| DELETE  | /orders/{id}                      | Supprimer une commande   |
| GET     | /health                           | Health check             |

La documentation interactive Swagger est disponible sur `/docs` de chaque service.

---

## 🔗 Communication inter-services

Le `order-service` appelle le `product-service` via HTTP interne :
- Vérification du stock avant création de commande
- Décrémentation automatique du stock après validation

La variable d'environnement `PRODUCT_SERVICE_URL` configure l'URL :
- **Docker Compose** : `http://product-service:8000`
- **Kubernetes** : `http://product-service.ecommerce.svc.cluster.local:8000`

---

## 💡 Conseils pour la présentation

1. Montrer le `kubectl get all -n ecommerce` pour prouver le déploiement
2. Démontrer le `kubectl auth can-i` pour le RBAC
3. Utiliser `kubectl describe ingress -n ecommerce` pour la gateway
4. Ouvrir Swagger (`/docs`) pour montrer l'API documentée automatiquement
5. Passer une commande depuis le frontend et montrer la décrémentation du stock
=======
Avec cette version, le projet est beaucoup plus cohérent pour une **démo réelle**.
>>>>>>> b429136 (projet cube V2)
