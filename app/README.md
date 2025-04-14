# MitNetwork Backend

Ce document décrit l’architecture et le rôle de chaque module du backend Flask de MitNetwork.

## Structure Générale

- `app/`
  - `__init__.py` : Initialisation de l’application Flask, configuration des extensions (JWT, DB, etc).
  - `config.py` : Paramètres de configuration (DB, JWT, etc).
  - `models/` : Définition des modèles de données (SQLAlchemy).
  - `routes/` : Définition des endpoints API REST (Blueprints).
  - `services/` : Logique métier réutilisable, accès système, manipulation réseau.
  - `utils/` : Utilitaires, décorateurs, helpers.

---

## Détail des principaux modules

### 1. `models/user.py`

Définit le modèle User (utilisateur) : id, username, email, password hash, is_admin, méthodes de gestion du mot de passe.

### 2. `routes/`

- **auth.py** :
  - `/api/auth/login` : Authentification, délivre un JWT.
  - Utilise Flask-JWT-Extended.
- **users.py** :
  - `/api/users/` (GET, POST) : Liste et création d’utilisateurs (admin).
  - `/api/users/<user_id>` (DELETE) : Suppression d’un utilisateur (admin).
- **firewall.py** :
  - `/api/firewall/` (GET, POST) : Liste et modification des règles firewall (admin).
- **monitoring.py** :
  - `/api/monitoring/network` : Statistiques réseau.
  - `/api/monitoring/connections` : Connexions actives.
  - `/api/monitoring/system` : Statistiques système (CPU, RAM, etc).
- **logs.py** :
  - `/api/logs/system` : Récupère les logs système (journalctl).
  - `/api/logs/auth` : Récupère les logs d’authentification.
- **services.py** :
  - `/api/services/` : Gestion des services système (statut, start/stop/restart, etc).

### 3. `services/`

- **firewall.py** : Fonctions pour manipuler iptables (ajout/suppression de règles).
- **monitoring.py** : Fonctions pour récupérer l’état du système et du réseau.
- **network.py** : Fonctions utilitaires réseau (IP, interfaces, etc).

### 4. `utils/`

- **decorators.py** :
  - `admin_required` : Décorateur pour restreindre l’accès aux admins.
  - Autres helpers de sécurité.

---

## Sécurité

- Authentification JWT (Flask-JWT-Extended).
- Droits d’accès vérifiés via décorateurs (`jwt_required`, `admin_required`).

## Bonnes pratiques

- Chaque module est petit, dédié à une responsabilité (Single Responsibility Principle).
- Toute la logique système (firewall, monitoring) est isolée dans `services/` et jamais dans les routes directement.
- Les Blueprints Flask permettent de séparer proprement les routes par domaine.

## Pour aller plus loin

- Ajouter des tests unitaires pour chaque route et service.
- Documenter chaque endpoint (Swagger, OpenAPI).
- Ajouter la gestion fine des erreurs et des logs d’audit.

---

Pour toute question sur un module précis, consultez le code source ou demandez une explication détaillée.
