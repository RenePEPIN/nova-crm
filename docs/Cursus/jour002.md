# 📅 JOUR 002 — CRUD Contacts + SQLAlchemy + Tests d’Intégration

**Date** : 1 février 2026  
**Durée estimée** : 6–8 heures  
**Niveau** : Débutant → Intermédiaire  
**Prérequis** : Jour 001 (SoC + FastAPI + /health + tests)  
**Focus** : CRUD Contacts + Base de données + contrats API + tests d’intégration

---

## 🎯 AUDIT DE COHÉRENCE

Avant de coder, vérifiez que tout est prêt :

- [ ] Vous avez terminé Jour 001 (SoC, /health, tests)
- [ ] Le backend FastAPI démarre (`python -m uvicorn ...`)
- [ ] Le dossier `backend/` existe avec `core/` et `infrastructure/`
- [ ] Vous savez où sont `dto.py`, `main.py`, `routes/`
- [ ] Votre virtualenv est activé

**Résultat attendu** : tous les checkmarks ✅

---

## 🎯 OBJECTIF UNIQUE

**Question motrice** : "Comment créer un CRUD Contacts propre, testable et aligné SoC ?"

**Réponse attendue** :
"On crée l’entité métier `Contact`, un modèle SQLAlchemy, des DTOs Pydantic, des routes CRUD, et on écrit des tests d’intégration."

**Validation de fin de journée** :

- `POST /contacts` fonctionne
- `GET /contacts` retourne des contacts
- `GET /contacts/{id}` fonctionne
- `PUT /contacts/{id}` fonctionne
- `DELETE /contacts/{id}` fonctionne
- Tests d’intégration passent ✅

---

## 🎓 THÉORIE ATOMIQUE : CRUD + Persistence

### Concept #1 : CRUD = 4 actions essentielles

| Verbe      | Action    | Endpoint                | Exemple              |
| ---------- | --------- | ----------------------- | -------------------- |
| **Create** | Créer     | `POST /contacts`        | Ajouter un contact   |
| **Read**   | Lire      | `GET /contacts`         | Lister contacts      |
| **Read**   | Lire 1    | `GET /contacts/{id}`    | Détails d’un contact |
| **Update** | Modifier  | `PUT /contacts/{id}`    | Modifier un contact  |
| **Delete** | Supprimer | `DELETE /contacts/{id}` | Supprimer un contact |

### Concept #2 : 3 couches SoC pour CRUD

```
core/domain/         → Entité Contact (métier pur)
core/use_cases/      → Logique de création, validation
infrastructure/      → BDD + API (SQLAlchemy + FastAPI)
```

**Pourquoi ?** Parce que la logique métier ne doit pas dépendre de SQLAlchemy ni FastAPI.

### Concept #3 : 2 modèles = 2 responsabilités

- **Contact (domain)** : Représente le métier (nom, email, téléphone).
- **ContactModel (SQLAlchemy)** : Représente la table SQL (colonnes, contraintes).

**Règle d’or** : l’entité métier ne connaît pas la BDD.

---

## 🌍 L’ANALOGIE : Bureau de Poste (CRUD)

Imaginez un bureau de poste :

- **Create** : vous déposez une lettre (POST)
- **Read** : vous lisez votre boîte (GET)
- **Update** : vous modifiez l’adresse (PUT)
- **Delete** : vous annulez l’envoi (DELETE)

**La BDD = le registre postal**.  
**Le backend = le guichet**.  
**Le domain = les règles postales**.

---

## 🧭 PLAN DE TRAVAIL (journée)

1. Créer l’entité métier `Contact` (domain)
2. Créer le modèle SQLAlchemy `ContactModel` (database)
3. Définir les DTOs Pydantic (HTTP)
4. Écrire les routes CRUD (HTTP)
5. Ajouter la logique métier (use_cases)
6. Écrire tests d’intégration

---

## 📝 PARTIE PRATIQUE A — Entité métier `Contact`

**Objectif** : créer la classe métier PURE.

### A1 — Créer `backend/core/domain/contact.py`

Exemple (court, lisible) :

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Contact:
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
```

**Pourquoi dataclass ?**

- Simple
- Lisible
- Immuable si besoin

**TODO Jour 003** : ajouter des validations avancées (PII, format téléphone).

---

## 📝 PARTIE PRATIQUE B — Modèle SQLAlchemy

**Objectif** : créer la table `contacts`.

### B1 — Créer `backend/infrastructure/database/models.py`

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ContactModel(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
```

**Pourquoi index/unique ?**

- `index=True` : accélère la recherche
- `unique=True` : empêche doublons email

**TODO Jour 002.5** : ajouter `created_at` et `updated_at`.

---

## 📝 PARTIE PRATIQUE C — DTOs Pydantic

**Objectif** : définir les contrats HTTP.

### C1 — Ajouter dans `backend/infrastructure/http/dto.py`

```python
from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactCreateRequest(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class ContactResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str] = None
```

**Pourquoi `EmailStr` ?** Pydantic valide l’email automatiquement.

---

## 📝 PARTIE PRATIQUE D — Use case métier

**Objectif** : encapsuler la logique (ex: vérifier doublons).

### D1 — Créer `backend/core/use_cases/create_contact.py`

```python
from core.domain.contact import Contact

class ContactService:
    def create(self, name: str, email: str, phone: str | None) -> Contact:
        # TODO JOUR 003 : Ajouter validation PII via engine
        return Contact(name=name, email=email, phone=phone)
```

**Pourquoi service ?** Facilite tests, logique isolée.

---

## 📝 PARTIE PRATIQUE E — Routes CRUD

**Objectif** : exposer API REST.

### E1 — Créer `backend/infrastructure/http/routes/contacts.py`

```python
from fastapi import APIRouter, HTTPException
from infrastructure.http.dto import ContactCreateRequest, ContactResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactResponse)
async def create_contact(contact: ContactCreateRequest):
    # TODO JOUR 002 : sauvegarder en BDD
    # TODO JOUR 003 : vérifier PII + audit
    raise HTTPException(status_code=501, detail="Not implemented")
```

**Note** : commencer par un endpoint partiel puis itérer.

### E2 — Enregistrer le routeur dans `main.py`

```python
from infrastructure.http.routes.contacts import router as contacts_router
app.include_router(contacts_router)
```

---

## 📝 PARTIE PRATIQUE F — Connexion SQLAlchemy

**Objectif** : ouvrir une session DB.

### F1 — Créer `backend/infrastructure/database/session.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Pourquoi session ?** Chaque requête API a sa session DB.

---

## 📝 PARTIE PRATIQUE G — Intégrer CRUD complet

**Objectif** : créer les vrais endpoints.

### G1 — Implémenter Create

Pseudo-étapes :

1. Ouvrir session DB
2. Vérifier email unique
3. Sauvegarder `ContactModel`
4. Retourner `ContactResponse`

### G2 — Implémenter Read (liste + détail)

### G3 — Implémenter Update

### G4 — Implémenter Delete

**TODO Jour 003** : brancher audit trail et compliance engine.

---

## 🧪 PARTIE PRATIQUE H — Tests d’intégration

**Objectif** : tester le CRUD avec TestClient + BDD.

### H1 — Créer `tests/backend/test_contacts.py`

```python
from fastapi.testclient import TestClient
from infrastructure.http.main import app

client = TestClient(app)

def test_create_contact():
    payload = {"name": "Sophie", "email": "sophie@example.com"}
    response = client.post("/contacts", json=payload)
    assert response.status_code == 201
```

**TODO Jour 002.5** : utiliser une BDD de test isolée (SQLite in-memory).

---

## ✅ CHECKLIST DE FIN DE JOURNÉE

- [ ] `Contact` créé dans domain
- [ ] `ContactModel` créé dans database
- [ ] DTOs Pydantic prêts
- [ ] Routes CRUD codées
- [ ] DB connectée (SQLAlchemy)
- [ ] Tests intégration passés

---

## 💼 ENTRETIEN — 5 QUESTIONS PIÈGES

1. **Pourquoi 2 modèles (domain + SQLAlchemy) ?**
2. **Pourquoi EmailStr dans Pydantic ?**
3. **Quelle différence entre CRUD et REST ?**
4. **Pourquoi mettre SQLAlchemy dans infrastructure/ ?**
5. **Pourquoi tester avec TestClient plutôt qu’un vrai serveur ?**

---

## 🚀 CONTINUITÉ PÉDAGOGIQUE

- Jour 001 = /health + tests unitaires
- Jour 002 = CRUD + SQLAlchemy + tests intégration
- Jour 003 = Engine IA + audit trail + PII masking

---

**FIN DE JOUR 002 ✅**
