# 🚀 SECTION C : FastAPI Backend pour NovaCRM

**Durée estimée** : 8-10 heures  
**Prérequis** : SECTION A (contexte), SECTION B (architecture)  
**Objectif** : Comprendre FastAPI + créer premiers endpoints pour NovaCRM

---

## 🚀 LEÇON 1 : FastAPI — Concept & Comparaison

### 📍 Le Concept (Théorie)

**FastAPI** = Framework Python pour créer APIs REST rapidement, avec type hints et async.

**Comparaison frameworks** :

| Framework | Type | Philosophie | Use case |
|-----------|------|-------------|----------|
| **Django** | Full-stack | "Batteries included" | Apps monolith (admin panel, ORM, forms, everything) |
| **Flask** | Micro | "Minimalist" | Simple REST APIs (petits projets) |
| **FastAPI** | Moderne | "Speed + types + async" | Production APIs (performance, scalability, dev experience) |

**Analogie concrète** : Restaurants

```
❌ DJANGO = Restaurant franchise classique
  ├─ Menu fixe (admin panel, ORM, auth)
  ├─ Tout standardisé (bon, mais lourd)
  └─ Parfait si vous vendez hamburgers et frites

❌ FLASK = Restaurant petit, DIY
  ├─ Vous cuisinez tout vous-même
  ├─ Flexible mais fatiguant
  └─ Parfait si vous faites 10 couverts/jour

✅ FASTAPI = Restaurant moderne, optimisé
  ├─ Recettes bien pensées (async, types, docs auto)
  ├─ Fast service (asynchrone, 100 requêtes/seconde)
  ├─ Smart kitchen (automatic validation, serialization)
  └─ Parfait si vous servez 1000 couverts/jour + besoin scaling
```

**FastAPI avantages** :

1. **Type hints** : Validation automatique (Pydantic)
   ```python
   @app.post("/contacts")
   def create_contact(contact: ContactDTO) -> ContactResponse:
       # FastAPI auto-validate contact has name, email, etc
       # Type hints = self-documenting code
   ```

2. **Async/await** : Concurrency native (10x+ performance vs Django)
   ```python
   @app.get("/contacts/{id}")
   async def get_contact(id: int):
       # async = handle 1000 concurrent requests without threads
   ```

3. **Auto docs** : Swagger UI generated from code (Pydantic + type hints)
   ```
   http://localhost:8000/docs → Interactive API docs
   ```

4. **Validation** : Pydantic validates input automatically
   ```python
   # If POST /contacts with missing email → 422 validation error (automatic!)
   ```

5. **Performance** : One of fastest Python frameworks (comparable Node.js/Go)

**Pourquoi FastAPI pour NovaCRM?**

- ✅ **Compliance engine** needs **async** (PII detection, scoring can be slow)
- ✅ **Real-time audit trail** needs **concurrency** (log every action instantly)
- ✅ **Type safety** important (PII masking bugs = GDPR fines)
- ✅ **Auto docs** = API contract for Frontend (no manual sync)
- ✅ **Performance** = compliance checks must return < 500ms

---

### 🚀 Cas d'usage Réel (NovaCRM + AI Hub)

**Scénario** : Sophie ouvre NovaCRM dashboard. Contacts list loads.

```
Timeline (ideally < 2s total):

T=0ms : Frontend requests GET /api/v1/contacts
T=1ms : FastAPI receives, route handler async function
T=2ms : SQLAlchemy ORM query contacts (async)
T=50ms : Engine adapter calls compliance check (async, parallel to DB)
T=100ms : DB returns 100 contacts
T=120ms : Compliance check returns findings (PII detected in 5 contacts)
T=125ms : Masking applied, audit trail logged
T=150ms : Response serialized to JSON (Pydantic auto-serialization)
T=160ms : Frontend receives JSON, renders list
T=2s : Sophie sees list

WITH DJANGO (sync):
  T=0ms : Request received
  T=1ms : DB query (BLOCKS)
  T=100ms : DB returns (FINALLY)
  T=101ms : Compliance check (BLOCKS)
  T=200ms : Check returns
  T=300ms : Serialization
  T=301ms : Response sent
  = 301ms for ONE user

  If 10 concurrent users → 10 requests queued, each waits 300ms
  = 3 seconds latency for users 5-10

WITH FASTAPI (async):
  T=0ms : Request 1 received, starts async
  T=1ms : Request 2 received, starts async (no wait!)
  T=2ms : Request 3 received, starts async
  ...
  T=100ms : Request 1 DB returns, Request 2 DB returns, Request 3 DB returns (PARALLEL)
  T=150ms : All compliance checks return (PARALLEL)
  T=200ms : All responses sent
  = All 10 users see result at ~200ms (30% latency improvement)
```

**FastAPI async = NovaCRM compliance checks don't block dashboard load.**

---

### 💻 Le Lab Pratique — FastAPI Setup

#### **LAB 1.1 : Setup FastAPI locally**

**Objectif** : Démarrer FastAPI et avoir premier endpoint.

```powershell
# Terminal WSL2
cd /mnt/c/Perso/nova-crm/backend

# Vérifier Python >= 3.10
python --version
# Doit afficher Python 3.10+ (pour async/await)

# Créer virtualenv
python -m venv .venv

# Activer virtualenv (WSL2)
source .venv/bin/activate

# Ou Windows PowerShell
.venv\Scripts\Activate.ps1

# Installer dependencies
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv pytest

# Vérifier installation
pip list | grep -E "fastapi|uvicorn|sqlalchemy|pydantic"
# Doit voir : fastapi, uvicorn, sqlalchemy, pydantic

echo "✅ FastAPI setup complete"
```

**Résultat** : Virtualenv activé, dependencies installées.

---

#### **LAB 1.2 : Créer premier endpoint /health**

**Objectif** : Créer endpoint /health qui retourne status.

**Étape 1 : Structure du projet**

```powershell
# Terminal
cd /mnt/c/Perso/nova-crm/backend

# Listez structure actuelle
ls -la
# Vous verrez : core/, infrastructure/, venv/, etc

# Créez dossier s'il n'existe pas
mkdir -p infrastructure/http/routes
mkdir -p infrastructure/db
mkdir -p core/domain
mkdir -p core/services
mkdir -p shared

echo "✅ Folders created"
```

**Étape 2 : Créer main.py (FastAPI app)**

```python
# backend/infrastructure/http/main.py
# Fichier principal FastAPI

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routes (créé après)
from infrastructure.http.routes import health, contacts

# Startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 NovaCRM Backend starting...")
    yield
    # Shutdown
    print("🛑 NovaCRM Backend shutting down...")

# Create FastAPI app
app = FastAPI(
    title="NovaCRM API",
    description="CRM + AI Compliance Hub",
    version="0.1.0",
    lifespan=lifespan
)

# CORS (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router)
app.include_router(contacts.router)

# Run with: uvicorn infrastructure.http.main:app --reload
```

**Étape 3 : Créer routes/health.py (health endpoint)**

```python
# backend/infrastructure/http/routes/health.py

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter(tags=["health"])

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        status: "ok" if healthy
        timestamp: server time
        version: API version
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "service": "NovaCRM Backend"
    }

@router.get("/health/detailed")
async def health_detailed() -> Dict[str, Any]:
    """
    Detailed health check (DB, Engine, etc).
    
    Returns:
        backend: ok
        database: ok/error
        engine: ok/error
    """
    return {
        "backend": "ok",
        "database": "ok",  # TODO: actually check
        "engine": "ok",    # TODO: actually check
        "timestamp": datetime.utcnow().isoformat()
    }
```

**Étape 4 : Créer routes/__init__.py (make it package)**

```python
# backend/infrastructure/http/routes/__init__.py
# Empty file to make routes a package
```

**Étape 5 : Créer routes/contacts.py (stub for future)**

```python
# backend/infrastructure/http/routes/contacts.py

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

router = APIRouter(prefix="/api/v1/contacts", tags=["contacts"])

@router.get("/")
async def list_contacts() -> List[Dict[str, Any]]:
    """
    List all contacts.
    
    TODO: Implement real CRUD
    """
    return [
        {"id": 1, "name": "Sophie Martin", "email": "sophie@example.com"},
        {"id": 2, "name": "Jean Dupont", "email": "jean@example.com"}
    ]

@router.get("/{contact_id}")
async def get_contact(contact_id: int) -> Dict[str, Any]:
    """
    Get contact by ID.
    """
    if contact_id < 1:
        raise HTTPException(status_code=400, detail="Invalid contact ID")
    
    return {"id": contact_id, "name": "Sophie Martin", "email": "sophie@example.com"}

@router.post("/")
async def create_contact(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create new contact.
    
    TODO: Validate with Pydantic DTO
    """
    return {"id": 3, "name": data.get("name"), "email": data.get("email")}
```

**Étape 6 : Démarrer le serveur**

```powershell
# Terminal (dans virtualenv)
cd backend

# Démarrer FastAPI server (hot reload enabled)
uvicorn infrastructure.http.main:app --reload --host 0.0.0.0 --port 8000

# Output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
```

**Étape 7 : Tester l'endpoint**

```powershell
# Terminal (nouvelle window)

# Test /health endpoint
curl http://localhost:8000/health

# Réponse attendue:
# {
#   "status": "ok",
#   "timestamp": "2026-01-28T10:15:23.123456",
#   "version": "0.1.0",
#   "service": "NovaCRM Backend"
# }

# Test /health/detailed
curl http://localhost:8000/health/detailed

# Test /api/v1/contacts
curl http://localhost:8000/api/v1/contacts
# Réponse:
# [
#   {"id": 1, "name": "Sophie Martin", "email": "sophie@example.com"},
#   {"id": 2, "name": "Jean Dupont", "email": "jean@example.com"}
# ]

# Accéder à Swagger UI
# Open browser: http://localhost:8000/docs
# Vous verrez interactive API documentation auto-générée!
```

**Résultat attendu** : 
- ✅ FastAPI server running
- ✅ /health endpoint returns 200 OK
- ✅ Swagger docs at /docs
- ✅ Contacts list endpoint returns data

---

### 💼 Préparation Entretien (Q&A)

#### **Q1 : "Pourquoi FastAPI plutôt que Django pour NovaCRM?"**

**Réponse attendue** :

> "FastAPI vs Django — c'est un choix architectural documenté en ADR-02.
>
> **Django** :
> - ✅ Full-stack (ORM, admin, auth built-in)
> - ✅ Mature (15+ years)
> - ❌ Synchrone par défaut (blocking I/O)
> - ❌ Lourd pour APIs seules (ORM + admin + templates = overhead)
> - ❌ Performance limitée (1 thread per request)
>
> **FastAPI** :
> - ✅ Async native (async/await)
> - ✅ Performance (10x+ vs Django on I/O-heavy apps)
> - ✅ Type hints (automatic validation, documentation)
> - ✅ Auto API docs (Swagger generated from code)
> - ✅ Lightweight (APIs only, no admin/templates)
> - ❌ Newer (less mature than Django)
> - ❌ Requires async mindset
>
> **Décision NovaCRM** :
> 1. **Compliance checks async** : Calling Engine IA can be slow (PII detection, scoring). Async = don't block dashboard
> 2. **Type safety** : PII masking bugs = GDPR fines. Type hints + Pydantic = compile-time safety
> 3. **Auto docs** : Frontend + Backend aligned on API contract (Swagger auto-generated)
> 4. **Performance** : Compliance checks must return < 500ms. Async = achievable
>
> **Verdict** : FastAPI = perfect fit for compliance-first, async-heavy, API-only backend."

**Score** : ✅ Montrez compréhension choix architectural (pourquoi FastAPI pour NovaCRM specifiquement).

---

#### **Q2 : "Expliquez async/await dans FastAPI. Quel bénéfice pour NovaCRM?"**

**Réponse attendue** :

> "**Async/await** = Coroutines. Une fonction peut pause et let autre fonction run.
>
> **Analogie** : Restaurant sans async = 1 serveur qui prend commande, puis attend que cuisine fasse le plat, puis livré. Pendant ce temps, autres clients attendent (blocking).
>
> Restaurant avec async = 1 serveur qui prend commande (client 1), tandis que cuisine travaille, il prend commande (client 2), etc. Pendant ce temps, cuisine prépare (parallelism sans threads).
>
> **Code** :
> ```python
> # Sync (BLOCKING) - Django
> @app.get('/contacts')
> def list_contacts():
>     contacts = db.query(Contact).all()  # ← BLOCKS 100ms
>     return contacts
> 
> # Si 10 requêtes concurrent → each waits 100ms = 1 second total
>
> # Async (NON-BLOCKING) - FastAPI
> @app.get('/contacts')
> async def list_contacts():
>     contacts = await db.query(Contact).all()  # ← YIELDS, other requests run
>     return contacts
> 
> # Si 10 requêtes concurrent → all run in parallel, 100ms total
> ```
>
> **Bénéfice NovaCRM** :
> ```python
> @app.post('/contacts')
> async def create_contact(contact: ContactDTO):
>     # Step 1: Validate & save DB (async)
>     db_contact = await db.save(contact)
>     
>     # Step 2: Call Engine for compliance check (async, parallel to other requests)
>     compliance = await engine_adapter.analyze(contact.text)
>     
>     # Step 3: Log audit trail (async)
>     await audit_logger.log(action='create_contact', contact_id=db_contact.id)
>     
>     return db_contact
> 
> # WHILE this request waiting for Engine (step 2), other requests can run!
> # Instead of blocking for 200ms, we yield and let others run.
> ```
>
> **Performance** :
> - Sync : 1000 requests × 200ms per request = 200 seconds latency for last user
> - Async : 1000 requests × 200ms per request = 200ms latency (all parallel)"

**Score** : ✅ Montrez compréhension async/await + bénéfice concret (parallelism sans threads).

---

#### **Q3 : "Qu'est-ce que Pydantic? Comment valide-t-il input?"**

**Réponse attendue** :

> "**Pydantic** = library Python pour validation + serialization de données via type hints.
>
> **Concept** : Vous déclarez structure de donnée avec types. Pydantic valide automatiquement.
>
> **Code** :
> ```python
> from pydantic import BaseModel, EmailStr, Field
> from typing import Optional
>
> class ContactDTO(BaseModel):
>     name: str = Field(..., min_length=1, max_length=100)
>     email: EmailStr  # Auto-validates email format
>     phone: Optional[str] = None
>     company: Optional[str] = None
>
> # Usage
> @app.post('/contacts')
> async def create_contact(contact: ContactDTO):  # ← Type hint
>     # If POST body missing 'name' or email invalid → FastAPI auto-returns 422
>     # No manual validation needed!
>     return contact
>
> # POST /contacts { name: 'Sophie', email: 'not-an-email' }
> # Response: 422 Unprocessable Entity
> # Error: 'not-an-email' is not a valid email address
> ```
>
> **Avantages** :
> - ✅ **Automatic validation** : No if/else checks
> - ✅ **Type safety** : Errors caught at runtime (better than runtime bugs)
> - ✅ **Auto docs** : DTO structure in Swagger
> - ✅ **Serialization** : Convert Python objects ↔ JSON automatically
> - ✅ **Compliance** : Email validation = reduces spam/typos (data quality)
>
> **Pourquoi important pour NovaCRM** :
> - Contact email invalid = PII detection might fail
> - Type safety = fewer bugs in compliance checks
> - Auto validation = frontend + backend aligned (both use same DTO)"

**Score** : ✅ Montrez compréhension Pydantic validation + bénéfices (moins bugs, meilleure qualité).

---

#### **Q4 : "Comment FastAPI génère-t-il la documentation API?"**

**Réponse attendue** :

> "**FastAPI auto-génère Swagger UI** à partir du code (type hints + docstrings).
>
> **Processus** :
> 1. Vous déclarez route avec types et docstring
> ```python
> from typing import List
> from pydantic import BaseModel
>
> class Contact(BaseModel):
>     id: int
>     name: str
>     email: str
>
> @app.get('/contacts', response_model=List[Contact])
> async def list_contacts(skip: int = 0, limit: int = 10):
>     '''
>     List all contacts.
>     
>     Query Parameters:
>     - skip: Skip first N contacts (pagination)
>     - limit: Return max N contacts
>     
>     Returns:
>         List of contacts
>     '''
>     return [...]
> ```
>
> 2. FastAPI auto-generates OpenAPI schema (JSON describing API)
> 3. Swagger UI reads OpenAPI schema → interactive docs
>
> **Result** :
> - GET http://localhost:8000/docs → Interactive API explorer
> - Try endpoints, see responses, auto-generates curl commands
> - No manual documentation needed! Code = docs
>
> **Avantage NovaCRM** :
> - Frontend dev opens /docs → sees all endpoints, response formats, error codes
> - No manual sync (Frontend doesn't ask 'what does /api/v1/contacts return?')
> - Type safety = contract enforced"

**Score** : ✅ Montrez compréhension auto-docs + bénéfice (no manual sync, contract enforced).

---

### ✅ Validation de l'étape

**Checklist — Vous avez compris FastAPI Basics quand** :

- [ ] Vous expliquez **FastAPI en 1 phrase** : "Framework pour APIs performantes, async-native, avec type hints et auto-docs"
- [ ] Vous comprenez **FastAPI vs Django vs Flask** (trade-offs)
- [ ] Vous pouvez **démarrer FastAPI localement** (virtualenv, pip install, uvicorn)
- [ ] Vous créez un **premier endpoint** (/health)
- [ ] Vous testez avec **curl** et **Swagger UI**
- [ ] Vous comprenez **async/await** et bénéfices (parallelism)
- [ ] Vous comprenez **Pydantic validation** (type hints = auto-validation)
- [ ] Vous savez que **FastAPI génère docs auto** (/docs = Swagger)
- [ ] Vous répondez aux **4 questions entretien** avec confiance

**Validation pratique** :

```powershell
# Vérifiez que le serveur tourne
curl http://localhost:8000/health

# Vous devriez voir:
# {"status":"ok","timestamp":"2026-01-28T10:15:23","version":"0.1.0","service":"NovaCRM Backend"}

# Vérifiez les docs
curl http://localhost:8000/docs | grep -q "swagger" && echo "✅ Swagger docs loaded"

echo "✅ FastAPI Basics validated"
```

---

## 🚀 LEÇON 2 : Pydantic DTOs (Data Transfer Objects)

### 📍 Le Concept (Théorie)

**DTO (Data Transfer Object)** = Classe définissant structure de donnée pour communication.

**Analogie concrète** : Formulaire d'inscription.

```
❌ SANS DTO (formulaire libre) :
  POST /contacts { name: 'Sophie', phone: '123' }
  Backend : "Quels champs attendus? Quels validations?"
  Si manquent champs → crash

✅ AVEC DTO (formulaire structuré) :
  DTO ContactCreateDTO = { name: str, email: EmailStr, phone?: str }
  POST /contacts → FastAPI auto-valide contra DTO
  Si email manquant → 422 Error (avant même entrer handler)
```

**Pydantic DTO structure** :

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# DTO for CREATE request (input)
class ContactCreateDTO(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, regex=r'^\+?[\d\s\-()]{10,}')
    company: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sophie Martin",
                "email": "sophie@example.com",
                "phone": "+33 6 12 34 56 78",
                "company": "Google"
            }
        }

# DTO for GET response (output)
class ContactResponseDTO(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True  # Map SQLAlchemy model → DTO

# Usage in routes
@app.post("/contacts", response_model=ContactResponseDTO)
async def create_contact(contact: ContactCreateDTO) -> ContactResponseDTO:
    # contact is validated ContactCreateDTO (not dict)
    # response will be serialized per ContactResponseDTO schema
    pass
```

**Avantages DTO** :

1. **Validation** : Pydantic checks types + constraints
2. **Documentation** : Swagger shows DTO structure
3. **Serialization** : Python ↔ JSON conversion automatic
4. **Decoupling** : Request/response format ≠ DB schema
5. **Versioning** : ContactCreateDTOv1 vs ContactCreateDTOv2

---

### 🚀 Cas d'usage Réel (NovaCRM)

**Scénario** : Frontend créé un contact via `/api/v1/contacts`. Backend masque PII avant storaging.

```python
# shared/dto.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ===== REQUEST DTOs =====

class ContactCreateDTO(BaseModel):
    """
    Request DTO for creating contact.
    Frontend sends this structure.
    """
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr  # Auto-validates email
    phone: Optional[str] = Field(None, regex=r'^\+?[\d\s\-()]{10,}')
    company: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sophie Martin",
                "email": "sophie@example.com",
                "phone": "+33 6 12 34 56 78",
                "company": "Google",
                "notes": "Met at conference"
            }
        }

# ===== RESPONSE DTOs =====

class ContactResponseDTO(BaseModel):
    """
    Response DTO for contact data.
    Frontend receives this structure.
    PII may be masked (depends on user role + scope).
    """
    id: int
    name: str
    email: str  # May be masked (sophi*@**mple.com)
    phone: Optional[str] = None  # May be masked
    company: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# ===== USAGE IN ROUTES =====

# infrastructure/http/routes/contacts.py

@app.post("/api/v1/contacts", response_model=ContactResponseDTO)
async def create_contact(
    contact: ContactCreateDTO
) -> ContactResponseDTO:
    """
    Create new contact.
    
    Flow:
    1. Pydantic validates ContactCreateDTO
    2. Backend calls engine to check PII
    3. Engine masks PII in contact data
    4. Backend stores masked contact in DB
    5. Backend returns ContactResponseDTO (masked)
    
    Args:
        contact: Contact data (validated by Pydantic)
    
    Returns:
        ContactResponseDTO: Created contact (with masked PII)
    
    Raises:
        422: Validation error (invalid email, etc)
        400: Business error (email already exists)
    """
    # Step 1: Validate via DTO (automatic by FastAPI)
    # contact.name : str (min_length 1, max_length 100)
    # contact.email : EmailStr (valid email)
    
    # Step 2: Convert DTO → Domain Entity
    contact_entity = Contact(
        name=contact.name,
        email=contact.email,
        phone=contact.phone,
        company=contact.company,
        notes=contact.notes
    )
    
    # Step 3: Call compliance engine
    compliance_result = await engine_adapter.analyze(
        text=f"{contact.email} {contact.phone} {contact.notes}"
    )
    # Returns: { pii_found: [...], masked_data: {...}, audit_id: '123' }
    
    # Step 4: Mask PII in entity
    if compliance_result.pii_found:
        contact_entity.email = compliance_result.masked_data['email']
        contact_entity.phone = compliance_result.masked_data['phone']
    
    # Step 5: Save to DB
    saved_contact = await db.save(contact_entity)
    
    # Step 6: Log audit trail
    await audit_logger.log(
        action='contact_created',
        contact_id=saved_contact.id,
        pii_found=compliance_result.pii_found,
        audit_id=compliance_result.audit_id
    )
    
    # Step 7: Return as DTO (Pydantic serializes)
    return ContactResponseDTO.from_orm(saved_contact)
```

**Benefit** : DTOs = contract between Frontend + Backend. Both use same structure.

---

### ✅ Validation de l'étape

**Checklist** :

- [ ] Vous comprenez **DTO purpose** (contract, validation, serialization)
- [ ] Vous créez **ContactCreateDTO** avec Pydantic
- [ ] Vous créez **ContactResponseDTO** avec Pydantic
- [ ] Vous utilisez DTO dans route (input + response_model)
- [ ] Vous testez validation (POST with missing email → 422)

**Test pratique** :

```powershell
# Test valide
curl -X POST http://localhost:8000/api/v1/contacts \
  -H "Content-Type: application/json" \
  -d '{"name": "Sophie", "email": "sophie@example.com"}'
# Réponse: 200 OK

# Test invalide (missing email)
curl -X POST http://localhost:8000/api/v1/contacts \
  -H "Content-Type: application/json" \
  -d '{"name": "Sophie"}'
# Réponse: 422 Validation Error

# Test Swagger
# Open http://localhost:8000/docs → Try it out → POST /api/v1/contacts
```

---

## 🚀 LEÇON 3 : Middleware & Error Handling

### 📍 Le Concept (Théorie)

**Middleware** = Fonction qui s'exécute pour chaque requête (logging, auth, CORS, etc).

**Error Handling** = Convertir exceptions → HTTP responses.

**Analogie** : Douane à aéroport

```
Request arrive :
  ↓
Douane (Middleware 1 : CORS check)
  ↓
Douane (Middleware 2 : Auth check, token validation)
  ↓
Douane (Middleware 3 : Request logging)
  ↓
✅ Request enters endpoint
  ↓
❌ Exception thrown (email not found)
  ↓
Error handler catches → converts to HTTP 404 response
```

**FastAPI middleware pattern** :

```python
@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    """Log every request + response."""
    start_time = time.time()
    
    # Call next middleware/endpoint
    response = await call_next(request)
    
    # Log after response
    duration = time.time() - start_time
    print(f"{request.method} {request.url.path} → {response.status_code} ({duration:.2f}s)")
    
    return response

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError → 400 Bad Request."""
    return JSONResponse(
        status_code=400,
        content={"error": str(exc), "path": request.url.path}
    )
```

---

### 💼 Préparation Entretien (Q&A)

#### **Q : "Comment valider JWT token dans FastAPI?"**

**Réponse attendue** :

> "JWT (JSON Web Token) = stateless authentication. Token contains user info + signature.
>
> ```python
> # Via middleware (run for all requests)
> @app.middleware('http')
> async def auth_middleware(request: Request, call_next):
>     token = request.headers.get('Authorization', '')
>     
>     if not token.startswith('Bearer '):
>         return JSONResponse(
>             status_code=401,
>             content={'error': 'Missing or invalid token'}
>         )
>     
>     try:
>         token_str = token.split(' ')[1]
>         payload = jwt.decode(token_str, SECRET_KEY)
>         request.state.user = payload  # Attach user to request
>     except jwt.InvalidTokenError:
>         return JSONResponse(
>             status_code=401,
>             content={'error': 'Invalid token'}
>         )
>     
>     response = await call_next(request)
>     return response
> 
> # Usage in endpoint
> @app.get('/protected')
> async def protected(request: Request):
>     user = request.state.user
>     return {'message': f'Hello {user[\"name\"]}'}
> ```"

---

### ✅ Validation SECTION C

**Checklist finale** :

- [ ] Vous démarrez FastAPI (uvicorn)
- [ ] Vous créez /health endpoint
- [ ] Vous créez Pydantic DTOs (ContactCreateDTO, ContactResponseDTO)
- [ ] Vous créez /api/v1/contacts endpoint
- [ ] Vous testez validation (curl + invalid data)
- [ ] Vous accessez Swagger docs (/docs)
- [ ] Vous comprenez async/await
- [ ] Vous comprenez middleware + error handling

---

**Fin de SECTION C**

✅ **Vous savez maintenant** :
- FastAPI fondamentals (async, Pydantic, auto-docs)
- Créer endpoints avec DTOs
- Valider input automatiquement
- Documenter API via code

➡️ **Prochaine** : LAB 1-2 (Setup env + /health endpoint)
