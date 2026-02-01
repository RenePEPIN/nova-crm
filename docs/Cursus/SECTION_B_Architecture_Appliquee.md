# 🏗️ SECTION B : Architecture Appliquée à NovaCRM

**Durée estimée** : 5-6 heures  
**Prérequis** : SECTION A (contexte + glossaire)  
**Objectif** : Comprendre COMMENT la structure backend/frontend/ai se traduit en patterns de code

---

## 🏗️ LEÇON 1 : Separation of Concerns (SoC) — Pourquoi 3 modules?

### 📍 Le Concept (Théorie)

**SoC (Separation of Concerns)** = Principe de modularity : **chaque module a UNE responsabilité, UNE raison de changer**.

**Analogie concrète** : Une entreprise.

```
❌ SANS SoC (Monolith) :
  [Entreprise unilatérale]
  ├─ PDG fait ventes ET comptabilité ET HR ET IT
  └─ Si PDG part → tout s'écroule

✅ AVEC SoC (Modular) :
  [Entreprise modulaire]
  ├─ VP Sales (ventes, client relations)
  ├─ CFO (comptabilité, finances)
  ├─ CHRO (ressources humaines)
  └─ CTO (IT, systèmes)

  Si VP Sales part, autres continuent.
  Chacun expert dans son domaine.
  Peuvent croître indépendamment.
```

**Appliqué à NovaCRM** :

| Module                 | Responsabilité                          | Raison de changer                                 |
| ---------------------- | --------------------------------------- | ------------------------------------------------- |
| **Backend (FastAPI)**  | Orchestration, persistance, API         | Changement métier (contacts, clients, rules CRUD) |
| **Frontend (Next.js)** | Affichage, UX, interactions utilisateur | Changement UI/UX, design system                   |
| **AI Engine (Python)** | Analyse compliance, détection risques   | Nouvelle règle, nouvelle détection (PII, secrets) |

**Sans SoC** : Changement Engine = recompile tout backend + frontend. Risque de bug. Deploy long.

**Avec SoC** : Changement Engine = recompile juste Engine. 2 min. Zéro risque backend/frontend.

---

### 🚀 Cas d'usage Réel (NovaCRM + AI Hub)

**Scénario** : Une nouvelle loi arrive : "Il faut aussi masquer les numéros de Sécurité Sociale".

**Étape 1 : Changement code Engine seul**

```python
# ai/detectors/pii_detector.py
# Avant
PATTERNS = {
    'email': r'[\w\.-]+@[\w\.-]+\.\w+',
    'phone': r'\+?[\d\s\-()]{10,}'
}

# Après
PATTERNS = {
    'email': r'[\w\.-]+@[\w\.-]+\.\w+',
    'phone': r'\+?[\d\s\-()]{10,}',
    'ss_number': r'\d{1}\s\d{2}\s\d{2}\s\d{3}\s\d{3}\s\d{2,3}'  # NEW
}
```

**Étape 2 : Redeploy Engine uniquement**

```bash
cd ai/
python -m pytest detectors/test_pii_detector.py  # Tests pass ✅
docker build -t nova-engine:v2 .
docker push nova-engine:v2
kubectl set image deployment/nova-engine engine=nova-engine:v2
# Engine updated in 2 min. Zero downtime for backend/frontend.
```

**Avantages SoC ici** :

- ✅ Backend code untouched → zéro risque regression
- ✅ Frontend code untouched → users see same UI
- ✅ Engine only tested → 5 min, pas 1 hour full test suite
- ✅ Parallel deployment : Engine v2 can run with backend v1 (backward compat)

---

### 💻 Le Lab Pratique — Structure & File Organization

#### **LAB 2.1 : Explorez la structure réelle du backend**

**Objectif** : Comprendre comment le backend applique SoC.

```bash
# Terminal
cd /home/renep/dev/nova-crm/backend

# Listez la structure
tree -L 3 -I '__pycache__|*.pyc'
# Vous devez voir :
# backend/
# ├─ core/                          ← Logique métier (SoC)
# │  ├─ domain/                     ← Modèles métier (Contact, Health, etc.)
# │  │  ├─ contact.py               ← Entity Contact
# │  │  ├─ health.py                ← Entity Health
# │  │  └─ ...                      ← Autres entités métier
# │  └─ use_cases/                  ← Use cases métier (logique applicative)
# │     ├─ create_contact.py        ← Use case : créer un contact
# │     ├─ check_compliance.py      ← Use case : vérifier conformité
# │     └─ ...                      ← Autres use cases
# │
# ├─ infrastructure/                ← Techniques (SoC)
# │  ├─ http/                       ← API REST (FastAPI)
# │  │  ├─ routes/
# │  │  │  ├─ contacts.py           ← GET/POST /api/v1/contacts (futur)
# │  │  │  ├─ clients.py            ← GET/POST /api/v1/clients (futur)
# │  │  │  └─ health_route.py       ← GET /health
# │  │  ├─ dto.py                   ← Data Transfer Objects (request/response)
# │  │  └─ main.py                  ← FastAPI app initialization
# │  │
# │  ├─ database/                   ← Persistence (SoC)
# │  │  ├─ models.py                ← SQLAlchemy ORM models (futur)
# │  │  ├─ session.py               ← DB session management (futur)
# │  │  └─ migrations/              ← Alembic versions (futur)
# │  │
# │  └─ audit/                      ← Audit trail & logging
# │     └─ ...                      ← Audit logs (futur)
# │
# └─ shared/                         ← Code partagé (SoC)
#    └─ ...                         ← Utils, exceptions (futur)

echo "Structure backend explored"
```

**Explications SoC** :

| Folder                     | Role                                                | Change trigger                               |
| -------------------------- | --------------------------------------------------- | -------------------------------------------- |
| `core/domain/`             | **Métier** : Entités pures (Contact, Health, etc.)  | Changement métier (nouveau champ contact?)   |
| `core/use_cases/`          | **Logique** : Use cases, validations, orchestration | Changement règles métier (nouveau workflow?) |
| `infrastructure/http/`     | **Présentation** : API REST (routes, DTOs)          | Changement contrat API (ajouter endpoint?)   |
| `infrastructure/database/` | **Persistence** : SQL, ORM (futur)                  | Changement schema DB (nouvel index?)         |
| `infrastructure/audit/`    | **Audit** : Logging, traçabilité (futur)            | Changement exigences audit                   |
| `shared/`                  | **Partagé** : Utils communs (futur)                 | Changement helpers partagés                  |

**Résumé** :

- ✅ Métier isolé de technique (domain/ vs infrastructure/)
- ✅ API isolée de DB (http/ vs db/)
- ✅ Engine isolé (adapters/engine_adapter.py = interface simple)

---

#### **LAB 2.2 : Explorez la structure réelle du frontend**

```bash
# Terminal WSL2
cd /home/renep/dev/nova-crm/frontend

# Listez la structure
tree -L 3 -I 'node_modules|\.next|.git'
# Vous devez voir :
# frontend/
# ├─ app/                           ← Next.js app dir
# │  ├─ layout.tsx                  ← Root layout (HTML, fonts, globals)
# │  ├─ page.tsx                    ← Home page
# │  ├─ dashboard/                  ← Dashboard page
# │  ├─ contacts/                   ← Contacts feature
# │  │  ├─ page.tsx                 ← Contacts list page
# │  │  ├─ [id]/                    ← Dynamic route /contacts/123
# │  │  │  └─ page.tsx              ← Contact detail page
# │  │  └─ create/
# │  │     └─ page.tsx              ← Create contact page
# │  ├─ clients/                    ← Clients feature (similar structure)
# │  ├─ audit/                      ← Audit trail viewer
# │  └─ settings/                   ← Admin settings
# │
# ├─ components/                    ← Reusable React components
# │  ├─ ui/                         ← Base components (Button, Input, Modal)
# │  │  ├─ button.tsx
# │  │  ├─ input.tsx
# │  │  ├─ modal.tsx
# │  │  └─ ...
# │  ├─ forms/                      ← Form components (ContactForm, ClientForm)
# │  │  ├─ contact-form.tsx
# │  │  ├─ client-form.tsx
# │  │  └─ ...
# │  ├─ layout/                     ← Layout components
# │  │  ├─ header.tsx
# │  │  ├─ sidebar.tsx
# │  │  ├─ footer.tsx
# │  │  └─ ...
# │  └─ shared/                     ← Shared across app
# │     ├─ compliance-banner.tsx   ← Shows compliance warnings
# │     ├─ loading.tsx
# │     └─ ...
# │
# ├─ lib/                           ← Utilities & services
# │  ├─ api.ts                      ← API client (fetch wrapper)
# │  ├─ auth.ts                     ← Auth utils (token management)
# │  ├─ hooks/                      ← Custom React hooks
# │  │  ├─ useContacts.ts           ← Hook for contacts API
# │  │  ├─ useAuth.ts               ← Hook for auth
# │  │  └─ ...
# │  ├─ store/                      ← State management (Zustand/Context)
# │  │  ├─ auth-store.ts            ← Auth state
# │  │  ├─ ui-store.ts              ← UI state (theme, sidebar open?)
# │  │  └─ ...
# │  ├─ types/                      ← TypeScript types (aligned with backend DTOs)
# │  │  ├─ contact.ts               ← Contact type
# │  │  ├─ client.ts                ← Client type
# │  │  └─ ...
# │  └─ utils.ts                    ← Helper functions (format date, validate email)
# │
# ├─ styles/                        ← Global styles
# │  └─ globals.css                 ← Tailwind, CSS variables
# │
# ├─ public/                        ← Static assets
# │  ├─ logo.svg
# │  └─ ...
# │
# ├─ next.config.ts                 ← Next.js configuration
# ├─ tsconfig.json                  ← TypeScript configuration
# ├─ tailwind.config.ts             ← Tailwind CSS config
# └─ package.json                   ← Dependencies

echo "Structure frontend explored"
```

**Explications SoC** :

| Folder        | Role                                              | Change trigger                        |
| ------------- | ------------------------------------------------- | ------------------------------------- |
| `app/`        | **Pages** : Pages Next.js (routes)                | Ajout fonctionnalité (nouvelle page?) |
| `components/` | **Reusable components** : Buttons, forms, layouts | Changement design system              |
| `lib/api.ts`  | **Backend communication**                         | Changement API backend                |
| `lib/hooks/`  | **Custom logic** : Fetch, auth, form state        | Changement logique métier frontend    |
| `lib/store/`  | **State management**                              | Changement state flow                 |
| `lib/types/`  | **Type safety** : DTOs from backend               | Changement contrat API                |
| `styles/`     | **Styling**                                       | Changement design                     |

**Résumé** :

- ✅ Pages isolées de composants réutilisables
- ✅ API isolation (lib/api.ts = point unique de communication)
- ✅ State management centralisé (lib/store/)
- ✅ Type safety (types/ alignés avec backend)

---

#### **LAB 2.3 : Explorez la structure réelle de l'AI Engine**

```bash
# Terminal WSL2
cd /home/renep/dev/nova-crm/ai

# Listez la structure
tree -L 3 -I '__pycache__|*.pyc'
# Vous devez voir :
# ai/
# ├─ detectors/                     ← Détecteurs de risques (rules implémentées)
# │  ├─ __init__.py
# │  ├─ base.py                     ← Classe abstraite Detector (interface)
# │  ├─ pii_detector.py             ← Implémentation rule : no_pii_in_prompts
# │  ├─ secrets_detector.py         ← Implémentation rule : no_api_keys_exposed
# │  ├─ scope_detector.py           ← Implémentation rule : scope_check
# │  └─ test_*.py                   ← Tests (test-driven development)
# │
# ├─ pipelines/                     ← Flux de traitement (orchestration)
# │  ├─ __init__.py
# │  ├─ compliance_pipeline.py      ← Orchestration : load policy → run detectors → mask PII → audit
# │  ├─ factories.py                ← Factory pattern : détecteur matching policy
# │  └─ test_*.py
# │
# ├─ policies/                      ← Déclaration règles (YAML, append-only)
# │  ├─ compliance_policy_v1.yaml   ← Policy v1 : [no_pii, no_secrets, scope_check]
# │  └─ ...
# │
# └─ main.py                        ← Entrypoint Engine (CLI ou server)

echo "Structure AI Engine explored"
```

**Explications SoC** :

| Folder                             | Role                                              | Change trigger                         |
| ---------------------------------- | ------------------------------------------------- | -------------------------------------- |
| `detectors/base.py`                | **Interface** : Contrat pour tous les détecteurs  | Changement signature (add severity?)   |
| `detectors/pii_detector.py`        | **Implémentation** : Une règle concrète           | Changement détection PII (add SS#?)    |
| `pipelines/compliance_pipeline.py` | **Orchestration** : Chaîne de traitement          | Changement flux (add redaction stage?) |
| `policies/`                        | **Configuration** : YAML déclaratif (append-only) | Nouvelle loi (masquer SS#?)            |

**Résumé** :

- ✅ Interface abstraite (base.py) = contrat
- ✅ Implémentations concrètes (detectors/) = pluggables
- ✅ Orchestration (pipelines/) = non-hardcoded
- ✅ Configuration déclarative (policies/) = data-driven, versionnée

---

### 💼 Préparation Entretien (Q&A)

#### **Q1 : "Expliquez la structure backend/frontend/ai. Pourquoi pas une monolith?"**

**Réponse attendue** :

> "NovaCRM a 3 modules isolés : **backend (FastAPI), frontend (Next.js), AI Engine (Python)**.
>
> **Structure logique** :
>
> - **Backend** : API REST orchestrant métier + DB + appels Engine
> - **Frontend** : UI affichant données, interactions utilisateur
> - **Engine** : Analyse compliance, détection risques (PII, secrets)
>
> **Pourquoi SoC et pas monolith?**
>
> 1. **Scaling indépendant** : Engine très CPU-intensive (ML, regex), doit scaler seul. Backend = réseau I/O. Frontend = rendu. Trois machines optimisées différemment.
> 2. **Teams isolées** : Team Python (Engine) ne touch à JavaScript. Team JS (Frontend) ne touch au Python. Zéro couplage, déploiement indépendant.
> 3. **Risk mitigation** : Bug Engine → juste Engine redéploie. Backend/Frontend stable. Monolith = bug partout, restart 1h.
> 4. **Réutilisabilité** : Engine = API universelle. Peut servir d'autres produits (pas juste NovaCRM). Backend = orchestration uniquement.
> 5. **Technology choice** : Python pour Engine (stats, ML librairies). TypeScript pour Frontend (réactivité, types). FastAPI pour Backend (async, performance). Freedom choix tech.
>
> **Contraste monolith** : Tout en Python Django. Ajouter feature → 2h test suite, 15min deploy. Feature bug → restart 1h. Engine bottleneck = tout ralentit."

**Score** : ✅ Montrez compréhension SoC + raisons pratiques (scaling, teams, risk, reuse).

---

#### **Q2 : "Décrivez comment le backend communique avec l'Engine IA."**

**Réponse attendue** :

> "Backend communique avec Engine via **adapter pattern**. Communication = API (HTTP ou message queue).
>
> **Flux concret** :
>
> 1. Frontend envoie `POST /api/v1/contacts` avec données contact
> 2. Backend (infrastructure/http/routes/contacts.py) reçoit requête
> 3. Backend valide input + créé Entity Contact (core/domain/contact.py)
> 4. Backend appelle use case de compliance (core/use_cases/check_compliance.py)
> 5. Le use case peut appeler l'AI Engine via HTTP (communication directe ou via client HTTP)
> 6. engine_adapter envoie `POST http://engine:8000/analyze` avec contact data
> 7. Engine répond : `{ pii_detected: [email, phone], masked_data: {...}, audit_id: 123 }`
> 8. Backend masque données, stocke DB + audit trail
> 9. Backend répond 200 OK à Frontend
>
> **Avantages adapter pattern** :
>
> - **Isolation** : Engine implementation details isolated (could be HTTP, gRPC, message queue later)
> - **Testability** : Backend can mock engine_adapter in tests (no real Engine needed)
> - **Resilience** : Engine timeout? Adapter can retry/fallback
>
> **Code sketch** :
>
> ````python
> # core/use_cases/check_compliance.py
> # Note: Dans l'architecture actuelle, l'appel à l'AI Engine se fait directement
> # via HTTP client, sans adapter pattern pour l'instant
> class CheckCompliance:
>     def analyze(self, data: dict) -> ComplianceResult:
>         response = requests.post(
>             f'{ENGINE_URL}/analyze',
>             json=data,
>             timeout=5
>         )
>         return ComplianceResult.from_dict(response.json())
> ```"
> ````

**Score** : ✅ Montrez compréhension flow + adapter pattern + isolation.

---

#### **Q3 : "Comment le frontend est-il isolé du backend? Montrez un exemple."**

**Réponse attendue** :

> "Frontend communique **uniquement via API client** isolé dans `lib/api.ts`. Cette isolation signifie :
>
> 1. **Toutes requêtes** passent par `lib/api.ts` (point unique)
> 2. Si backend change endpoint, change UNE FOIS dans `lib/api.ts`
> 3. Tous les composants Front continuent marcher (zero refactor)
>
> **Exemple concret** :
>
> **Avant** (mauvais, tight coupling) :
>
> ```typescript
> // components/contact-form.tsx (COUPLÉ à backend)
> const handleSubmit = async (data) => {
>   const res = await fetch("http://localhost:8000/contacts", {
>     method: "POST",
>     body: JSON.stringify(data),
>   });
> };
> // Si endpoint change → modifier ici + 10 autres fichiers
> ```
>
> **Après** (bon, loose coupling) :
>
> ```typescript
> // lib/api.ts (API CLIENT ISOLÉ)
> export const createContact = async (data: Contact) => {
>   return fetch("/api/v1/contacts", {
>     method: "POST",
>     body: JSON.stringify(data),
>     headers: { Authorization: `Bearer ${token}` },
>   });
> };
>
> // components/contact-form.tsx (DÉCOUPLÉ de backend)
> import { createContact } from "@/lib/api";
> const handleSubmit = async (data) => {
>   const result = await createContact(data);
> };
> // Si endpoint change → change dans lib/api.ts seul. Composant untouched.
> ```
>
> **Avantages** :
>
> - ✅ **Centralized** : Auth headers, error handling, retries = un seul endroit
> - ✅ **Testable** : Mock api.ts en tests (no real backend needed)
> - ✅ **Type safety** : TypeScript types alignées avec backend DTOs"

**Score** : ✅ Montrez compréhension API client pattern + code example + avantages.

---

#### **Q4 : "Donnez un exemple de Rule + Detector dans l'Engine."**

**Réponse attendue** :

> "Une **Rule** = une détection spécifique (ex: no_pii_in_prompts). Un **Detector** = implémentation concrète.
>
> **Architecture pattern** : Strategy pattern (interface + implementations pluggables).
>
> **Code** :
>
> ```python
> # ai/detectors/base.py (INTERFACE)
> from abc import ABC, abstractmethod
>
> class Detector(ABC):
>     @abstractmethod
>     def detect(self, text: str) -> DetectionResult:
>         '''Detect violations in text. Return findings.'''
>         pass
>
> # ai/detectors/pii_detector.py (IMPLÉMENTATION)
> import re
>
> class PiiDetector(Detector):
>     PATTERNS = {
>         'email': r'[\\w\\.-]+@[\\w\\.-]+\\.\\w+',
>         'phone': r'\\+?[\\d\\s\\-()]{10,}',
>         'iban': r'^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$'
>     }
>
>     def detect(self, text: str) -> DetectionResult:
>         findings = []
>         for pii_type, pattern in self.PATTERNS.items():
>             matches = re.findall(pattern, text)
>             if matches:
>                 findings.append({
>                     'type': pii_type,
>                     'matches': matches,
>                     'severity': 'HIGH'
>                 })
>         return DetectionResult(
>             rule_name='no_pii_in_prompts',
>             findings=findings,
>             passed=len(findings) == 0
>         )
>
> # ai/pipelines/compliance_pipeline.py (ORCHESTRATION)
> class CompliancePipeline:
>     def __init__(self):
>         self.detectors = [
>             PiiDetector(),
>             SecretsDetector(),
>             ScopeDetector()
>         ]
>
>     def analyze(self, data: dict) -> ComplianceResult:
>         all_findings = []
>         for detector in self.detectors:
>             result = detector.detect(data['text'])
>             all_findings.extend(result.findings)
>
>         # Mask PII before storing
>         masked_data = self.mask_pii(data, all_findings)
>
>         return ComplianceResult(
>             original_data=data,
>             masked_data=masked_data,
>             findings=all_findings,
>             audit_id='audit_123'
>         )
> ```
>
> **Avantages** :
>
> - ✅ **Pluggable** : Ajouter nouveau détecteur? Étendre `Detector` + ajouter à pipeline
> - ✅ **Testable** : Chaque détecteur testé en isolation
> - ✅ **Reusable** : Détecteur peut être utilisé ailleurs (pas couplé à NovaCRM)
> - ✅ **Configurable** : Policies YAML définissent quels détecteurs run"

**Score** : ✅ Montrez compréhension Strategy pattern + code concret + avantages.

---

### ✅ Validation de l'étape

**Checklist — Vous avez compris SECTION B quand** :

- [ ] Vous expliquez **SoC en 1 phrase** : "Chaque module, une responsabilité, une raison de changer"
- [ ] Vous connaissez les **3 modules** et leur responsabilité (backend=orchestration, frontend=UI, engine=compliance)
- [ ] Vous comprenez le **folder structure backend** (core/domain, core/use_cases, infrastructure/http, infrastructure/database, infrastructure/audit)
- [ ] Vous comprenez le **folder structure frontend** (app, components, lib, lib/api, lib/store, lib/types)
- [ ] Vous comprenez le **folder structure engine** (detectors, pipelines, policies)
- [ ] Vous pouvez **dessiner la communication** : Frontend → Backend API → Engine → Audit trail
- [ ] Vous comprenez le **adapter pattern** (backend ↔ engine isolation)
- [ ] Vous comprenez le **API client pattern** (lib/api.ts = point unique backend communication)
- [ ] Vous comprenez le **Strategy pattern** (Detector interface + implémentations pluggables)
- [ ] Vous répondriez aux **4 questions entretien** ci-dessus avec confiance

**Validation pratique** :

```bash
# Terminal : vérifiez la structure
cd /home/renep/dev/nova-crm/backend
test -d core/domain && test -d core/use_cases && test -d infrastructure/http && test -d infrastructure/database && echo "✅ Backend structure OK"

cd /home/renep/dev/nova-crm/frontend
test -d app && test -d components && test -f lib/api.ts && echo "✅ Frontend structure OK"

cd /home/renep/dev/nova-crm/ai
test -d detectors && test -d pipelines && test -d policies && echo "✅ Engine structure OK"

echo "✅ SECTION B validée"
```

---

## 🏗️ LEÇON 2 : Hexagonal Architecture (Ports & Adapters)

### 📍 Le Concept (Théorie)

**Hexagonal Architecture** = Un pattern pour isoler **métier** du **technique**.

**Analogie concrète** : Une batterie.

```
❌ TIGHT COUPLING (batterie soudée à appareil) :
  [Appareil soudé à batterie]
  Si batterie meurt → appareil mort (remplacer tout)

✅ HEXAGONAL (batterie amovible via port) :
  [Appareil] ←PORT→ [Batterie]
  Si batterie meurt → remplacer batterie seul
  Si besoin batterie AA → adapter AA-vers-port
```

**Appliqué à Backend NovaCRM** :

```
[Backend métier (core/)]
  ↓ (PORT DB)
[PostgreSQL adapter (infrastructure/db/)]

[Backend métier (core/)]
  ↓ (PORT API)
[FastAPI adapter (infrastructure/http/)]

[Backend métier (core/)]
  ↓ (PORT Engine)
[Engine adapter (infrastructure/adapters/)]
```

**Avantage** : Si vous changez PostgreSQL → MongoDB, métier inchangé. Change juste l'adapter.

---

### 🚀 Cas d'usage Réel (NovaCRM + AI Hub)

**Scénario** : Vous devez changer de persistance PostgreSQL → MongoDB (pour scaling documents).

**Hexagonal = facile** :

```python
# core/services/contact_service.py (MÉTIER, unchanged)
class ContactService:
    def __init__(self, repository: ContactRepository):  # ← PORT (interface)
        self.repository = repository

    def create_contact(self, data: dict):
        contact = Contact(**data)
        self.repository.save(contact)  # ← Pas d'SQL, abstrait!
        return contact

# infrastructure/db/postgres_adapter.py (ADAPTER PostgreSQL)
class PostgresContactRepository(ContactRepository):
    def save(self, contact: Contact):
        session.add(contact)  # SQLAlchemy
        session.commit()

# infrastructure/db/mongo_adapter.py (ADAPTER MongoDB)
class MongoContactRepository(ContactRepository):
    def save(self, contact: Contact):
        db['contacts'].insert_one(contact.to_dict())  # MongoDB

# infrastructure/http/main.py (INJECTION)
if USE_POSTGRES:
    repository = PostgresContactRepository()
else:
    repository = MongoContactRepository()

service = ContactService(repository=repository)
```

**Résultat** : Métier untouched. Swapper repository = 1 ligne. Tests = facile (mock repository).

---

### 💻 Le Lab Pratique — Ports & Adapters

#### **LAB 2.4 : Identifiez ports & adapters dans le codebase**

```bash
# Terminal
cd /home/renep/dev/nova-crm

# Trouvez les ports (interfaces)
echo "=== PORTS (Interfaces) ==="
grep -r "class.*Repository\|ABC\|@abstractmethod" backend/core/ --include="*.py" | head -20
# Vous verrez : ContactRepository (interface), ContactService (interface), etc

# Trouvez les adapters
echo "=== ADAPTERS (Implémentations) ==="
grep -r "class.*Repository.*:" backend/infrastructure/ --include="*.py" | head -20
# Vous verrez : PostgresContactRepository, MongoContactRepository, etc

# Trouvez l'injection
echo "=== INJECTION ==="
grep -r "repository = " backend/infrastructure/http/main.py | head -5
# Vous verrez : repository = PostgresContactRepository() ou MongoContactRepository()
```

**Résultat attendu** : Vous comprenez

- ✅ Interfaces (ports) dans core/
- ✅ Implémentations (adapters) dans infrastructure/
- ✅ Injection dans http/main.py (point de décision tech)

---

## 🏗️ LEÇON 3 : Design Patterns — Strategy, Factory, Adapter

### 📍 Le Concept (Théorie & Application)

**3 patterns critiques dans NovaCRM** :

| Pattern      | Rôle                         | Exemple                                 |
| ------------ | ---------------------------- | --------------------------------------- |
| **Strategy** | Comportement interchangeable | Detector (PiiDetector, SecretsDetector) |
| **Factory**  | Créer objets polymorphes     | RuleFactory crée rules selon policy     |
| **Adapter**  | Adapter deux interfaces      | EngineAdapter (backend ↔ engine)        |

#### **Pattern 1 : Strategy (Détecteurs pluggables)**

```python
# INTERFACE (port)
from abc import ABC, abstractmethod

class Detector(ABC):
    @abstractmethod
    def detect(self, text: str) -> Result:
        pass

# IMPLÉMENTATIONS (strategies)
class PiiDetector(Detector):
    def detect(self, text: str):
        # PII detection logic
        pass

class SecretsDetector(Detector):
    def detect(self, text: str):
        # Secrets detection logic
        pass

# USAGE
class CompliancePipeline:
    def __init__(self, detectors: List[Detector]):
        self.detectors = detectors  # ← Agnostic, ne sait pas quel detector

    def analyze(self, text: str):
        results = []
        for detector in self.detectors:  # ← Run each strategy
            results.append(detector.detect(text))
        return results

# INSTANTIATION (adapter chooses strategies)
pipeline = CompliancePipeline(detectors=[
    PiiDetector(),
    SecretsDetector(),
    ScopeDetector()
])
```

**Avantage** : Ajouter nouveau detector? Extend Detector + ajouter à list. Pipeline inchangé.

---

#### **Pattern 2 : Factory (Créer rules selon policy)**

```python
# Factory crée detectors selon policy YAML
class DetectorFactory:
    @staticmethod
    def create(rule_name: str) -> Detector:
        if rule_name == 'no_pii':
            return PiiDetector()
        elif rule_name == 'no_secrets':
            return SecretsDetector()
        elif rule_name == 'scope_check':
            return ScopeDetector()
        else:
            raise ValueError(f"Unknown rule: {rule_name}")

# USAGE
policy = load_policy('compliance_policy_v1.yaml')
# policy.rules = ['no_pii', 'no_secrets', 'scope_check']

detectors = [
    DetectorFactory.create(rule_name)
    for rule_name in policy.rules
]

pipeline = CompliancePipeline(detectors=detectors)
```

**Avantage** : Politique définit rules. Factory crée. Pipeline agnostic. Policy-driven.

---

#### **Pattern 3 : Adapter (Backend ↔ Engine)**

```python
# INCOMPATIBLE INTERFACES
# Backend format
backend_data = {
    'contact_id': 123,
    'text': 'My email is sophie@example.com'
}

# Engine expected format
engine_format = {
    'input': 'My email is sophie@example.com',
    'context': {'source': 'email', 'actor': 'sophie'}
}

# ADAPTER : convertir format
class EngineAdapter:
    def analyze(self, backend_data: dict) -> EngineResult:
        # Convert backend format to engine format
        engine_input = {
            'input': backend_data['text'],
            'context': {'source': 'backend', 'actor': backend_data.get('actor')}
        }

        # Call engine
        response = requests.post(
            f'{ENGINE_URL}/analyze',
            json=engine_input
        )

        # Convert engine response back to backend format
        return {
            'contact_id': backend_data['contact_id'],
            'pii_found': response.json()['findings'],
            'masked_data': response.json()['masked']
        }

# USAGE
adapter = EngineAdapter()
result = adapter.analyze(backend_data)
```

**Avantage** : Engine change format? Update adapter seul. Backend untouched.

---

### 💼 Préparation Entretien (Q&A)

#### **Q1 : "Expliquez le Strategy pattern. Pourquoi l'utiliser pour les détecteurs?"**

**Réponse attendue** :

> "Strategy pattern = interface commune pour comportements interchangeables.
>
> **Appliqué à Engine** : Chaque détecteur (PII, secrets, scope) est une stratégie différente, mais tous respectent interface `Detector`.
>
> ```python
> class Detector(ABC):
>     def detect(self, text: str) -> Result: pass
>
> class PiiDetector(Detector):
>     def detect(self, text): return pii_findings
>
> class SecretsDetector(Detector):
>     def detect(self, text): return secret_findings
> ```
>
> **Avantage** :
>
> - ✅ **Pluggable** : Ajouter DetectorX? Extend Detector + ajouter à pipeline. Zéro changement pipeline.
> - ✅ **Testable** : Mock Detector en tests (no real detection needed)
> - ✅ **Reusable** : Détecteur peut servir autre système (pas couplé NovaCRM)
>
> **Sans Strategy** : if/else hardcoded dans pipeline. Ajouter règle = modifier pipeline = risqué.
> **Avec Strategy** : Policies YAML définissent rules. Pipeline agnostic. Safe."

**Score** : ✅ Montrez compréhension interface commune + avantages (pluggable, testable, reusable).

---

#### **Q2 : "Donnez un exemple Factory pattern dans NovaCRM."**

**Réponse attendue** :

> "Factory pattern = créer objets polymorphes sans hardcoding type.
>
> **Exemple Engine** :
>
> ```python
> class DetectorFactory:
>     @staticmethod
>     def create(rule_name: str) -> Detector:
>         REGISTRY = {
>             'no_pii': PiiDetector,
>             'no_secrets': SecretsDetector,
>             'scope_check': ScopeDetector,
>         }
>         detector_class = REGISTRY.get(rule_name)
>         return detector_class() if detector_class else None
> ```
>
> **Usage** :
>
> ```python
> policy = load_yaml('policy.yaml')  # policy.rules = ['no_pii', 'no_secrets']
> detectors = [DetectorFactory.create(rule) for rule in policy.rules]
> pipeline = CompliancePipeline(detectors=detectors)
> ```
>
> **Avantage** :
>
> - ✅ **Data-driven** : Policy YAML définit rules. Factory crée automatiquement.
> - ✅ **Extensible** : Nouvelle règle? Ajouter à REGISTRY. Pas de code change ailleurs.
> - ✅ **Maintainable** : Créations en un endroit. Vs scattered if/else.
>
> **Sans Factory** : `if rule == 'no_pii': detector = PiiDetector()` scattered partout.
> **Avec Factory** : Centralisé, data-driven, versionnié (policy.yaml v1 vs v2)."

**Score** : ✅ Montrez compréhension creation logic centralisée + data-driven + avantages.

---

### ✅ Validation de l'étape — SECTION B complète

**Checklist finale** :

- [ ] Vous expliquez **SoC** (chaque module, responsabilité unique, raison de changer)
- [ ] Vous connaissez les **3 modules** et leurs responsabilités
- [ ] Vous comprenez les **folder structures** (core, infrastructure, adapters)
- [ ] Vous comprenez le **flow** : Frontend → Backend API → Engine → Audit
- [ ] Vous comprenez **Hexagonal Architecture** (ports & adapters, métier isolé)
- [ ] Vous comprenez **Strategy pattern** (Detector interface + implémentations)
- [ ] Vous comprenez **Factory pattern** (créer objets selon policy)
- [ ] Vous comprenez **Adapter pattern** (backend ↔ engine conversion)
- [ ] Vous dessinez **un diagramme** :
  ```
  [Frontend] --API--> [Backend (core + infrastructure)] --Adapter--> [Engine]
  [Backend] --Ports--> [DB Adapter (PostgreSQL/Mongo)]
  [Engine] --Strategy--> [Detectors (PII, Secrets, Scope)]
  ```
- [ ] Vous répondez aux **Q&A** avec confiance (Strategy, Factory, Adapter)

---

**Fin de SECTION B**

✅ **Vous savez maintenant** :

- Pourquoi 3 modules (SoC)
- Comment chaque module est structuré (folder layout)
- Comment modules communiquent (adapters, APIs)
- Patterns critiques (Strategy, Factory, Adapter)
- Pourquoi ces patterns facilitent évolution + testing

➡️ **Prochaine** : SECTION C — FastAPI Backend (code concret)
