# 🛒 ShopMicro — E-Commerce Microservices

Projet microservices Python/FastAPI + Docker + Kubernetes + RBAC

---

## 📁 Structure du projet

```
ecommerce-microservices/
├── product-service/          # Microservice Produits (port 8000)
│   ├── app/main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── k8s/deployment.yaml
├── order-service/            # Microservice Commandes (port 8001)
│   ├── app/main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── k8s/deployment.yaml
├── frontend/                 # Interface web (port 3000)
│   ├── index.html
│   └── Dockerfile
├── k8s-global/
│   ├── rbac.yaml             # Namespace + ServiceAccounts + Roles (RBAC)
│   └── ingress.yaml          # Gateway (routage /api/products → /api/orders)
├── docker-compose.yml        # Dev local
└── README.md
```

---

## 🚀 Étape 1 — Lancer en local (sans Kubernetes) — 10/20

### Prérequis
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

---

## 🐳 Étape 2 — Publier les images sur Docker Hub

```bash
# Remplacer "votre-dockerhub" par votre username Docker Hub
docker build -t votre-dockerhub/product-service:latest ./product-service
docker build -t votre-dockerhub/order-service:latest ./order-service
docker build -t votre-dockerhub/frontend:latest ./frontend

docker push votre-dockerhub/product-service:latest
docker push votre-dockerhub/order-service:latest
docker push votre-dockerhub/frontend:latest
```

> ⚠️ Puis modifier les fichiers `k8s/deployment.yaml` des deux services :
> remplacer `votre-dockerhub` par votre vrai username.

---

## ☸️ Étape 3 — Déployer sur Kubernetes (Minikube) — 12/20

### Démarrer Minikube avec l'Ingress

```bash
minikube start
minikube addons enable ingress
```

### Appliquer les manifests dans l'ordre

```bash
# 1. Namespace + RBAC (ServiceAccounts, Roles, RoleBindings)
kubectl apply -f k8s-global/rbac.yaml

# 2. Déployer les services
kubectl apply -f product-service/k8s/deployment.yaml
kubectl apply -f order-service/k8s/deployment.yaml

# 3. Appliquer la gateway Ingress
kubectl apply -f k8s-global/ingress.yaml
```

### Ajouter le domaine local dans /etc/hosts

```bash
echo "$(minikube ip) ecommerce.local" | sudo tee -a /etc/hosts
```

### Vérifier le déploiement

```bash
kubectl get all -n ecommerce
kubectl get ingress -n ecommerce
```

L'application est accessible sur : http://ecommerce.local

---

## 🔐 RBAC — Sécurité Kubernetes — 18/20

Le fichier `k8s-global/rbac.yaml` contient :

| Ressource                | Rôle                                                          |
|--------------------------|---------------------------------------------------------------|
| `Namespace ecommerce`    | Isolation dédiée au projet                                    |
| `product-service-sa`     | ServiceAccount avec accès lecture ConfigMaps/Secrets/Pods     |
| `order-service-sa`       | ServiceAccount avec accès lecture + Services/Endpoints        |
| `ecommerce-readonly`     | ClusterRole monitoring (Pods, Services, Deployments)          |

### Vérifier les droits RBAC

```bash
# Tester que le service account NE PEUT PAS supprimer des pods
kubectl auth can-i delete pods \
  --as=system:serviceaccount:ecommerce:product-service-sa \
  -n ecommerce
# → no  ✅ (accès refusé, c'est voulu)

# Tester que le service account PEUT lire les configmaps
kubectl auth can-i get configmaps \
  --as=system:serviceaccount:ecommerce:product-service-sa \
  -n ecommerce
# → yes ✅
```

---

## 🌐 API Reference

### Product Service (port 8000)

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

## 📊 Barème visé

| Fonctionnalité                              | Points |
|---------------------------------------------|--------|
| 1 service + Dockerfile + Kubernetes         | 10/20  |
| Gateway Ingress (routage /api/...)          | 12/20  |
| 2 services + communication inter-services   | 14/20  |
| Base de données in-memory + full REST API   | 16/20  |
| RBAC Kubernetes (Roles, ServiceAccounts)    | 18/20  |

---

## 💡 Conseils pour la présentation

1. Montrer le `kubectl get all -n ecommerce` pour prouver le déploiement
2. Démontrer le `kubectl auth can-i` pour le RBAC
3. Utiliser `kubectl describe ingress -n ecommerce` pour la gateway
4. Ouvrir Swagger (`/docs`) pour montrer l'API documentée automatiquement
5. Passer une commande depuis le frontend et montrer la décrémentation du stock
