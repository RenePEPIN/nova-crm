# 📅 JOUR 002 — CRUD Contacts + SQLAlchemy + Première Règle de Conformité

**Date** : 29 janvier 2026  
**Durée estimée** : 8-10 heures (CRUD backend + frontend + tests)  
**Environnement** : Windows 11 + WSL2 + Python 3.12.4 + FastAPI + SQLAlchemy  
**Focus** : Architecture en couches (repository pattern) + ORM + Validation Pydantic + Premier moteur IA

**Statut dans le cursus** :  
- ✅ jour001 : Infrastructure SoC + /health endpoint
- **📍 jour002 : CRUD métier + persistance**
- 📋 jour003 : Audit trail immuable + PII masking (Sprint 2 critique)
- 📋 jour004 : Authentication JWT + RBAC (Sprint 5-6 critique)

---

## 🎯 Objectif du Jour

À la fin de cette journée, vous aurez :

✅ **Sur le plan technique** :
- Table `Contact` en SQLite (structurée pour PostgreSQL migration)
- CRUD complet : POST (créer), GET (lire), PUT (modifier), DELETE (supprimer)
- Repository pattern (séparation données ↔ domaine)
- Validation Pydantic des requêtes
- Migrations Alembic (versionnage BDD)
- Tests d'intégration (API + BDD)
- Première règle IA : détection PII (emails, téléphones)

✅ **Sur le plan conceptuel** :
- Repository pattern (anti-pattern Active Record)
- SQLAlchemy ORM avantages vs SQL brut
- Alembic migrations versionnées
- Stratégie pattern pour règles IA
- Transaction ACID (atomicité)

✅ **Livrable projet** :
- `POST /api/v1/contacts` → créer contact
- `GET /api/v1/contacts/{id}` → lire contact
- `PUT /api/v1/contacts/{id}` → modifier contact
- `DELETE /api/v1/contacts/{id}` → supprimer contact
- Tests E2E pour chaque endpoint
- Première règle IA : détection emails non masqués

---

## 🎓 La Leçon du Jour : Repository Pattern & ORM

### Qu'est-ce que le Repository Pattern ?

**Définition** : Le Repository Pattern est une abstraction qui encapsule la logique d'accès aux données. La couche métier ne connaît PAS SQL ; elle communique avec le Repository (qui gère SQL).

```
Requête HTTP
    ↓
Route HTTP (infrastructure/http/routes/contacts.py)
    ↓
Use Case (core/use_cases/create_contact.py)
    ↓
Repository (infrastructure/database/contact_repository.py)  ← Seul endroit avec SQL/ORM
    ↓
Modèle SQLAlchemy (infrastructure/database/models.py)
    ↓
Base de données (SQLite → PostgreSQL)
```

### Les 3 niveaux d'accès données (du pire au meilleur)

| Approche | Problème | Exemple | Verdict |
|----------|----------|---------|---------|
| **SQL brut** (concaténation) | Injection SQL, pas de validation | `SELECT * FROM contacts WHERE id=` + id | ❌ DANGEREUX |
| **Active Record** (model = BDD) | Modèle couplé DB, migrations chaotiques | Django ORM (model fait tout) | ⚠️ Facile mais couplé |
| **Repository Pattern** (abstraction) | Modèle ≠ BDD, migration transparente | SQLAlchemy + Repository | ✅ RECOMMANDÉ |

### Pourquoi Repository Pattern pour NovaCRM ?

1. **Testabilité** : Remplacer Repository par mock dans tests (pas besoin vraie BDD)
2. **Flexibilité** : Si demain on migre SQLite → PostgreSQL → MongoDB, Repository change, use_case ne change pas
3. **Séparation des préoccupations** : Domaine ne connaît pas SQL

**Exemple concret** :

```python
# ✅ CORRECT (Repository abstrait)
class CreateContactUseCase:
    def __init__(self, repository: ContactRepository):
        self.repository = repository
    
    def execute(self, name: str, email: str) -> Contact:
        # Logique métier : aucune mention de SQL
        if not self.is_email_valid(email):
            raise ValueError("Email invalide")
        
        contact = Contact(name, email)
        self.repository.save(contact)  # Repository gère SQL
        return contact

# ❌ MAUVAIS (couplé à Django ORM)
class CreateContactView(View):
    def post(self, request):
        # SQL directement dans la vue
        Contact.objects.create(name=request.data['name'], ...)
        # Impossible à tester sans vraie BDD
```

### SQLAlchemy vs SQL brut

| Critère | SQL brut | SQLAlchemy |
|---------|----------|-----------|
| **Sécurité** | Injection SQL risquée | Requêtes paramétrées auto |
| **Maintenance** | Changement schéma = chaos | Migrations versionnées |
| **Lisibilité** | VARCHAR(255) vs 4000? | Type hints Python |
| **Testabilité** | Mock difficile | Mock facile |

---

## 🌍 L'Analogie Réelle : Le Restaurateur et le Fournisseur

### Scénario : Gestion du stock restaurant

**Sans Repository (chaotique)** :

```
Chef : "Je veux un ingredient précis"
Chef va directement au stock (entrepôt)
Chef vérifie lui-même les rayons
Chef modifie la liste (Excel improvisé)
Chef paie le fournisseur
→ Chaos : chef distrait de la cuisine, erreurs comptabilité
```

**Avec Repository (organisé)** :

```
Chef : "J'ai besoin de 5kg tomates"
Chef appelle Gestionnaire Stock (Repository)
Gestionnaire vérifie stock
Gestionnaire commande auprès fournisseur
Gestionnaire met à jour comptabilité
Chef continue cuisiner
→ Séparation des responsabilités, chef efficace
```

### Traduction pour NovaCRM

| Restaurant | NovaCRM | Rôle |
|------------|---------|------|
| **Chef** | Use Case | Logique métier (créer contact) |
| **Gestionnaire Stock** | Repository | Accès données (créer dans BDD) |
| **Stock/Rayons** | SQLAlchemy Models | Structure données |
| **Entrepôt** | Base données | Stockage physique |

**Bénéfice clé** : Si demain on change fournisseur (SQL → NoSQL), on dit au Gestionnaire "nouvelle technique", Chef continue cuisiner sans changement.

---

## 🛠️ Application au Projet : Architecture données NovaCRM

### Arborescence cible (jour002)

```
backend/
├── core/
│   ├── domain/
│   │   ├── contact.py          # ← Entité Contact (logique métier pure)
│   │   └── health.py           # (déjà existant)
│   └── use_cases/
│       ├── create_contact.py   # ← Cas d'usage : créer contact
│       ├── get_contact.py      # ← Cas d'usage : lire contact
│       ├── update_contact.py   # ← Cas d'usage : modifier contact
│       └── delete_contact.py   # ← Cas d'usage : supprimer contact
│
├── infrastructure/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py           # ← Modèles SQLAlchemy (Contact table)
│   │   ├── repository.py       # ← Interface Repository (abstraite)
│   │   ├── contact_repository.py # ← Implémentation Contact
│   │   ├── database.py         # ← Initialisation SQLAlchemy
│   │   └── migrations/         # ← Alembic (versions)
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       ├── versions/
│   │       │   └── 0001_create_contact_table.py
│   │       └── alembic.ini
│   └── http/
│       ├── routes/
│       │   ├── health.py       # (déjà existant)
│       │   └── contacts.py     # ← Routes CRUD
│       ├── dto.py              # (modifié pour ContactDTOs)
│       └── main.py             # (modifié : ajouter router contacts)
│
└── shared/
    └── exceptions.py           # (modifié : ContactNotFound, etc.)

tests/
├── backend/
│   ├── test_health.py          # (déjà existant)
│   ├── test_contact_routes.py  # ← Tests E2E CRUD
│   └── test_contact_repository.py # ← Tests unitaires repository
│
ai/
├── detectors/
│   ├── __init__.py
│   ├── base.py                 # ← Interface Detector (Strategy)
│   └── pii_detector.py         # ← Détection emails, téléphones
└── pipelines/
    └── compliance_pipeline.py   # ← Orchestration détecteurs
```

### Les 3 règles d'or de jour002

#### ✅ RÈGLE 1 : Core ne connaît pas SQLAlchemy

```python
# ✅ CORRECT (core/domain/contact.py)
from dataclasses import dataclass

@dataclass
class Contact:
    """Entité Contact - logique métier pure."""
    id: int
    name: str
    email: str
    phone: str
    # Zéro dépendance SQLAlchemy, Pydantic, FastAPI
```

```python
# ❌ INTERDIT (core/domain/contact.py)
from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase

class Contact(DeclarativeBase):  # NON ! Couplé ORM
    __tablename__ = "contacts"
    name = Column(String)
```

#### ✅ RÈGLE 2 : Repository encapsule SQL/ORM

```python
# ✅ CORRECT (infrastructure/database/contact_repository.py)
from core.domain.contact import Contact

class ContactRepository:
    """Interface abstraite - aucun détail SQL."""
    def create(self, contact: Contact) -> Contact:
        raise NotImplementedError
    
    def get_by_id(self, contact_id: int) -> Contact:
        raise NotImplementedError

class SQLAlchemyContactRepository(ContactRepository):
    """Implémentation SQLAlchemy - seule couche avec SQL."""
    def create(self, contact: Contact) -> Contact:
        db_model = ContactModel(  # SQLAlchemy Model
            name=contact.name,
            email=contact.email
        )
        self.session.add(db_model)
        self.session.commit()
        return contact
```

#### ✅ RÈGLE 3 : Routes HTTP dépendent Use Case, pas Repository

```python
# ✅ CORRECT (infrastructure/http/routes/contacts.py)
from core.use_cases.create_contact import CreateContactUseCase
from infrastructure.database.contact_repository import ContactRepository

@router.post('/contacts')
async def create_contact(dto: ContactCreateDTO):
    repository = ContactRepository()  # Injecter
    use_case = CreateContactUseCase(repository)
    contact = use_case.execute(dto.name, dto.email)
    return contact

# ❌ INTERDIT
@router.post('/contacts')
async def create_contact(dto: ContactCreateDTO):
    db_session.query(ContactModel).insert(...)  # SQL directement dans route!
```

---

## 💻 Lab Technique : CRUD Contacts + Tests

### 📋 ÉTAPE 1 : Créer entité Contact (logique métier pure)

**Fichier** : `backend/core/domain/contact.py`

```python
"""
Domaine : Entité Contact (logique métier pure).

Ce module contient la définition de Contact indépendante
de toute technologie (pas de SQLAlchemy, pas de Pydantic).

Principe SoC : Domaine ne connaît pas infra.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Contact:
    """
    Entité Contact - structure de données métier immuable.
    
    Attributs :
        id : Identifiant unique (None si pas encore créé en BDD)
        name : Nom complet du contact (> 2 caractères)
        email : Adresse email (doit être valide)
        phone : Numéro téléphone optionnel (format E.164)
        created_at : Date de création (auto-générée)
        updated_at : Date modification (auto-générée)
    """
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def is_valid(self) -> bool:
        """
        Valide le contact selon règles métier.
        
        Retour :
            True si contact respecte contraintes métier
        """
        # Nom obligatoire et > 2 caractères
        if not self.name or len(self.name) < 2:
            return False
        
        # Email obligatoire (format validé par Pydantic)
        if not self.email:
            return False
        
        return True
    
    def to_dict(self) -> dict:
        """
        Convertit en dictionnaire (sérialisation JSON).
        
        Retour :
            Dict avec tous les champs
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# TODO JOUR 003 : Créer classe Client dans core/domain/client.py
# TODO JOUR 003 : Créer classe Opportunity dans core/domain/opportunity.py
```

---

### 📋 ÉTAPE 2 : Créer modèle SQLAlchemy (infrastructure)

**Fichier** : `backend/infrastructure/database/models.py`

```python
"""
Modèles SQLAlchemy - mappage objet↔relationnel.

Ces modèles décrivent les tables SQL et leurs colonnes.
Un modèle SQLAlchemy ≠ Entité domaine (séparation intentionnelle).

Principe SoC : Infrastructure ne sort pas du database/.
"""

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import declarative_base
from datetime import datetime

# Base pour tous les modèles
Base = declarative_base()


class ContactModel(Base):
    """
    Modèle Contact - mappage table SQL ↔ classe Python.
    
    Pas de logique métier ici, seulement structure BDD.
    """
    __tablename__ = "contacts"
    
    # Colonnes
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        """Représentation texte pour debug."""
        return f"<ContactModel(id={self.id}, name={self.name}, email={self.email})>"


# TODO JOUR 002 : Créer ClientModel pour table clients
# TODO JOUR 003 : Créer OpportunityModel pour table opportunities
# TODO JOUR 004 : Créer AuditLogModel pour audit trail immuable
```

---

### 📋 ÉTAPE 3 : Créer interface Repository (abstraite)

**Fichier** : `backend/infrastructure/database/repository.py`

```python
"""
Interface Repository - abstraction accès données.

Cette interface définit COMMENT les use cases accèdent aux données,
SANS révéler les détails SQL/ORM.

Principe SoC : Interface stable, implémentation peut changer.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from core.domain.contact import Contact


class ContactRepository(ABC):
    """
    Interface pour accès aux données Contact.
    
    Tous les use cases dépendent de cette interface,
    pas de l'implémentation SQLAlchemy.
    """
    
    @abstractmethod
    def create(self, contact: Contact) -> Contact:
        """
        Crée un nouveau contact en BDD.
        
        Args :
            contact : Contact avec name, email, phone
        
        Retour :
            Contact avec id assigné
        
        Lève :
            ValueError si email déjà existe (unique constraint)
        """
        pass
    
    @abstractmethod
    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        """
        Récupère contact par ID.
        
        Args :
            contact_id : Identifiant contact
        
        Retour :
            Contact si trouvé, None sinon
        """
        pass
    
    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Contact]:
        """
        Liste tous les contacts (paginé).
        
        Args :
            skip : Nombre contacts à ignorer (offset)
            limit : Nombre contacts max retournés
        
        Retour :
            Liste de Contact (peut être vide)
        """
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Contact]:
        """
        Récupère contact par email.
        
        Args :
            email : Adresse email
        
        Retour :
            Contact si trouvé, None sinon
        """
        pass
    
    @abstractmethod
    def update(self, contact: Contact) -> Contact:
        """
        Met à jour un contact existant.
        
        Args :
            contact : Contact avec id + champs modifiés
        
        Retour :
            Contact mis à jour
        
        Lève :
            ValueError si contact.id introuvable
        """
        pass
    
    @abstractmethod
    def delete(self, contact_id: int) -> bool:
        """
        Supprime un contact par ID.
        
        Args :
            contact_id : Identifiant contact
        
        Retour :
            True si supprimé, False si introuvable
        """
        pass


# TODO JOUR 003 : Créer interface ClientRepository
```

---

### 📋 ÉTAPE 4 : Implémenter ContactRepository avec SQLAlchemy

**Fichier** : `backend/infrastructure/database/contact_repository.py`

```python
"""
Implémentation SQLAlchemy du Repository Contact.

Cette classe SEULE gère SQLAlchemy/SQL.
Les use cases n'importent JAMAIS SQLAlchemy directement.

Principe SoC : Tout le SQL ici, nulle part ailleurs.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from core.domain.contact import Contact
from infrastructure.database.models import ContactModel
from infrastructure.database.repository import ContactRepository


class SQLAlchemyContactRepository(ContactRepository):
    """
    Implémentation Repository avec SQLAlchemy ORM.
    
    Gère la conversion Contact (domaine) ↔ ContactModel (BDD).
    """
    
    def __init__(self, session: Session):
        """
        Initialise le repository avec session SQLAlchemy.
        
        Args :
            session : SQLAlchemy Session (connexion BDD)
        """
        self.session = session
    
    def create(self, contact: Contact) -> Contact:
        """
        Crée contact en BDD.
        
        Étapes :
        1. Convertir Contact (domaine) → ContactModel (ORM)
        2. Ajouter à session
        3. Commit (sauvegarder)
        4. Retourner Contact avec id assigné
        """
        try:
            # Créer modèle SQLAlchemy
            db_model = ContactModel(
                name=contact.name,
                email=contact.email,
                phone=contact.phone
            )
            
            # Ajouter et sauvegarder
            self.session.add(db_model)
            self.session.commit()
            
            # Retourner domaine avec id assigné par BDD
            contact.id = db_model.id
            contact.created_at = db_model.created_at
            contact.updated_at = db_model.updated_at
            
            return contact
        
        except IntegrityError as e:
            # Email unique violation
            self.session.rollback()
            raise ValueError(f"Email {contact.email} déjà existant") from e
    
    def get_by_id(self, contact_id: int) -> Optional[Contact]:
        """
        Récupère contact par ID.
        
        Requête SQL générée automatiquement :
        SELECT * FROM contacts WHERE id = ?
        """
        db_model = self.session.query(ContactModel).filter(
            ContactModel.id == contact_id
        ).first()
        
        if not db_model:
            return None
        
        return self._model_to_domain(db_model)
    
    def get_all(self, skip: int = 0, limit: int = 10) -> List[Contact]:
        """
        Liste tous les contacts (pagination).
        
        SQL généré : SELECT * FROM contacts LIMIT ? OFFSET ?
        """
        db_models = self.session.query(ContactModel).offset(skip).limit(limit).all()
        
        return [self._model_to_domain(model) for model in db_models]
    
    def get_by_email(self, email: str) -> Optional[Contact]:
        """
        Récupère contact par email.
        
        SQL généré : SELECT * FROM contacts WHERE email = ?
        """
        db_model = self.session.query(ContactModel).filter(
            ContactModel.email == email
        ).first()
        
        if not db_model:
            return None
        
        return self._model_to_domain(db_model)
    
    def update(self, contact: Contact) -> Contact:
        """
        Met à jour contact existant.
        
        Étapes :
        1. Vérifier que contact.id existe
        2. Modifier colonnes
        3. Commit
        """
        if contact.id is None:
            raise ValueError("Contact doit avoir un id pour update")
        
        db_model = self.session.query(ContactModel).filter(
            ContactModel.id == contact.id
        ).first()
        
        if not db_model:
            raise ValueError(f"Contact id={contact.id} introuvable")
        
        # Mettre à jour champs
        db_model.name = contact.name
        db_model.email = contact.email
        db_model.phone = contact.phone
        
        self.session.commit()
        
        # Retourner domaine mis à jour
        contact.updated_at = db_model.updated_at
        
        return contact
    
    def delete(self, contact_id: int) -> bool:
        """
        Supprime contact par ID.
        
        SQL généré : DELETE FROM contacts WHERE id = ?
        """
        db_model = self.session.query(ContactModel).filter(
            ContactModel.id == contact_id
        ).first()
        
        if not db_model:
            return False
        
        self.session.delete(db_model)
        self.session.commit()
        
        return True
    
    def _model_to_domain(self, db_model: ContactModel) -> Contact:
        """
        Convertit ContactModel (ORM) → Contact (domaine).
        
        Cette méthode private encapsule la conversion.
        """
        return Contact(
            id=db_model.id,
            name=db_model.name,
            email=db_model.email,
            phone=db_model.phone,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at,
        )


# TODO JOUR 003 : Implémenter SQLAlchemyClientRepository
```

---

### 📋 ÉTAPE 5 : Créer Use Cases (logique métier)

**Fichier** : `backend/core/use_cases/create_contact.py`

```python
"""
Use Case : Créer contact.

Logique métier PURE :
- Valider contact
- Intégrer règles métier (emails uniques)
- Déléguer persistance au Repository

Pas de SQL, pas de HTTP, pas de BDD ici.
"""

from core.domain.contact import Contact
from infrastructure.database.repository import ContactRepository


class CreateContactUseCase:
    """
    Cas d'usage : créer un nouveau contact CRM.
    
    Dépend du Repository (inversion de dépendance).
    Peut être testé sans vraie BDD (mock Repository).
    """
    
    def __init__(self, repository: ContactRepository):
        """
        Initialise use case avec un repository.
        
        Args :
            repository : ContactRepository (injection de dépendance)
        """
        self.repository = repository
    
    def execute(self, name: str, email: str, phone: str = None) -> Contact:
        """
        Exécute la création de contact.
        
        Étapes :
        1. Valider saisie utilisateur
        2. Vérifier email unique
        3. Créer Contact (domaine)
        4. Persister via Repository
        5. Retourner Contact créé
        
        Args :
            name : Nom du contact
            email : Email du contact
            phone : Téléphone optionnel
        
        Retour :
            Contact créé avec id assigné
        
        Lève :
            ValueError si validation échoue
        """
        # Valider inputs
        if not name or len(name.strip()) < 2:
            raise ValueError("Nom doit avoir au minimum 2 caractères")
        
        if not email or "@" not in email:
            raise ValueError("Email invalide")
        
        # Vérifier unicité email
        existing = self.repository.get_by_email(email)
        if existing:
            raise ValueError(f"Email {email} déjà utilisé par contact id={existing.id}")
        
        # Créer entité métier
        contact = Contact(
            name=name.strip(),
            email=email.lower(),
            phone=phone
        )
        
        # Valider selon règles métier
        if not contact.is_valid():
            raise ValueError("Contact invalide selon règles métier")
        
        # Persister
        created = self.repository.create(contact)
        
        return created


# TODO JOUR 003 : Créer GetContactUseCase
# TODO JOUR 003 : Créer UpdateContactUseCase
# TODO JOUR 003 : Créer DeleteContactUseCase
```

---

### 📋 ÉTAPE 6 : Créer DTOs Pydantic (requête/réponse)

**Fichier** : `backend/infrastructure/http/dto.py` (AJOUTER à la fin)

```python
# ===== DTOs CONTACT =====

class ContactCreateRequest(BaseModel):
    """
    Schéma requête POST /contacts.
    
    Pydantic valide automatiquement :
    - name : string obligatoire
    - email : string format email (vérification @)
    - phone : string optionnel
    """
    name: str = Field(..., min_length=2, max_length=255, description="Nom du contact")
    email: EmailStr = Field(..., description="Email du contact (validé)")
    phone: Optional[str] = Field(None, max_length=20, description="Téléphone optionnel")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Sophie Martin",
                "email": "sophie.martin@example.com",
                "phone": "+33612345678"
            }
        }


class ContactResponse(BaseModel):
    """
    Schéma réponse GET /contacts/{id}.
    
    Retourné après création/lecture/modification.
    """
    id: int = Field(..., description="ID unique")
    name: str
    email: EmailStr
    phone: Optional[str] = None
    created_at: str = Field(..., description="ISO 8601 timestamp")
    updated_at: str = Field(..., description="ISO 8601 timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Sophie Martin",
                "email": "sophie.martin@example.com",
                "phone": "+33612345678",
                "created_at": "2026-01-29T10:15:23.123456",
                "updated_at": "2026-01-29T10:15:23.123456"
            }
        }


class ContactUpdateRequest(BaseModel):
    """
    Schéma requête PUT /contacts/{id}.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Sophie Martin-Dupont",
                "phone": "+33698765432"
            }
        }


# TODO JOUR 003 : Créer ClientCreateRequest, ClientResponse, ClientUpdateRequest
```

---

### 📋 ÉTAPE 7 : Créer routes HTTP (CRUD)

**Fichier** : `backend/infrastructure/http/routes/contacts.py`

```python
"""
Routes HTTP pour CRUD Contacts.

Points d'accès disponibles :
- POST /api/v1/contacts : créer contact
- GET /api/v1/contacts/{id} : lire contact
- GET /api/v1/contacts : lister contacts
- PUT /api/v1/contacts/{id} : modifier contact
- DELETE /api/v1/contacts/{id} : supprimer contact

Principe SoC : Routes orchestrent use cases.
Ne contiennent PAS de logique métier (celle-ci est dans use_cases/).
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from infrastructure.http.dto import (
    ContactCreateRequest,
    ContactUpdateRequest,
    ContactResponse,
)
from core.use_cases.create_contact import CreateContactUseCase
from infrastructure.database.contact_repository import SQLAlchemyContactRepository
from infrastructure.database.database import get_db

# Créer routeur avec préfixe /contacts
router = APIRouter(
    prefix="/api/v1/contacts",
    tags=["contacts"]
)


@router.post("", response_model=ContactResponse)
async def create_contact(
    request: ContactCreateRequest,
    db: Session = Depends(get_db)
) -> ContactResponse:
    """
    Créer un nouveau contact.
    
    Méthode HTTP : POST /api/v1/contacts
    
    Requête :
    ```json
    {
      "name": "Sophie Martin",
      "email": "sophie@example.com",
      "phone": "+33612345678"
    }
    ```
    
    Réponse : 201 Created
    ```json
    {
      "id": 1,
      "name": "Sophie Martin",
      "email": "sophie@example.com",
      "phone": "+33612345678",
      "created_at": "2026-01-29T10:15:23.123456",
      "updated_at": "2026-01-29T10:15:23.123456"
    }
    ```
    
    Erreurs :
    - 422 Unprocessable Entity : email invalide
    - 409 Conflict : email déjà utilisé
    """
    try:
        # Injecter Repository
        repository = SQLAlchemyContactRepository(db)
        
        # Créer Use Case
        use_case = CreateContactUseCase(repository)
        
        # Exécuter logique métier
        contact = use_case.execute(
            name=request.name,
            email=request.email,
            phone=request.phone
        )
        
        # Retourner réponse (Pydantic serialise automatiquement)
        return ContactResponse(
            id=contact.id,
            name=contact.name,
            email=contact.email,
            phone=contact.phone,
            created_at=contact.created_at.isoformat(),
            updated_at=contact.updated_at.isoformat()
        )
    
    except ValueError as e:
        # Logique métier violation (ex: email unique)
        raise HTTPException(status_code=409, detail=str(e))


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int,
    db: Session = Depends(get_db)
) -> ContactResponse:
    """
    Récupère contact par ID.
    
    Méthode HTTP : GET /api/v1/contacts/1
    
    Réponse : 200 OK
    
    Erreurs :
    - 404 Not Found : contact inexistant
    """
    repository = SQLAlchemyContactRepository(db)
    contact = repository.get_by_id(contact_id)
    
    if not contact:
        raise HTTPException(status_code=404, detail=f"Contact id={contact_id} introuvable")
    
    return ContactResponse(
        id=contact.id,
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        created_at=contact.created_at.isoformat(),
        updated_at=contact.updated_at.isoformat()
    )


@router.get("", response_model=list[ContactResponse])
async def list_contacts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> list[ContactResponse]:
    """
    Liste tous les contacts (paginé).
    
    Méthode HTTP : GET /api/v1/contacts?skip=0&limit=10
    
    Retour : 200 OK avec liste contacts
    """
    repository = SQLAlchemyContactRepository(db)
    contacts = repository.get_all(skip=skip, limit=limit)
    
    return [
        ContactResponse(
            id=c.id,
            name=c.name,
            email=c.email,
            phone=c.phone,
            created_at=c.created_at.isoformat(),
            updated_at=c.updated_at.isoformat()
        )
        for c in contacts
    ]


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    contact_id: int,
    request: ContactUpdateRequest,
    db: Session = Depends(get_db)
) -> ContactResponse:
    """
    Met à jour un contact.
    
    Méthode HTTP : PUT /api/v1/contacts/1
    
    Requête : Champs optionnels (envoyer seulement ce qui change)
    ```json
    {
      "name": "Sophie Martin-Dupont"
    }
    ```
    
    Réponse : 200 OK avec contact mis à jour
    
    Erreurs :
    - 404 Not Found
    - 409 Conflict (email déjà utilisé)
    """
    repository = SQLAlchemyContactRepository(db)
    existing = repository.get_by_id(contact_id)
    
    if not existing:
        raise HTTPException(status_code=404, detail=f"Contact id={contact_id} introuvable")
    
    # Mettre à jour seulement champs fournis
    if request.name:
        existing.name = request.name
    if request.email:
        existing.email = request.email
    if request.phone:
        existing.phone = request.phone
    
    try:
        updated = repository.update(existing)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    
    return ContactResponse(
        id=updated.id,
        name=updated.name,
        email=updated.email,
        phone=updated.phone,
        created_at=updated.created_at.isoformat(),
        updated_at=updated.updated_at.isoformat()
    )


@router.delete("/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db)
) -> dict:
    """
    Supprime un contact.
    
    Méthode HTTP : DELETE /api/v1/contacts/1
    
    Réponse : 200 OK
    ```json
    {"message": "Contact id=1 supprimé"}
    ```
    
    Erreurs :
    - 404 Not Found
    """
    repository = SQLAlchemyContactRepository(db)
    
    if not repository.delete(contact_id):
        raise HTTPException(status_code=404, detail=f"Contact id={contact_id} introuvable")
    
    return {"message": f"Contact id={contact_id} supprimé"}


# TODO JOUR 003 : Ajouter routes Clients
# TODO JOUR 004 : Ajouter authentication/authorization
```

---

### 📋 ÉTAPE 8 : Initialiser SQLAlchemy + session

**Fichier** : `backend/infrastructure/database/database.py`

```python
"""
Configuration SQLAlchemy - connexion BDD + session.

Gère :
- Création engine (connexion BDD)
- SessionLocal (factory sessions)
- Créer tables au démarrage
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

# URL BDD (SQLite en dev, PostgreSQL en prod)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./nova_crm.db"  # Valeur par défaut dev
)

# Créer engine (connexion pool)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Factory sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    """
    Crée toutes les tables (si elles n'existent pas).
    
    À appeler une seule fois au démarrage.
    """
    from infrastructure.database.models import Base
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """
    Dépendance FastAPI : injecte session BDD dans routes.
    
    Usage :
    @router.get('/contacts/{id}')
    def get_contact(contact_id: int, db: Session = Depends(get_db)):
        ...
    
    FastAPI appelle get_db() automatiquement à chaque requête.
    Retour :
        Session SQLAlchemy
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Fermer connexion proprement


# TODO JOUR 003 : Intégrer Alembic (migrations versionnées)
```

---

### 📋 ÉTAPE 9 : Enregistrer routes dans app FastAPI

**Fichier** : `backend/infrastructure/http/main.py` (MODIFIER)

```python
# === Dans la section "ENREGISTREMENT DES ROUTES" ===

# Importer routeur contacts
from infrastructure.http.routes.contacts import router as contacts_router

# Enregistrer routeur /contacts
app.include_router(contacts_router)

# === Au démarrage, créer les tables ===

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    # ... (log startup existant) ...
    
    # Créer tables SQLAlchemy
    from infrastructure.database.database import init_db
    init_db()
    logger.info("✅ Tables BDD créées (si nécessaire)")
    
    # ... (reste startup) ...
    yield
    # === SHUTDOWN ===
```

---

### 📋 ÉTAPE 10 : Tester CRUD avec pytest

**Fichier** : `tests/backend/test_contact_routes.py`

```python
"""
Tests d'intégration : routes CRUD Contacts.

Teste sans vraie BDD (SQLite en mémoire).
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from infrastructure.http.main import app
from infrastructure.database.models import Base
from infrastructure.database.database import get_db


# === CONFIGURATION TESTS ===

@pytest.fixture
def test_db():
    """
    Crée BDD en mémoire pour tests.
    
    Chaque test a sa propre BDD isolée.
    """
    # Créer engine en mémoire
    engine = create_engine("sqlite:///:memory:")
    
    # Créer tables
    Base.metadata.create_all(bind=engine)
    
    # Créer session factory
    TestingSessionLocal = sessionmaker(bind=engine)
    
    # Overrider dépendance FastAPI
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Crée client HTTP pour tests."""
    return TestClient(app)


# === TESTS CREATE ===

class TestCreateContact:
    """Suite tests POST /contacts"""
    
    def test_create_contact_success(self, client):
        """Crée contact avec données valides."""
        response = client.post(
            "/api/v1/contacts",
            json={
                "name": "Sophie Martin",
                "email": "sophie@example.com",
                "phone": "+33612345678"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Sophie Martin"
        assert data["email"] == "sophie@example.com"
        assert data["id"] is not None
    
    def test_create_contact_email_invalid(self, client):
        """Rejette email invalide."""
        response = client.post(
            "/api/v1/contacts",
            json={
                "name": "Sophie",
                "email": "pas-un-email",  # ← Pas @
                "phone": None
            }
        )
        
        assert response.status_code == 422  # Pydantic validation error
    
    def test_create_contact_email_duplicate(self, client):
        """Rejette email duplicata."""
        # Créer premier contact
        client.post(
            "/api/v1/contacts",
            json={
                "name": "Sophie",
                "email": "sophie@example.com"
            }
        )
        
        # Tenter créer deuxième avec même email
        response = client.post(
            "/api/v1/contacts",
            json={
                "name": "Sophie Autre",
                "email": "sophie@example.com"  # ← Duplicate
            }
        )
        
        assert response.status_code == 409  # Conflict


# === TESTS READ ===

class TestGetContact:
    """Suite tests GET /contacts/{id}"""
    
    def test_get_contact_exists(self, client):
        """Récupère contact existant."""
        # Créer contact
        create_response = client.post(
            "/api/v1/contacts",
            json={"name": "Sophie", "email": "sophie@example.com"}
        )
        contact_id = create_response.json()["id"]
        
        # Récupérer
        response = client.get(f"/api/v1/contacts/{contact_id}")
        
        assert response.status_code == 200
        assert response.json()["name"] == "Sophie"
    
    def test_get_contact_not_found(self, client):
        """Retourne 404 contact inexistant."""
        response = client.get("/api/v1/contacts/999")
        
        assert response.status_code == 404


# === TESTS LIST ===

class TestListContacts:
    """Suite tests GET /contacts"""
    
    def test_list_contacts_empty(self, client):
        """Liste vide initialement."""
        response = client.get("/api/v1/contacts")
        
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_contacts_pagination(self, client):
        """Pagination fonctionne."""
        # Créer 3 contacts
        for i in range(3):
            client.post(
                "/api/v1/contacts",
                json={
                    "name": f"Contact {i}",
                    "email": f"contact{i}@example.com"
                }
            )
        
        # Lister avec limit=2
        response = client.get("/api/v1/contacts?skip=0&limit=2")
        
        assert response.status_code == 200
        assert len(response.json()) == 2


# === TESTS UPDATE ===

class TestUpdateContact:
    """Suite tests PUT /contacts/{id}"""
    
    def test_update_contact_success(self, client):
        """Met à jour contact."""
        # Créer
        create_response = client.post(
            "/api/v1/contacts",
            json={"name": "Sophie", "email": "sophie@example.com"}
        )
        contact_id = create_response.json()["id"]
        
        # Modifier
        response = client.put(
            f"/api/v1/contacts/{contact_id}",
            json={"name": "Sophie Martin"}
        )
        
        assert response.status_code == 200
        assert response.json()["name"] == "Sophie Martin"
    
    def test_update_contact_not_found(self, client):
        """Retourne 404 si contact inexistant."""
        response = client.put(
            "/api/v1/contacts/999",
            json={"name": "Non Existant"}
        )
        
        assert response.status_code == 404


# === TESTS DELETE ===

class TestDeleteContact:
    """Suite tests DELETE /contacts/{id}"""
    
    def test_delete_contact_success(self, client):
        """Supprime contact."""
        # Créer
        create_response = client.post(
            "/api/v1/contacts",
            json={"name": "Sophie", "email": "sophie@example.com"}
        )
        contact_id = create_response.json()["id"]
        
        # Supprimer
        response = client.delete(f"/api/v1/contacts/{contact_id}")
        
        assert response.status_code == 200
        
        # Vérifier suppression
        get_response = client.get(f"/api/v1/contacts/{contact_id}")
        assert get_response.status_code == 404
    
    def test_delete_contact_not_found(self, client):
        """Retourne 404 si contact inexistant."""
        response = client.delete("/api/v1/contacts/999")
        
        assert response.status_code == 404
```

**Exécuter les tests** :

```powershell
(.venv) PS C:\Perso\nova-crm> pip install pytest pytest-asyncio
(.venv) PS C:\Perso\nova-crm> pytest tests/backend/test_contact_routes.py -v

# Sortie attendue :
# tests/backend/test_contact_routes.py::TestCreateContact::test_create_contact_success PASSED
# tests/backend/test_contact_routes.py::TestCreateContact::test_create_contact_email_invalid PASSED
# tests/backend/test_contact_routes.py::TestCreateContact::test_create_contact_email_duplicate PASSED
# tests/backend/test_contact_routes.py::TestGetContact::test_get_contact_exists PASSED
# ... (autres tests) ...
# ==================== 12+ passed ====================
```

---

### 📋 ÉTAPE 11 : Ajouter première règle PII (Engine IA)

**Fichier** : `backend/ai/detectors/base.py`

```python
"""
Classe abstraite Detector - interface pour tous les détecteurs IA.

Utilise Strategy pattern : chaque règle IA est une stratégie interchangeable.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Finding:
    """
    Résultat de détection : problème trouvé.
    
    Attributs :
        rule_id : Identifiant règle (ex: "no_pii_in_text")
        severity : Sévérité ("info", "warning", "error", "critical")
        message : Description humaine du problème
        snippet : Texte concerné (masqué pour PII)
        action : Action recommandée (ex: "mask", "reject")
    """
    rule_id: str
    severity: str  # "info" | "warning" | "error" | "critical"
    message: str
    snippet: str
    action: str  # "mask" | "reject" | "log" | "quarantine"


class Detector(ABC):
    """
    Interface abstraite pour détecteurs (Strategy pattern).
    
    Chaque Detector est une règle isolée qu'on peut ajouter/enlever
    sans impact sur les autres. 
    
    Exemple : PiiDetector, SecretsDetector, ScopeDetector, etc.
    """
    
    @abstractmethod
    def detect(self, text: str) -> List[Finding]:
        """
        Analyse texte et retourne problèmes détectés.
        
        Args :
            text : Contenu à analyser
        
        Retour :
            Liste Finding (peut être vide si aucun problème)
        """
        pass


# TODO JOUR 003 : Créer SecretsDetector (clés API)
# TODO JOUR 003 : Créer ScopeDetector (violations RBAC)
```

**Fichier** : `backend/ai/detectors/pii_detector.py`

```python
"""
Détecteur PII (Personally Identifiable Information).

Détecte emails et téléphones non masqués.

Règles :
- Email : pattern xxx@yyy.zzz
- Téléphone : E.164 format (+33..., 06...)
"""

import re
from typing import List
from ai.detectors.base import Detector, Finding


class PiiDetector(Detector):
    """
    Détecteur PII - repère emails et téléphones.
    
    Patterns :
    - Email : \S+@\S+\.\S+ (simplifié, pour démo)
    - Téléphone : +33\d{9} ou 06\d{8}
    """
    
    def __init__(self):
        """Initialise patterns regex."""
        # Pattern email (simplifié)
        self.email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        
        # Pattern téléphone France
        self.phone_pattern = re.compile(r'\+33\d{9}|06\d{8}|07\d{8}')
    
    def detect(self, text: str) -> List[Finding]:
        """
        Détecte PII dans texte.
        
        Args :
            text : Contenu à scanner
        
        Retour :
            Liste Finding (emails + téléphones trouvés)
        """
        findings = []
        
        # Détecter emails
        for match in self.email_pattern.finditer(text):
            email = match.group()
            findings.append(Finding(
                rule_id="pii_email",
                severity="warning",
                message=f"Email détecté non masqué : {email}",
                snippet=email,  # Pour démo (en prod: masquer)
                action="mask"
            ))
        
        # Détecter téléphones
        for match in self.phone_pattern.finditer(text):
            phone = match.group()
            findings.append(Finding(
                rule_id="pii_phone",
                severity="warning",
                message=f"Téléphone détecté non masqué : {phone}",
                snippet=phone,
                action="mask"
            ))
        
        return findings


# TODO JOUR 003 : Ajouter détection SSN (numéro sécu)
# TODO JOUR 003 : Ajouter détection IBAN/numéros cartes
```

**Fichier** : `backend/ai/pipelines/compliance_pipeline.py`

```python
"""
Pipeline Compliance - orchestre tous les détecteurs.

Factory pattern : crée les détecteurs et les exécute en séquence.
"""

from typing import List
from ai.detectors.base import Detector, Finding
from ai.detectors.pii_detector import PiiDetector


class CompliancePipeline:
    """
    Pipeline qui orchestre tous les détecteurs (Strategy).
    
    Jour 002 : Seulement PiiDetector
    Jour 003 : Ajouter SecretsDetector, ScopeDetector
    """
    
    def __init__(self, detectors: List[Detector] = None):
        """
        Initialise pipeline avec détecteurs.
        
        Args :
            detectors : Liste Detector (None = créer defaults)
        """
        if detectors is None:
            # Factory : créer détecteurs par défaut
            self.detectors = [
                PiiDetector(),
                # TODO JOUR 003 : SecretsDetector()
                # TODO JOUR 003 : ScopeDetector()
            ]
        else:
            self.detectors = detectors
    
    def analyze(self, text: str) -> dict:
        """
        Analyse texte avec tous les détecteurs.
        
        Args :
            text : Contenu à analyser
        
        Retour :
            {
                "overall_risk": "high" | "medium" | "low",
                "findings": [Finding, ...],
                "actions": ["mask", "reject", ...]
            }
        """
        all_findings = []
        
        # Exécuter tous les détecteurs
        for detector in self.detectors:
            findings = detector.detect(text)
            all_findings.extend(findings)
        
        # Déterminer risque global
        if any(f.severity == "critical" for f in all_findings):
            overall_risk = "critical"
        elif any(f.severity == "error" for f in all_findings):
            overall_risk = "high"
        elif any(f.severity == "warning" for f in all_findings):
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        return {
            "overall_risk": overall_risk,
            "findings": all_findings,
            "actions": list(set(f.action for f in all_findings))  # Unique actions
        }


# TODO JOUR 003 : Créer endpoint /compliance/check
# TODO JOUR 003 : Intégrer audit trail
# TODO JOUR 004 : Ajouter masking/redaction
```

**Test PII Detector** :

```powershell
(.venv) PS C:\Perso\nova-crm> python -c "
from ai.detectors.pii_detector import PiiDetector

detector = PiiDetector()
text = 'Contact Sophie Martin au sophie@example.com ou 0612345678'
findings = detector.detect(text)

for finding in findings:
    print(f'{finding.rule_id}: {finding.message}')
"

# Sortie :
# pii_email: Email détecté non masqué : sophie@example.com
# pii_phone: Téléphone détecté non masqué : 0612345678
```

---

### 📋 ÉTAPE 12 : Commit Git jour002

```powershell
(.venv) PS C:\Perso\nova-crm> git add .
(.venv) PS C:\Perso\nova-crm> git commit -m "Jour 002 : CRUD Contacts + SQLAlchemy + Première règle PII

✅ Repository pattern : séparation domaine ↔ infra
✅ SQLAlchemy ORM + models Contact + migrations Alembic
✅ CRUD complet : POST/GET/PUT/DELETE /api/v1/contacts
✅ DTOs Pydantic validation
✅ Tests E2E (12+ tests)
✅ Première règle IA : PiiDetector (emails, téléphones)
✅ Pipeline Compliance orchestre détecteurs

Prêt pour Jour 003 : Audit trail immuable + PII masking"
```

---

## 💼 Le Coin du Recruteur — 5 Questions/Réponses Types

### **Q1 : "Explique le Repository Pattern. Pourquoi l'utiliser plutôt que SQL brut?"**

**Réponse d'expert** :

> "Le Repository Pattern est une abstraction qui encapsule la logique d'accès aux données. Au lieu que mes Use Cases parlent directement à la BDD, ils parlent à un Repository.
>
> **Exemple concret** :
> 
> Sans Repository (couplé) :
> ```python
> # Dans ma route ou use case
> contact = db.query(ContactModel).filter(id=1).first()  # SQL ici!
> # Problème : Use Case connaît SQLAlchemy
> # Si je change ORM ou BDD → refactoriser partout
> ```
>
> Avec Repository (découplé) :
> ```python
> # Interface
> repository.get_by_id(1)  # Pas de SQL visible
> # Implémentation encapsule SQLAlchemy
> # Si je change ORM → seulement le Repository change
> ```
>
> **3 avantages majeurs** :
> 1. **Testabilité** : Remplacer Repository par mock dans tests (pas besoin BDD réelle)
> 2. **Maintenabilité** : Change ORM/BDD sans toucher domaine
> 3. **Flexibilité** : Ajouter cache/logging au Repository sans refactor Use Cases
>
> **Pour NovaCRM** : On migrera SQLite → PostgreSQL en Jour 8. Avec Repository, c'est 1 ligne changée. Sans Repository, chaos total."

---

### **Q2 : "SQLAlchemy ORM vs SQL brut - quel compromis?"**

**Réponse d'expert** :

> "SQLAlchemy ORM est **70% plus facile** que SQL brut, mais **20% plus lent** (négligeable pour CRM).
>
> **Comparaison** :
>
> | Critère | SQL brut | SQLAlchemy |
> |---------|----------|-----------|
> | Sécurité | Injection SQL risquée | Requêtes paramétrées auto |
> | Migrations | Chaos (personne sait schéma) | Alembic versionnée |
> | Joins | N+1 queries facile | Eager loading option |
> | Testabilité | Difficile (mock SQL?) | Facile (mock ORM) |
> | Perf | Rapide si optimisé | 5-10% overhead |
> | Maintenabilité | Bas (SQL legacy) | Haut (type-safe) |
>
> **Pour NovaCRM** : SQLAlchemy gagne. Pourquoi?
> - Jour 8 migration SQLite → PostgreSQL = 1 config change
> - Joins nombreux (Contacts + Audit + Compliance)
> - Tests sans BDD réelle (crucial)
>
> **Compromis accepté** : 10% perf pour 70% facilité dev."

---

### **Q3 : "Qu'est-ce qu'une migration Alembic? Pourquoi versionnée?"**

**Réponse d'expert** :

> "Migration Alembic = historique versionnée du schéma BDD.
>
> **Problème sans migrations** :
> ```
> Jour 1 : CREATE TABLE contacts (name VARCHAR(100))
> Jour 5 : Ajouter colonne email → ALTER TABLE contacts ADD COLUMN email VARCHAR(255)
> Jour 10 : Augmenter name → ALTER TABLE contacts MODIFY name VARCHAR(255)
> Jour 20 : Déployer en prod
> → Quelle version de schéma est en prod? Personne le sait.
> ```
>
> **Solution Alembic** :
> ```
> Version 0001: CREATE TABLE contacts (name VARCHAR(100))
> Version 0002: ALTER TABLE contacts ADD COLUMN email VARCHAR(255)
> Version 0003: ALTER TABLE contacts MODIFY name VARCHAR(255)
>
> Prod en V0003, dev en V0003, staging en V0002 → problème vite détecté
> ```
>
> **Pour NovaCRM** :
> - Jour 2 : V0001 (contacts table)
> - Jour 3 : V0002 (ajouter audit_log table)
> - Jour 8 : Migration SQLite → PostgreSQL (réévaluation versions)
> - Jour 12 : V0005+ (schema final)"

---

### **Q4 : "Pydantic valide comment? Où s'arrête la validation?"**

**Réponse d'expert** :

> "Pydantic valide à l'**entrée HTTP** (frontière API). Une fois parsée, données sont **trustées**.
>
> **Flux validation** :
>
> ```
> Requête HTTP (JSON)
>   ↓ Pydantic parse + valide
> ContactCreateRequest (DTO)
>   ↓ FastAPI injecte dans route
> Route reçoit données valides
>   ↓ Passe au Use Case
> Use Case applique logique métier (autre couche validation)
>   ↓ Repository persiste
> ```
>
> **Validation 3 niveaux** :
> 1. **Pydantic** : Format email, longueur, types (HTTP layer)
> 2. **Use Case** : Règles métier (email unique, nom>2 car) (domain layer)
> 3. **Repository** : Contraintes DB (unique constraint, foreign keys) (data layer)
>
> **Exemple** : Email
> ```
> Requête: {\"email\": \"pas-un-email\"} ← Attaquant
>   ↓ Pydantic: EmailStr validation échoue
> Erreur 422 Unprocessable Entity ← Attaquant rejeté immédiatement
> 
> Requête: {\"email\": \"sophie@example.com\"} ← Valide
>   ↓ Pydantic: ✅ Format OK
> Route reçoit email valide
>   ↓ Use Case: Vérifier email unique
>   ↓ Si duplicate: ValueError
> HTTP 409 Conflict ← Métier reject
> ```
>
> **Pourquoi 3 niveaux?** Chacun a responsabilité :
> - Pydantic = «Ce qu'on accepte comme HTTP»
> - Use Case = «Ce qu'on permet métier»
> - DB = «Ce qu'on peut stocker»"

---

### **Q5 : "Tests avec BDD en mémoire - comment ça marche?"**

**Réponse d'expert** :

> "Tests d'intégration NE passent pas par vraie BDD (trop lent). À la place, SQLite en mémoire (:memory:).
>
> **Setup test** :
>
> ```python
> # Créer engine en mémoire (pas fichier .db)
> engine = create_engine(\"sqlite:///:memory:\")
>
> # Créer tables (comme en prod)
> Base.metadata.create_all(bind=engine)
>
> # Tester
> # → Insert/Update/Delete opèrent sur tables en mémoire
> # → 1000x plus rapide que BDD réelle
> ```
>
> **Comparaison vitesses** :
> | Approche | Temps | Trade-off |
> |----------|-------|-----------|
> | Mock Repository | 1ms | Teste seulement Use Case logic |
> | Vraie BDD | 100ms | Teste ORM + constraints mais lent |
> | SQLite memory | 5ms | Teste intégration en mode rapide |
>
> **Pour NovaCRM** :
> - Unit tests (Use Cases) : Mock Repository (1ms)
> - Integration tests (Routes) : SQLite memory (5ms)
> - E2E tests (Workflow) : Docker PostgreSQL (100ms)
> - Production : PostgreSQL réelle
>
> **Bénéfice** : 12 tests tournent en 50ms, pas 5 secondes. Dev heureux ✨"

---

## 📝 Exercices de Compréhension

### **Exercice 1 : Refactoriser sans Repository**

**Code (mauvais)** :

```python
# infrastructure/http/routes/contacts.py
from sqlalchemy.orm import Session

@router.post('/contacts')
def create_contact(request: ContactCreateRequest, db: Session):
    # ❌ SQL directement dans route!
    # Email unique?
    existing = db.query(ContactModel).filter(ContactModel.email == request.email).first()
    if existing:
        return error("Email existe")
    
    # Créer
    contact = ContactModel(name=request.name, email=request.email)
    db.add(contact)
    db.commit()
    
    return contact
```

**Tâche** :

1. Extraire logique SQL vers `SQLAlchemyContactRepository`
2. Créer interface `ContactRepository` (abstraite)
3. Créer Use Case `CreateContactUseCase` (reçoit Repository injecté)
4. Route appelle Use Case (pas SQL)

**Réponses attendues** :

- Route = 10 lignes (orchestration)
- Use Case = 15 lignes (logique métier)
- Repository = 20 lignes (SQL encapsulé)
- Code testable : mock Repository, tests en mémoire

---

### **Exercice 2 : Ajouter colonne phone (migration)**

**Scénario** :

Jour 2 fin : "Ajouter colonne phone à Contact"

**Tâche** :

1. Modifier `ContactModel.phone` (SQLAlchemy)
2. Créer migration Alembic (versionner changement)
3. Update `ContactRepository.create()` pour accepter phone
4. Update tests

**Réponses attendues** :

- Migration 0001: CREATE TABLE contacts (id, name, email, created_at)
- Migration 0002: ALTER TABLE contacts ADD COLUMN phone VARCHAR(20)
- Rollback possible : `alembic downgrade`

---

### **Exercice 3 : Tester PiiDetector avec textes variés**

**Code** :

```python
detector = PiiDetector()

texts = [
    "Contact Sophie à sophie@example.com",
    "Call me at +33612345678",
    "Bonjour, aucune PII ici",
    "Email: john@acme.fr Téléphone: 06 98 76 54 32"
]

for text in texts:
    findings = detector.detect(text)
    print(f"Text: {text}")
    print(f"  Findings: {len(findings)}")
    for f in findings:
        print(f"    - {f.rule_id}: {f.message}")
```

**Tâche** :

1. Exécuter code (prédit output)
2. Pourquoi certains téléphones ne sont PAS détectés? (06 98 76 → pas E.164)
3. Améliorer regex pour accepter formats France (06/07 avec espaces)

**Réponses attendues** :

- Text 1: 1 finding (email)
- Text 2: 1 finding (téléphone +33)
- Text 3: 0 findings
- Text 4: 1 finding (email), 0 pour téléphone (format non reconnu)
- Improve: regex r'0[67]\d{8}' or r'0[67](\s)?[\d\s]{8}' (avec espaces)

---

## 🚀 Checklist de Fin de Journée

**Avant de fermer, vérifiez :**

### Architecture & Code ✅
- [ ] Domain Contact créé (logique métier pure)
- [ ] SQLAlchemy ContactModel créé (mappage ORM)
- [ ] Interface ContactRepository abstraite
- [ ] SQLAlchemyContactRepository implémentée
- [ ] CreateContactUseCase + autres Use Cases
- [ ] Routes CRUD (/api/v1/contacts)
- [ ] DTOs Pydantic validation
- [ ] PiiDetector + CompliancePipeline
- [ ] Database setup SQLite + init_db()

### Tests ✅
- [ ] Tests CRUD (create/read/update/delete)
- [ ] Tests validation (email unique, format)
- [ ] Tests pagination
- [ ] Tests PiiDetector
- [ ] Couverture 80%+ backend

### Serveur ✅
- [ ] POST /api/v1/contacts → crée contact
- [ ] GET /api/v1/contacts/{id} → lire contact
- [ ] PUT /api/v1/contacts/{id} → modifier
- [ ] DELETE /api/v1/contacts/{id} → supprimer
- [ ] GET /api/v1/contacts → lister (paginé)
- [ ] Swagger UI  updated (/docs)
- [ ] PiiDetector testable en Python shell

### Git ✅
- [ ] Tous fichiers committé
- [ ] Commit message descriptif
- [ ] Pas d'erreurs lint/format
- [ ] Pas de fichiers .db en git

### Documentation ✅
- [ ] jour002.md compris
- [ ] Analogie Restaurant internalisée
- [ ] Repository pattern expliqué
- [ ] ORM benefits understood

### Prêt pour Jour 003 ✅
- [ ] Comprendre Jour 003 = Audit Trail Immuable (CRITIQUE)
- [ ] Anticiper masking PII avant stockage
- [ ] Planifier 📝 TODO journal des accès

---

## 📌 Notes & Astuces

### Repository Pattern - Résumé

```
Use Case dépend de Repository (abstrait)
         ↓
Repository encapsule SQLAlchemy
         ↓
SQLAlchemy gère SQL/migrations
         ↓
Base de données physique

Bénéfice : Change BDD sans toucher Use Case
```

### Fichiers à connaître

- **core/domain/** : Entités métier (0 imports externes)
- **core/use_cases/** : Logique métier (importe domain + repository)
- **infrastructure/database/** : SQLAlchemy + Repository (importe domain)
- **infrastructure/http/routes/** : Endpoints (importe use_cases)
- **infrastructure/http/dto.py** : Validation (importe domain)

### SQLite vs PostgreSQL

**Dev** : SQLite (fichier `nova_crm.db`)  
**Prod** : PostgreSQL (migration Jour 8)  
**Tests** : SQLite memory (:memory:)

### Pydantic Config

```python
class ContactCreateRequest(BaseModel):
    email: EmailStr  # Auto-valide format email
    name: str = Field(..., min_length=2)  # Min length
    
    class Config:
        schema_extra = {"example": {...}}  # Swagger example
```

---

**FIN DE JOUR 002 ✅**

Vous avez maintenant un **backend métier complet** :
- ✅ CRUD Contacts fonctionnel
- ✅ Repository Pattern (testabilité)
- ✅ SQLAlchemy ORM + migrations
- ✅ Première règle IA (PiiDetector)
- ✅ Tests intégration 80%+

💪 **Vous êtes désormais capable de** :
- Expliquer Repository Pattern à un architecte
- Justifier SQLAlchemy vs SQL brut
- Implémenter CRUD avec séparation concerns
- Tester sans vraie BDD

➡️ **DEMAIN (Jour 003 — CRITIQUE)** :  
**Audit Trail Immuable + PII Masking + Intégration Engine**

🔴 **SPRINT 2 GO/NO-GO : Audit trail fondation conformité IA Act**

🎉 **Excellent ! Jour 002 complété !**
