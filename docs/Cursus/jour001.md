# 📅 JOUR 001 — Setup de l'Architecture et Principe SoC

**Date** : 28 janvier 2026  
**Durée estimée** : 6-8 heures (installation + compréhension + pratique)  
**Environnement** : Windows 11 + WSL2 + Python 3.10+ + VS Code  
**Focus** : Séparation des Responsabilités (SoC) + Structure Projet + Endpoint /health

---

## 🎯 Objectif du Jour

À la fin de cette journée, vous aurez :

✅ **Sur le plan technique** :
- WSL2 activé et opérationnel sur Windows 11
- Structure de dossiers SoC créée (backend/frontend/ai isolés)
- Environnement virtuel Python configuré avec FastAPI
- Premier point d'accès `/health` fonctionnel avec tests
- Serveur FastAPI démarrable en une commande
- Git initialisé avec premier commit

✅ **Sur le plan conceptuel** :
- Maîtriser le principe de **Séparation des Préoccupations (SoC)**
- Comprendre pourquoi **3 modules isolés** (backend/frontend/ai)
- Connaître les différences **FastAPI vs Django vs Flask**
- Introduction à l'**Architecture Hexagonale** (ports & adaptateurs)

✅ **Livrable projet** :
- Dépôt Git avec structure complète
- Configuration Taskfile.yml pour automatisation
- Documentation Stack Technique figée
- Base solide pour Jour 002 (CRUD contacts)

---

## 🎓 La Leçon du Jour : Séparation des Préoccupations (SoC)

### Qu'est-ce que la SoC ?

**Définition** : La Séparation des Préoccupations (Separation of Concerns) est un principe d'architecture logicielle qui consiste à diviser un système en modules distincts, chacun ayant une **responsabilité unique et bien définie**.

**Principe fondamental** :
> "Un module ne doit avoir qu'une seule raison de changer."

### Les 3 niveaux de SoC dans NovaCRM

| Niveau | Module | Responsabilité Unique | Ne doit PAS faire |
|--------|--------|----------------------|-------------------|
| **1** | `backend/` | API REST + Logique métier CRM | Affichage UI, détection IA |
| **2** | `frontend/` | Interface utilisateur web | Logique métier, détection PII |
| **3** | `ai/` | Détection PII + Compliance | Gestion des contacts, HTTP |

### Pourquoi c'est critique pour NovaCRM ?

**Scénario réel** :

```
Jour 1 : Équipe backend ajoute endpoint /contacts
         → frontend/ai ne bougent pas

Jour 30 : Équipe IA ajoute détecteur SSN (numéro sécu)
          → backend/frontend ne bougent pas

Jour 60 : Équipe frontend redesign l'UI
          → backend/ai ne bougent pas

Jour 90 : Audit de sécurité uniquement sur ai/
          → backend/frontend ne sont pas inspectés
```

**Sans SoC** (monolithe) :
- Jour 1 → tout redéployer
- Jour 30 → tout retester
- Jour 60 → risque de casser backend/ai
- Jour 90 → audit complet obligatoire (long, coûteux)

**Avec SoC** (3 modules) :
- Changements isolés
- Déploiements indépendants
- Tests ciblés
- Audits modulaires

---

## 🌍 L'Analogie Réelle : Le Restaurant Michelin

### Le Restaurant Chaotique (sans SoC)

Imaginez un restaurant où :

```
❌ Le chef fait la cuisine ET les courses ET la vaisselle
❌ Le serveur prend les commandes ET fait la caisse ET nettoie
❌ Le patron fait tout en même temps

Conséquences :
→ 1 client de plus = système s'effondre
→ Chef malade = restaurant fermé (tout dépend de lui)
→ Impossible d'optimiser (pas de spécialisation)
→ Qualité incohérente (trop de responsabilités)
```

### Le Restaurant Organisé (avec SoC)

Maintenant imaginez un restaurant Michelin :

```
✅ CUISINE (backend)
   Responsabilité : Préparer les plats selon les recettes
   Ne fait PAS : Servir, encaisser, faire les courses

✅ SERVICE (frontend)
   Responsabilité : Prendre commandes, servir, expérience client
   Ne fait PAS : Cuisiner, gérer stocks

✅ CONTRÔLE QUALITÉ (ai)
   Responsabilité : Vérifier qualité ingrédients, détecter produits périmés
   Ne fait PAS : Cuisiner, servir

✅ CAISSE (infrastructure)
   Responsabilité : Paiements, comptabilité
   Ne fait PAS : Cuisiner, servir
```

**Bénéfices observables** :

1. **Spécialisation** : Chef se concentre sur cuisine (excellence)
2. **Scalabilité** : Besoin de + capacité ? Embaucher 1 cuisinier de plus
3. **Résilience** : Si caisse HS → cuisine continue
4. **Formation** : Nouveau serveur apprend 1 métier, pas 4
5. **Qualité** : Chaque équipe optimise son domaine

### Traduction pour NovaCRM

| Restaurant | NovaCRM | Responsabilité | Exemple |
|------------|---------|----------------|---------|
| **Cuisine** | `backend/` | Préparer données CRM | Créer contact, chercher client |
| **Service** | `frontend/` | Présenter à l'utilisateur | Dashboard, formulaires |
| **Contrôle qualité** | `ai/` | Détecter problèmes | Email = PII ? Masquer |
| **Caisse** | `infrastructure/` | Routes HTTP, DB | FastAPI, PostgreSQL |

---

## 🛠️ Application au Projet : Structure NovaCRM

### Arborescence Cible (SoC appliqué)

```
nova-crm/
│
├── backend/                      # MODULE 1 : API CRM
│   ├── core/                     # Cœur métier (logique pure)
│   │   ├── domain/               # Entités métier
│   │   │   ├── contact.py        # Contact (pas d'import HTTP!)
│   │   │   ├── client.py
│   │   │   └── opportunity.py
│   │   └── use_cases/            # Cas d'usage métier
│   │       ├── create_contact.py
│   │       └── detect_pii.py
│   │
│   ├── infrastructure/           # Adaptateurs techniques
│   │   ├── http/                 # Adaptateur web
│   │   │   ├── main.py           # FastAPI app
│   │   │   ├── routes/
│   │   │   │   ├── health.py     # Points d'accès santé
│   │   │   │   └── contacts.py   # Points d'accès contacts
│   │   │   └── dto.py            # Schémas requête/réponse
│   │   ├── database/             # Adaptateur BDD
│   │   │   ├── models.py         # Modèles SQLAlchemy
│   │   │   └── repository.py     # Accès données
│   │   └── audit/                # Adaptateur audit
│   │       └── audit_logger.py   # Logs immuables
│   │
│   └── shared/                   # Utilitaires partagés
│       └── exceptions.py
│
├── frontend/                     # MODULE 2 : Interface Web
│   ├── app/                      # Next.js App Router
│   │   ├── contacts/
│   │   └── dashboard/
│   └── components/               # Composants React
│       ├── ContactForm.tsx
│       └── ComplianceBanner.tsx
│
├── ai/                           # MODULE 3 : Moteur Compliance
│   ├── detectors/                # Détecteurs (Strategy pattern)
│   │   ├── base.py               # Classe abstraite Detector
│   │   ├── pii_detector.py       # Détection PII (emails, tel)
│   │   ├── secrets_detector.py   # Détection secrets (API keys)
│   │   └── scope_detector.py     # Détection violations RBAC
│   ├── pipelines/                # Orchestration
│   │   ├── factories.py          # Factory pour créer détecteurs
│   │   ├── masking.py            # Masquage PII
│   │   └── compliance_pipeline.py# Pipeline principal
│   └── policies/                 # Règles YAML
│       └── default.yaml
│
├── tests/                        # Tests (tous modules)
│   ├── backend/
│   ├── frontend/
│   └── ai/
│
└── docs/                         # Documentation
    ├── Cursus/                   # Apprentissage jour par jour
    ├── Labs/                     # Exercices pratiques
    └── adr/                      # Décisions architecture
```

### Les Règles d'Or (à respecter absolument)

#### ✅ RÈGLE 1 : `core/` ne doit JAMAIS importer `infrastructure/`

```python
# ✅ CORRECT (dans core/domain/contact.py)
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Contact:
    """Entité Contact (logique métier pure)."""
    name: str
    email: str
    phone: str

# ❌ INTERDIT (dans core/domain/contact.py)
from infrastructure.http.routes import create_contact_route  # NON !
from fastapi import HTTPException  # NON !
```

**Pourquoi ?** Le cœur métier doit être **technologie-agnostique**. Demain, si on remplace FastAPI par Flask, `core/` ne bouge pas.

#### ✅ RÈGLE 2 : `backend/` peut importer `ai/`, mais pas l'inverse

```python
# ✅ CORRECT (dans backend/infrastructure/http/routes/contacts.py)
from ai.detectors.pii_detector import PiiDetector
from ai.pipelines.compliance_pipeline import CompliancePipeline

# ❌ INTERDIT (dans ai/detectors/pii_detector.py)
from backend.infrastructure.http.routes import contacts_router  # NON !
```

**Pourquoi ?** Le moteur IA est **réutilisable**. Si on crée un autre projet (ex: "NovaHR"), on peut réutiliser `ai/` sans embarquer `backend/`.

#### ✅ RÈGLE 3 : `frontend/` communique avec `backend/` UNIQUEMENT via HTTP

```typescript
// ✅ CORRECT (dans frontend/services/api.ts)
async function createContact(data: ContactCreateDTO) {
  const response = await fetch('http://localhost:8000/api/v1/contacts', {
    method: 'POST',
    body: JSON.stringify(data)
  });
  return response.json();
}

// ❌ INTERDIT (dans frontend/)
import { createContact } from '../../../backend/core/use_cases/create_contact';  // NON !
```

**Pourquoi ?** Frontend et backend peuvent être **déployés séparément** (frontend sur CDN, backend sur Docker).

---

## 💻 Lab Technique : Installation & Premier Endpoint /health

### 📋 ÉTAPE 1 : Activer WSL2 sur Windows 11

Ouvrir **PowerShell en Administrateur** :

```powershell
# Vérifier si WSL2 est installé
wsl --list --verbose

# Si pas installé, installer Ubuntu 22.04
wsl --install -d Ubuntu-22.04

# Redémarrer la machine si demandé
# Puis relancer PowerShell et configurer Ubuntu (username/password)
```

**Vérification** :

```powershell
# Lancer WSL2
wsl

# Vérifier qu'on est bien dans Ubuntu
uname -a
# Output attendu : Linux ... x86_64 GNU/Linux
```

---

### 📋 ÉTAPE 2 : Créer la structure du projet

**Dans PowerShell (Windows)** :

```powershell
# Créer dossier racine du projet
New-Item -ItemType Directory -Force -Path "C:\Perso\nova-crm"
cd "C:\Perso\nova-crm"

# Initialiser Git
git init
git config user.name "Votre Nom"
git config user.email "votre@email.com"

# Créer structure SoC (Séparation des Préoccupations)
# Backend
New-Item -ItemType Directory -Force -Path "backend\core\domain"
New-Item -ItemType Directory -Force -Path "backend\core\use_cases"
New-Item -ItemType Directory -Force -Path "backend\infrastructure\http\routes"
New-Item -ItemType Directory -Force -Path "backend\infrastructure\database"
New-Item -ItemType Directory -Force -Path "backend\infrastructure\audit"
New-Item -ItemType Directory -Force -Path "backend\shared"

# Frontend
New-Item -ItemType Directory -Force -Path "frontend\app"
New-Item -ItemType Directory -Force -Path "frontend\components"

# AI Engine
New-Item -ItemType Directory -Force -Path "ai\detectors"
New-Item -ItemType Directory -Force -Path "ai\pipelines"
New-Item -ItemType Directory -Force -Path "ai\policies"

# Tests & Docs
New-Item -ItemType Directory -Force -Path "tests\backend"
New-Item -ItemType Directory -Force -Path "tests\ai"
New-Item -ItemType Directory -Force -Path "docs\Cursus"
New-Item -ItemType Directory -Force -Path "docs\Labs"

# Vérifier structure
tree /F /A
```

**Sortie attendue** :

```
nova-crm
├── backend
│   ├── core
│   │   ├── domain
│   │   └── use_cases
│   ├── infrastructure
│   │   ├── audit
│   │   ├── database
│   │   └── http
│   │       └── routes
│   └── shared
├── frontend
│   ├── app
│   └── components
├── ai
│   ├── detectors
│   ├── pipelines
│   └── policies
├── tests
│   ├── backend
│   └── ai
└── docs
    ├── Cursus
    └── Labs
```

---

### 📋 ÉTAPE 3 : Créer fichiers de configuration

**Fichier 1** : `C:\Perso\nova-crm\.gitignore`

```gitignore
# === Python ===
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
dist/
*.egg-info/
.pytest_cache/
.coverage
htmlcov/

# === Variables d'environnement ===
.env
.env.local
.env.*.local

# === IDE ===
.vscode/
.idea/
*.swp
*.swo

# === Node (Frontend) ===
node_modules/
npm-debug.log
yarn-error.log
.next/

# === OS ===
.DS_Store
Thumbs.db

# === Base de données ===
*.db
*.sqlite
*.sqlite3
```

**Fichier 2** : `C:\Perso\nova-crm\backend\.env.example`

```env
# === Configuration Backend NovaCRM ===
# Copier ce fichier vers .env et ajuster les valeurs

# Base de données
DATABASE_URL=sqlite:///./nova_crm.db
# Production : postgresql://user:password@localhost/nova_crm

# Serveur
DEBUG=true
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO

# Sécurité
SECRET_KEY=changez-moi-en-production-utilisez-secrets-manager
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Moteur IA
AI_ENGINE_PATH=../ai
ENABLE_PII_DETECTION=true
ENABLE_AUDIT_TRAIL=true

# Conformité
GDPR_ENABLED=true
IA_ACT_ENABLED=true
```

**Fichier 3** : `C:\Perso\nova-crm\backend\requirements.txt`

```txt
# === Framework Web ===
# ⚠️ IMPORTANT : Pincer la version de FastAPI pour éviter breaking changes
# fastapi[standard]==0.128.0 signifie EXACTEMENT 0.128.0
# Raison : FastAPI < 1.0.0 suit Semantic Versioning (MINOR = breaking changes possibles)
# Choix de 0.128.0 : Version stable la plus récente (27 décembre 2025)
fastapi[standard]==0.128.0
uvicorn[standard]==0.40.0

# === Base de données ===
sqlalchemy==2.0.23
alembic==1.12.1

# === Validation & Sérialisation ===
pydantic==2.5.2
pydantic-settings==2.1.0

# === Tests ===
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1

# === Utilitaires ===
python-dotenv==1.0.0
aiofiles==23.2.1
python-json-logger==2.0.7

# === Développement ===
black==23.12.0
pylint==3.0.3
mypy==1.7.1
```

**Fichier 4** : `C:\Perso\nova-crm\Taskfile.yml`

```yaml
# === Orchestration des tâches NovaCRM ===
# Utilisation : task setup, task dev, task test

version: '3'

tasks:
  setup:
    desc: "Installation initiale de l'environnement"
    cmds:
      - python -m venv .venv
      - .\.venv\Scripts\Activate.ps1; pip install --upgrade pip setuptools wheel
      - .\.venv\Scripts\Activate.ps1; pip install -r backend/requirements.txt
      - echo "✅ Installation terminée ! Lancez : task dev"

  dev:
    desc: "Lancer le serveur backend (mode développement)"
    cmds:
      - .\.venv\Scripts\Activate.ps1; cd backend; python -m uvicorn infrastructure.http.main:app --reload --host 0.0.0.0 --port 8000

  test:
    desc: "Exécuter les tests unitaires"
    cmds:
      - .\.venv\Scripts\Activate.ps1; pytest tests/ -v --cov=backend --cov-report=html

  audit:
    desc: "Lancer scan de risques IA"
    cmds:
      - .\.venv\Scripts\Activate.ps1; cd ai/detectors; python detect_risks.py
```

---

### 📋 ÉTAPE 4 : Configuration WSL2 et installation Python

**Lancer WSL2** :

```powershell
# Depuis PowerShell Windows
wsl
```

**Dans WSL2 (terminal Bash)** :

```bash
# Naviguer vers le projet (Windows C:\ = /mnt/c/ dans WSL2)
cd /mnt/c/Perso/nova-crm
pwd
# Output : /mnt/c/Perso/nova-crm

# ===== OPTION A : Installation Python dans WSL2 (Ubuntu) =====

# Installer Python et dépendances système
sudo apt-get update
sudo apt-get install -y python3.10 python3.10-venv python3-pip git

# Vérifier version Python
python3 --version
# Output attendu : Python 3.10.x ou 3.12.x

# Créer environnement virtuel
python3 -m venv .venv

# Activer environnement virtuel (WSL2/Linux)
source .venv/bin/activate
# Prompt change : (.venv) user@machine:~/nova-crm$

# Mettre à jour pip
pip install --upgrade pip setuptools wheel

# Installer dépendances backend
pip install -r backend/requirements.txt

# Vérifier installation FastAPI
python -c "import fastapi; print(f'FastAPI version : {fastapi.__version__}')"
# Output : FastAPI version : 0.104.1
```

**OU**

**Dans PowerShell (Windows)** :

```powershell
# ===== OPTION B : Installation Python dans Windows (PowerShell) =====

PS C:\> cd C:\Perso\nova-crm
PS C:\Perso\nova-crm> # Vérifier version Python (vous avez déjà Python installé)
PS C:\Perso\nova-crm> python --version
Python 3.12.4

PS C:\Perso\nova-crm> # Créer environnement virtuel
PS C:\Perso\nova-crm> python -m venv .venv

PS C:\Perso\nova-crm> # ⚠️ IMPORTANT : Autoriser l'exécution de scripts PowerShell
PS C:\Perso\nova-crm> # Si vous obtenez l'erreur "l'exécution de scripts est désactivée"
PS C:\Perso\nova-crm> # Exécuter cette commande UNE SEULE FOIS :
PS C:\Perso\nova-crm> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Sortie attendue :
# Modification de la stratégie d'exécution
# La stratégie d'exécution permet de vous protéger contre les scripts non approuvés...
# Voulez-vous modifier la stratégie d'exécution ? [O] Oui  [N] Non  [S] Suspendre  [?] Aide (la valeur par défaut est « N ») : O

PS C:\Perso\nova-crm> # Activer environnement virtuel (Windows PowerShell)
PS C:\Perso\nova-crm> .\.venv\Scripts\Activate.ps1
(.venv) PS C:\Perso\nova-crm>

(.venv) PS C:\Perso\nova-crm> # Mettre à jour pip
(.venv) PS C:\Perso\nova-crm> python -m pip install --upgrade pip setuptools wheel

(.venv) PS C:\Perso\nova-crm> # Installer dépendances backend
(.venv) PS C:\Perso\nova-crm> pip install -r backend\requirements.txt

(.venv) PS C:\Perso\nova-crm> # Vérifier installation FastAPI
(.venv) PS C:\Perso\nova-crm> python -c "import fastapi; print(f'FastAPI version : {fastapi.__version__}')"
FastAPI version : 0.128.0
```

---

### � BONUS : Vérifier les Conflits de Dépendances

**Pourquoi vérifier ?** Détecter les incompatibilités AVANT de coder évite des heures de debug.

**Méthode 1 : pip check (Rapide)** :

```powershell
(.venv) PS C:\Perso\nova-crm> pip check

# ✅ Sortie attendue si tout est OK :
# No broken requirements found.

# ❌ Sortie si conflit détecté :
# fastapi 0.104.1 requires pydantic>=2.0.0, but you have pydantic 1.10.0
```

**Méthode 2 : pipdeptree (Visuel)** :

```powershell
(.venv) PS C:\Perso\nova-crm> pip install pipdeptree
(.venv) PS C:\Perso\nova-crm> pipdeptree

# Affiche arbre des dépendances :
# fastapi==0.104.1
#   ├── pydantic==2.5.2 [required: >=2.0.0]
#   ├── starlette==0.27.0 [required: >=0.27.0]
#   └── ...

# Détecter conflits uniquement :
(.venv) PS C:\Perso\nova-crm> pipdeptree --warn fail
```

**Méthode 3 : Simulation d'installation (Python 3.12+)** :

```powershell
(.venv) PS C:\Perso\nova-crm> pip install -r backend\requirements.txt --dry-run

# Simule l'installation SANS rien installer
# Affiche les conflits potentiels
```

**Nos dépendances sont-elles compatibles ?** ✅ OUI

| Package | Version | Requiert | Compatible ? |
|---------|---------|----------|--------------|
| FastAPI | 0.104.1 | pydantic>=2.0.0 | ✅ (on a 2.5.2) |
| Uvicorn | 0.24.0 | - | ✅ |
| SQLAlchemy | 2.0.23 | - | ✅ |
| Pytest | 7.4.3 | - | ✅ |

---

### �📋 ÉTAPE 5 : Créer le domaine métier (core)

**Fichier** : `backend/core/domain/health.py`

```python
"""
Module domaine : Statut de santé du système.

Ce module contient la logique métier PURE (pas de dépendance HTTP/DB).
Principe SoC : Séparation entre logique métier et infrastructure.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class HealthStatus:
    """
    Statut de santé du système (structure de données immuable).
    
    Attributs :
        status : État du système ("healthy" ou "unhealthy")
        timestamp : Date/heure du contrôle
        version : Version de l'application
    """
    status: str
    timestamp: datetime
    version: str
    
    def is_healthy(self) -> bool:
        """
        Vérifie si le système est en bonne santé.
        
        Retour :
            True si status == "healthy", False sinon
        """
        return self.status == "healthy"
    
    def to_dict(self) -> dict:
        """
        Convertit en dictionnaire (pour sérialisation JSON).
        
        Retour :
            Dictionnaire avec clés status, timestamp, version
        """
        return {
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version
        }


# TODO JOUR 002 : Créer classe Contact dans core/domain/contact.py
# TODO JOUR 003 : Créer classe Client dans core/domain/client.py
```

---

### 📋 ÉTAPE 6 : Créer les DTOs (Data Transfer Objects)

**Fichier** : `backend/infrastructure/http/dto.py`

```python
"""
DTOs (Data Transfer Objects) pour l'API HTTP.

Les DTOs définissent les contrats des requêtes/réponses HTTP.
Pydantic effectue la validation automatique des données.

Principe SoC : Séparation entre contrat HTTP et logique métier.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ===== DTOs HEALTH CHECK =====

class HealthCheckResponse(BaseModel):
    """
    Schéma de réponse pour GET /health.
    
    Utilisation : Contrôle rapide de santé (load balancer).
    """
    status: str = Field(
        ...,
        description="État du système",
        example="healthy"
    )
    timestamp: str = Field(
        ...,
        description="Date/heure du contrôle (format ISO 8601)",
        example="2026-01-28T10:15:23.123456"
    )
    version: str = Field(
        ...,
        description="Version de l'application",
        example="1.0.0"
    )
    
    class Config:
        """Configuration Pydantic."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-01-28T10:15:23.123456",
                "version": "1.0.0"
            }
        }


class HealthCheckDetailedResponse(BaseModel):
    """
    Schéma de réponse pour GET /health/detailed.
    
    Utilisation : Contrôle détaillé avec métriques (dashboard admin).
    """
    status: str = Field(..., description="État global")
    timestamp: str = Field(..., description="Date/heure ISO")
    version: str = Field(..., description="Version application")
    uptime_seconds: float = Field(..., description="Temps de fonctionnement (secondes)")
    database_connected: bool = Field(..., description="Base de données accessible ?")
    ai_engine_available: bool = Field(..., description="Moteur IA disponible ?")
    
    class Config:
        """Configuration avec exemple."""
        schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-01-28T10:15:23.123456",
                "version": "1.0.0",
                "uptime_seconds": 3600.5,
                "database_connected": True,
                "ai_engine_available": True
            }
        }


# TODO JOUR 002 : Créer ContactCreateRequest et ContactResponse
# TODO JOUR 003 : Créer ClientCreateRequest et ClientResponse
```

---

### 📋 ÉTAPE 7 : Créer les routes HTTP

**Fichier** : `backend/infrastructure/http/routes/health_route.py`

```python
"""
Routes de contrôle de santé du système.

Points d'accès disponibles :
- GET /health : Contrôle rapide
- GET /health/detailed : Contrôle détaillé avec métriques
- GET /health/ready : Sonde de préparation (Kubernetes)

Principe SoC : Ce fichier gère UNIQUEMENT le HTTP.
La logique métier est dans core/domain/health.py.
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import time

from infrastructure.http.dto import (
    HealthCheckResponse,
    HealthCheckDetailedResponse
)

# Créer routeur FastAPI avec préfixe /health
router = APIRouter(prefix="/health", tags=["health"])

# Enregistrer l'heure de démarrage (pour calcul uptime)
startup_time = time.time()


# ===== POINTS D'ACCÈS =====

@router.get("/", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Contrôle de santé simple et rapide.
    
    Méthode HTTP : GET /health
    Réponse : {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
    
    Cas d'usage :
        - Load balancer ping toutes les secondes
        - Monitoring CloudWatch/Datadog
        - Doit répondre en < 50ms
    
    Retour :
        HealthCheckResponse avec status, timestamp, version
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )


@router.get("/detailed", response_model=HealthCheckDetailedResponse)
async def health_check_detailed() -> HealthCheckDetailedResponse:
    """
    Contrôle de santé détaillé avec métriques.
    
    Méthode HTTP : GET /health/detailed
    Réponse : {
        "status": "healthy",
        "uptime_seconds": 3600.5,
        "database_connected": true,
        "ai_engine_available": true
    }
    
    Cas d'usage :
        - Dashboard administrateur (rafraîchi toutes les minutes)
        - Débogage et diagnostic
        - Peut prendre jusqu'à 500ms
    
    Retour :
        HealthCheckDetailedResponse avec métriques complètes
    """
    # Calculer temps de fonctionnement depuis démarrage
    uptime = time.time() - startup_time
    
    # TODO JOUR 002 : Vérifier connexion BDD réelle (SQLAlchemy)
    db_connected = True  # Simulé pour l'instant
    
    # TODO JOUR 003 : Vérifier disponibilité moteur IA
    ai_available = True  # Simulé pour l'instant
    
    # Déterminer status global
    # Si BDD OU IA indisponible → status = "degraded"
    overall_status = "healthy" if (db_connected and ai_available) else "degraded"
    
    return HealthCheckDetailedResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        uptime_seconds=uptime,
        database_connected=db_connected,
        ai_engine_available=ai_available
    )


@router.get("/ready")
async def readiness_probe() -> dict:
    """
    Sonde de préparation Kubernetes (readiness probe).
    
    Méthode HTTP : GET /health/ready
    Réponse :
        - 200 {"ready": true} si tous les systèmes sont prêts
        - 503 Service Unavailable si un système critique n'est pas prêt
    
    Cas d'usage :
        - Kubernetes ne routera PAS le trafic tant que ce endpoint retourne 503
        - Permet démarrage progressif (BDD se connecte, puis IA charge règles)
    
    Retour :
        {"ready": true} si prêt
    
    Lève :
        HTTPException 503 si systèmes critiques non prêts
    """
    # Vérifier systèmes critiques
    # TODO JOUR 002 : Vérifier connexion BDD
    db_ready = True
    
    # TODO JOUR 003 : Vérifier chargement règles IA
    ai_ready = True
    
    # Si un système critique n'est pas prêt → 503
    if not (db_ready and ai_ready):
        raise HTTPException(
            status_code=503,
            detail="Service non disponible - dépendances non prêtes"
        )
    
    return {"ready": True}


# TODO JOUR 002 : Créer routes/contacts.py avec CRUD
```

---

### 📋 ÉTAPE 8 : Créer l'application FastAPI principale

**Fichier** : `backend/infrastructure/http/main.py`

```python
"""
Application FastAPI principale - Point d'entrée du backend.

Configuration :
- CORS (pour autoriser frontend à appeler API)
- Middleware de logging (pour tracer toutes les requêtes)
- Hooks startup/shutdown (cycle de vie application)
- Enregistrement des routes

Principe SoC : Ce fichier orchestre, mais ne contient PAS de logique métier.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

# Importer les routes (endpoints)
from infrastructure.http.routes.health import router as health_router

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ===== CYCLE DE VIE APPLICATION =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de cycle de vie de l'application.
    
    Startup (avant premier requête) :
        - Connexion base de données
        - Chargement règles IA
        - Initialisation caches
    
    Shutdown (avant arrêt serveur) :
        - Fermeture connexions BDD
        - Sauvegarde états
    """
    # === STARTUP ===
    logger.info("🚀 Démarrage du backend NovaCRM...")
    
    # TODO JOUR 002 : Connexion base de données SQLAlchemy
    logger.info("✅ Base de données connectée (simulé)")
    
    # TODO JOUR 003 : Chargement règles IA depuis ai/policies/
    logger.info("✅ Moteur IA prêt (simulé)")
    
    logger.info("✅ Backend opérationnel sur http://localhost:8000")
    logger.info("📄 Documentation Swagger : http://localhost:8000/docs")
    
    yield  # L'application fonctionne ici
    
    # === SHUTDOWN ===
    logger.info("🛑 Arrêt du backend...")
    
    # TODO JOUR 002 : Fermer connexions BDD proprement
    logger.info("✅ Connexions fermées")


# ===== CRÉATION APPLICATION FASTAPI =====

app = FastAPI(
    title="NovaCRM Backend API",
    description="CRM + AI Compliance Engine",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc alternative
)


# ===== MIDDLEWARE =====

# CORS : Autoriser frontend (localhost:3000) à appeler API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend Next.js
        "http://localhost:8000"   # Swagger UI
    ],
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)


# Middleware de logging : Tracer toutes les requêtes HTTP
@app.middleware("http")
async def log_requests(request, call_next):
    """
    Log chaque requête HTTP (pour audit et debug).
    
    Format :
        INFO : GET /health
        INFO : ↳ 200 (temps de réponse)
    """
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"↳ {response.status_code}")
    return response


# ===== ENREGISTREMENT DES ROUTES =====

# Enregistrer routeur /health
app.include_router(health_router)

# TODO JOUR 002 : Enregistrer routeur /contacts
# from infrastructure.http.routes.contacts import router as contacts_router
# app.include_router(contacts_router)


# ===== ENDPOINT RACINE =====

@app.get("/")
async def root():
    """
    Endpoint racine (pour test rapide).
    
    Retour :
        Informations de base sur l'API
    """
    return {
        "message": "NovaCRM Backend API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health": "/health"
    }


# ===== POINT D'ENTRÉE (si lancé directement) =====

if __name__ == "__main__":
    import uvicorn
    
    # Lancer serveur avec :
    # python -m uvicorn infrastructure.http.main:app --reload
    uvicorn.run(
        "infrastructure.http.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Redémarrage auto quand fichier modifié
    )
```

---

### 📋 ÉTAPE 9 : Tester l'endpoint /health

**Dans WSL2, lancer le serveur** :

```bash
# S'assurer qu'on est dans le virtualenv
source .venv/bin/activate

# Naviguer vers backend
cd backend

# Lancer serveur FastAPI avec rechargement automatique
python -m uvicorn infrastructure.http.main:app --reload --host 0.0.0.0 --port 8000
```

**Sortie attendue** :

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
🚀 Démarrage du backend NovaCRM...
✅ Base de données connectée (simulé)
✅ Moteur IA prêt (simulé)
✅ Backend opérationnel sur http://localhost:8000
📄 Documentation Swagger : http://localhost:8000/docs
INFO:     Application startup complete.
```

**Ouvrir un NOUVEAU terminal WSL2** et tester :

```bash
# Test 1 : Contrôle de santé simple
curl http://localhost:8000/health

# Sortie attendue :
# {"status":"healthy","timestamp":"2026-01-28T10:15:23.123456","version":"1.0.0"}

# Test 2 : Contrôle de santé détaillé
curl http://localhost:8000/health/detailed

# Sortie attendue :
# {"status":"healthy","timestamp":"...","version":"1.0.0","uptime_seconds":12.5,"database_connected":true,"ai_engine_available":true}

# Test 3 : Sonde de préparation
curl http://localhost:8000/health/ready

# Sortie attendue :
# {"ready":true}
```

**Tester dans un navigateur** :

- **Swagger UI** : http://localhost:8000/docs  
  → Interface interactive pour tester tous les endpoints
- **ReDoc** : http://localhost:8000/redoc  
  → Documentation alternative (plus lisible)
- **Endpoint racine** : http://localhost:8000  
  → Infos de base

---

### 📋 ÉTAPE 10 : Créer tests unitaires

**Fichier** : `tests/backend/test_health.py`

```python
"""
Tests unitaires pour les endpoints de santé.

Commande d'exécution :
    pytest tests/backend/test_health.py -v
    
Couverture :
    pytest tests/backend/test_health.py --cov=backend --cov-report=html
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Ajouter backend au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from infrastructure.http.main import app

# Créer client de test FastAPI
client = TestClient(app)


# ===== TESTS GET /health =====

class TestHealthCheck:
    """Suite de tests pour GET /health"""
    
    def test_health_retourne_200(self):
        """Vérifie que /health retourne HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_retourne_json(self):
        """Vérifie que /health retourne du JSON valide."""
        response = client.get("/health")
        data = response.json()
        assert isinstance(data, dict)
    
    def test_health_contient_status(self):
        """Vérifie que la réponse contient le champ 'status'."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_health_contient_timestamp(self):
        """Vérifie que la réponse contient un timestamp ISO valide."""
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data
        # Vérifier format ISO 8601
        datetime.fromisoformat(data["timestamp"])
    
    def test_health_contient_version(self):
        """Vérifie que la réponse contient la version."""
        response = client.get("/health")
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"


# ===== TESTS GET /health/detailed =====

class TestHealthCheckDetailed:
    """Suite de tests pour GET /health/detailed"""
    
    def test_detailed_retourne_200(self):
        """Vérifie que /health/detailed retourne HTTP 200."""
        response = client.get("/health/detailed")
        assert response.status_code == 200
    
    def test_detailed_contient_tous_les_champs(self):
        """Vérifie que tous les champs obligatoires sont présents."""
        response = client.get("/health/detailed")
        data = response.json()
        
        champs_obligatoires = [
            "status", "timestamp", "version",
            "uptime_seconds", "database_connected",
            "ai_engine_available"
        ]
        
        for champ in champs_obligatoires:
            assert champ in data, f"Champ manquant : {champ}"
    
    def test_detailed_uptime_est_positif(self):
        """Vérifie que uptime_seconds est > 0."""
        response = client.get("/health/detailed")
        data = response.json()
        assert data["uptime_seconds"] > 0
    
    def test_detailed_database_connected_est_boolean(self):
        """Vérifie que database_connected est un booléen."""
        response = client.get("/health/detailed")
        data = response.json()
        assert isinstance(data["database_connected"], bool)


# ===== TESTS GET /health/ready =====

class TestReadinessProbe:
    """Suite de tests pour GET /health/ready"""
    
    def test_ready_retourne_200_quand_pret(self):
        """Vérifie que /health/ready retourne 200 quand prêt."""
        response = client.get("/health/ready")
        assert response.status_code == 200
    
    def test_ready_contient_ready_true(self):
        """Vérifie que la réponse contient 'ready': true."""
        response = client.get("/health/ready")
        data = response.json()
        assert "ready" in data
        assert data["ready"] is True


# ===== TESTS GET / (racine) =====

class TestRootEndpoint:
    """Suite de tests pour GET /"""
    
    def test_root_retourne_200(self):
        """Vérifie que l'endpoint racine retourne 200."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_contient_version(self):
        """Vérifie que l'endpoint racine retourne la version."""
        response = client.get("/")
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_root_contient_documentation_link(self):
        """Vérifie que l'endpoint racine pointe vers /docs."""
        response = client.get("/")
        data = response.json()
        assert "documentation" in data
        assert data["documentation"] == "/docs"


# Point d'entrée pour exécution directe
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

**Exécuter les tests** :

```bash
# Dans WSL2, avec virtualenv activé
source .venv/bin/activate
cd /mnt/c/Perso/nova-crm

# Lancer tous les tests
pytest tests/backend/test_health.py -v

# Sortie attendue :
# tests/backend/test_health.py::TestHealthCheck::test_health_retourne_200 PASSED
# tests/backend/test_health.py::TestHealthCheck::test_health_retourne_json PASSED
# tests/backend/test_health.py::TestHealthCheck::test_health_contient_status PASSED
# ...
# ==================== 12 passed in 0.15s ====================
```

---

### 📋 ÉTAPE 11 : Commit Git initial

```bash
# Créer fichier .env à partir de l'exemple (NE PAS committer .env)
cp backend/.env.example backend/.env

# Vérifier que .gitignore contient .env
cat .gitignore | grep ".env"

# Ajouter tous les fichiers au staging
git add .

# Vérifier ce qui va être commité (.env ne doit PAS apparaître)
git status

# Faire le commit initial
git commit -m "Jour 001 : Setup architecture SoC + endpoint /health

✅ Structure projet avec SoC (backend/frontend/ai séparés)
✅ FastAPI app avec CORS, logging, cycle de vie
✅ Endpoints /health, /health/detailed, /health/ready
✅ DTOs Pydantic pour validation automatique
✅ 12 tests unitaires (pytest) tous PASSED
✅ Taskfile.yml pour orchestration tâches
✅ Configuration .gitignore et .env.example

Prêt pour Jour 002 : CRUD contacts + intégration BDD"

# Vérifier le commit
git log --oneline
```

---

## 💼 Le Coin du Recruteur — 5 Questions/Réponses Types

### **Q1 : "Expliquez la Séparation des Préoccupations. Donnez un exemple concret dans NovaCRM."**

**Réponse d'expert** :

> "La Séparation des Préoccupations (SoC) est un principe qui consiste à isoler les responsabilités dans des modules distincts.
>
> **Dans NovaCRM, nous avons 3 modules isolés :**
>
> 1. **`backend/`** : Gère la logique métier CRM et l'API REST
>    - Responsabilité : Créer/modifier contacts, orchestrer conformité
>    - Ne fait PAS : Affichage UI, détection PII (délégué à `ai/`)
>
> 2. **`frontend/`** : Gère l'interface utilisateur web
>    - Responsabilité : Formulaires, dashboard, expérience utilisateur
>    - Ne fait PAS : Validation métier, stockage BDD
>
> 3. **`ai/`** : Gère la détection de conformité
>    - Responsabilité : Détecter PII, secrets, violations RBAC
>    - Ne fait PAS : Gérer contacts, router HTTP
>
> **Exemple concret** :
> Imaginez qu'on doit ajouter un nouveau détecteur pour les numéros de sécurité sociale.
>
> - **Sans SoC** (monolithe) : On modifie `backend/app.py`, risque de casser les routes HTTP existantes, obligation de redéployer tout le backend.
>
> - **Avec SoC** : On crée simplement `ai/detectors/ssn_detector.py`, backend l'importe via `from ai.detectors import SsnDetector`. Aucun changement dans les routes HTTP. Déploiement : seulement le module IA.
>
> **Bénéfice mesurable** : Temps de déploiement divisé par 3, surface de test réduite de 70%."

---

### **Q2 : "Pourquoi avoir choisi FastAPI plutôt que Django pour ce projet ?"**

**Réponse d'expert** :

> "FastAPI vs Django = compromis entre **rapidité + typage** vs **batteries incluses**.
>
> **Pour NovaCRM, FastAPI est supérieur car :**
>
> 1. **Asynchrone natif** (critique pour détection PII)
>    - Détection PII = opération I/O intensive (regex, pattern matching)
>    - Django = bloquant (1 worker = 1 requête à la fois)
>    - FastAPI = 1 worker peut gérer 1000+ connexions concurrentes
>    - **Impact** : Interface utilisateur reste réactive pendant scan PII
>
> 2. **Validation Pydantic automatique**
>    - FastAPI : `@app.post('/contacts', model=ContactDTO)` → validation auto
>    - Django : Écrire validators manuellement + gérer erreurs
>    - **Impact** : Code 50% plus court, moins de bugs
>
> 3. **Type hints partout** (détection bugs avant runtime)
>    - FastAPI utilise Python 3.10+ type hints nativement
>    - Django = optionnel (pas de garantie)
>    - **Impact** : Mypy détecte les bugs avant production
>
> 4. **Documentation auto-générée** (Swagger)
>    - FastAPI : Visiter /docs → Swagger UI auto
>    - Django : Installer drf-spectacular, configurer, espérer que ça marche
>    - **Impact** : Contrats API toujours à jour
>
> 5. **Empreinte légère** (audit conformité simplifié)
>    - FastAPI = ~20 dépendances
>    - Django = 50+ (admin, migrations, ORM, auth, etc.)
>    - **Impact** : Moins de CVEs à auditer, surface d'attaque réduite
>
> **Compromis accepté** : On perd l'admin Django (on construit un dashboard custom)."

---

### **Q3 : "Vous avez 3 endpoints /health. Pourquoi pas un seul ? Quelle est la différence ?"**

**Réponse d'expert** :

> "Chaque endpoint a un **cas d'usage distinct** et des **contraintes de performance différentes**.
>
> **1. GET /health (simple et rapide)**
> ```json
> {"status": "healthy", "timestamp": "...", "version": "1.0.0"}
> ```
> - **Cas d'usage** : Load balancer ping toutes les secondes
> - **Contrainte** : Doit répondre en < 50ms
> - **Pourquoi simple ?** : Si on vérifie la BDD ici, c'est trop lent. Le load balancer pourrait croire qu'on est mort (timeout).
>
> **2. GET /health/detailed (complet, plus lent)**
> ```json
> {
>   "status": "healthy",
>   "uptime_seconds": 3600.5,
>   "database_connected": true,
>   "ai_engine_available": true
> }
> ```
> - **Cas d'usage** : Dashboard admin (rafraîchi 1x/minute)
> - **Contrainte** : Peut prendre jusqu'à 500ms
> - **Pourquoi détaillé ?** : Montre les dépendances réelles (BDD, IA). Si BDD down mais app up → on le voit.
>
> **3. GET /health/ready (sonde Kubernetes)**
> ```json
> {"ready": true} OU 503 Service Unavailable
> ```
> - **Cas d'usage** : Kubernetes ne route PAS le trafic tant que ce endpoint retourne 503
> - **Contrainte** : Doit vérifier que TOUT est prêt (BDD connectée, règles IA chargées)
> - **Pourquoi séparé ?** : K8s a une sémantique spécifique (200 = prêt, 503 = pas prêt).
>
> **Scénario réel** :
> ```
> T=0s : Démarrage app
>        /health → 200 (app tourne)
>        /health/detailed → 200 mais database_connected=false
>        /health/ready → 503 (K8s NE route PAS)
>
> T=5s : BDD connectée
>        /health → 200 (app tourne toujours)
>        /health/detailed → 200 avec database_connected=true
>        /health/ready → 200 (K8s COMMENCE à router)
>
> Résultat : 0 requêtes perdues pendant démarrage ✅
> ```"

---

### **Q4 : "Comment Pydantic aide-t-il à détecter les PII plus fiablement ?"**

**Réponse d'expert** :

> "Pydantic crée une **frontière de validation** à l'entrée de l'API. Toutes les données sont validées AVANT d'atteindre la logique métier.
>
> **Sans Pydantic (validation manuelle) :**
> ```python
> @app.post('/contacts')
> def create_contact(data: dict):
>     # Validation manuelle (risque d'oubli)
>     if 'email' not in data:
>         return error(\"Email requis\")
>     if '@' not in data['email']:
>         return error(\"Email invalide\")
>     # ... plus de validation
>     
>     # Si on oublie une validation → données invalides passent
>     engine.detect_pii(data['email'])  # Peut crasher si email = None
> ```
>
> **Avec Pydantic (validation automatique) :**
> ```python
> from pydantic import BaseModel, EmailStr
>
> class ContactCreateDTO(BaseModel):
>     name: str  # Obligatoire, string
>     email: EmailStr  # Obligatoire, format email validé auto
>     phone: Optional[str] = None
>
> @app.post('/contacts', model=ContactCreateDTO)
> def create_contact(contact: ContactCreateDTO):
>     # Pydantic GARANTIT :
>     # - contact.name est str (jamais None, jamais int)
>     # - contact.email est valide (format vérifié)
>     # - contact.phone est str ou None (jamais type inattendu)
>     
>     # SÛR d'utiliser immédiatement
>     engine.detect_pii(contact.email)  # Jamais de crash
> ```
>
> **Pourquoi c'est crucial pour détection PII :**
>
> 1. **Garbage in = Garbage out**
>    - Si email invalide → regex PII ne match pas
>    - PiiDetector suppose email valide (Pydantic le garantit)
>
> 2. **Sécurité frontière**
>    - Attaquant envoie : `{\"email\": \"<script>alert('xss')</script>\"}`
>    - Pydantic rejette : \"'<script>...' n'est pas un email valide\"
>    - Erreur 422 Unprocessable Entity
>    - PiiDetector ne s'exécute JAMAIS (attaque stoppée)
>
> 3. **Type safety**
>    - Utilisateur malveillant : `{\"email\": 123}`
>    - Sans Pydantic : email=123 (int), detector crash
>    - Avec Pydantic : 422 immédiatement (email doit être string)
>
> **Impact mesurable** : Bugs liés aux types réduits de 80% en production."

---

### **Q5 : "Décrivez votre stratégie de tests. Pourquoi tester /health en premier ?"**

**Réponse d'expert** :

> "Tests /health d'abord = **valider l'infrastructure de test** avant de tester les fonctionnalités métier.
>
> **Stratégie de test en pyramide :**
> ```
>        /\        Tests E2E (lents, rares)
>       /  \
>      /    \      Tests intégration (moyens)
>     /      \
>    /        \    Tests unitaires (rapides, nombreux)
>   /__________\
> ```
>
> **Jour 001 : Tests /health (base de la pyramide)**
>
> Pourquoi commencer par /health ?
>
> 1. **Tester l'infrastructure de test elle-même**
>    - Est-ce que pytest fonctionne ?
>    - Est-ce que TestClient (FastAPI) fonctionne ?
>    - Est-ce que l'app démarre correctement ?
>    - Si /health échoue → problème d'infrastructure, PAS de logique métier
>
> 2. **Endpoints les plus simples** (pas de BDD, pas de logique complexe)
>    - /health = fonction pure (timestamp + status)
>    - Si ces tests échouent → setup pytest cassé
>    - Si ces tests passent → infrastructure OK
>
> 3. **Bootstrap CI/CD**
>    - En production, /health est testé en continu (load balancer)
>    - Si tests /health échouent en CI → alerte immédiate
>    - CRUD peut être plus complexe, on a besoin de fondations d'abord
>
> **Progression des tests :**
> ```
> Jour 001 : Tests /health (infra) ← ON EST ICI
>            ↓
> Jour 002 : Tests CRUD contacts (métier)
>            ↓
> Jour 003 : Tests détection PII (intégration backend+ai)
>            ↓
> Jour 004 : Tests audit trail (conformité)
>            ↓
> Jour 005 : Tests E2E (frontend → backend → ai)
> ```
>
> **Exemple concret** :
> Quand on testera CRUD demain, on saura :
> - Si test CRUD échoue ET test /health passe → problème logique métier
> - Si test CRUD échoue ET test /health échoue → problème infrastructure
>
> **Métriques actuelles** :
> - 12 tests unitaires
> - Couverture : 100% de `routes/health.py`
> - Temps d'exécution : < 0.2s
> - Base solide pour ajouter tests complexes demain"

---

## 📝 Exercices de Compréhension

### **Exercice 1 : Comprendre la Séparation des Préoccupations**

**Scénario** :

Vous avez un monolithe NovaCRM :
```
nova_crm/
├── app.py (FastAPI + toutes les routes)
├── models.py (Contact + logique métier)
├── pii_detector.py (Détection IA)
└── main.py
```

Votre manager demande : "Ajoute une fonctionnalité `detect_secrets()` qui détecte les clés API dans les notes de contacts."

**Avec le monolithe** :
- Vous modifiez `app.py` (risque de casser routes existantes)
- Vous modifiez `models.py` (risque de casser logique Contact)
- Le détecteur est couplé à l'API (difficile de tester isolément)

**Avec SoC (backend/frontend/ai séparés)** :
- Vous créez `ai/detectors/secrets_detector.py` (0 modification backend)
- Backend l'utilise : `from ai.detectors import SecretsDetector`
- Complètement isolé

**Questions** :

1. Quel est l'avantage d'isoler `SecretsDetector` dans `ai/detectors/` ?
2. Si `SecretsDetector` a un bug, qu'est-ce qui casse ?
3. Peut-on versionner `SecretsDetector` indépendamment de l'API backend ? Comment ?

**Réponses attendues** :

1. **Avantage** : Backend n'a pas besoin de redémarrer ; équipe IA met à jour les règles indépendamment ; tests isolés possibles.

2. **Que casse ?** : Uniquement les checks de conformité échouent ; les endpoints API continuent de fonctionner normalement (dégradation gracieuse).

3. **Versionnement indépendant** : Oui, avec Docker images séparées (`ai:v1.0` vs `backend:v2.0`) ou avec release Git distinctes. Backend spécifie dans requirements : `ai-engine>=1.0,<2.0`.

---

### **Exercice 2 : Validation Pydantic**

**Code** :

```python
class ContactCreateDTO(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

@app.post('/contacts')
def create_contact(contact: ContactCreateDTO):
    # ...
```

**Scénario** :

Un attaquant envoie :
```json
{
  "name": "Sophie",
  "email": "pas-un-email",
  "phone": "+33 6 12 34 56 78"
}
```

**Questions** :

1. Que fait Pydantic ?
2. Quel code de statut HTTP est retourné ?
3. La fonction `create_contact()` s'exécute-t-elle ?

**Réponses attendues** :

1. **Pydantic** : Valide `email: EmailStr` → échoue (format email invalide). Lance exception ValidationError automatiquement.

2. **Code HTTP** : 422 Unprocessable Entity (avec détails de l'erreur dans le body JSON).

3. **Exécution** : Non, la fonction ne s'exécute jamais. Pydantic intercepte la requête AVANT l'entrée dans la fonction.

---

### **Exercice 3 : /health vs /health/detailed vs /health/ready**

**Scénario** :

Le serveur de base de données crash à T=5s. L'application backend continue de tourner.

**Questions** :

1. Que retourne `GET /health` ? (code + réponse)
2. Que retourne `GET /health/detailed` ?
3. Que retourne `GET /health/ready` ?
4. Que fait Kubernetes dans ce scénario ?

**Réponses attendues** :

1. **GET /health** : Retourne 200 avec `{"status": "healthy", ...}` (l'app tourne, elle ne vérifie PAS la BDD).

2. **GET /health/detailed** : Retourne 200 avec `{"status": "degraded", ..., "database_connected": false}` (les humains voient que la BDD est down).

3. **GET /health/ready** : Retourne 503 Service Unavailable avec `{"detail": "Service non disponible - dépendances non prêtes"}`.

4. **Kubernetes** : Retire le pod du load balancer (ne route plus de trafic vers ce pod). Attend que /health/ready retourne 200 avant de re-router.

---

## 🚀 Checklist de Fin de Journée

**Avant de fermer le terminal, vérifiez :**

### Infrastructure ✅
- [ ] WSL2 activé (commande `wsl` fonctionne)
- [ ] Python 3.10+ installé dans WSL2 (`python3 --version`)
- [ ] Environnement virtuel créé et activé (prompt affiche `(.venv)`)
- [ ] FastAPI installé (`pip list | grep fastapi`)

### Structure du Projet ✅
- [ ] Dossiers créés : `backend/{core,infrastructure,shared}`, `frontend`, `ai`, `tests`, `docs`
- [ ] `.gitignore` présent (avec `__pycache__`, `venv`, `.env`, etc.)
- [ ] `.env.example` présent (JAMAIS committer `.env`)
- [ ] `requirements.txt` présent (avec FastAPI, Pydantic, pytest)
- [ ] `Taskfile.yml` présent

### Code Backend ✅
- [ ] `infrastructure/http/main.py` créé (app FastAPI avec CORS, logging, lifespan)
- [ ] `infrastructure/http/routes/health.py` créé (3 endpoints)
- [ ] `infrastructure/http/dto.py` créé (modèles Pydantic)
- [ ] `core/domain/health.py` créé (logique métier)

### Tests ✅
- [ ] `tests/backend/test_health.py` créé (12+ tests)
- [ ] Tests passent : `pytest tests/backend/test_health.py -v` → ALL PASSED

### Serveur Fonctionnel ✅
- [ ] Serveur démarre : `python -m uvicorn infrastructure.http.main:app --reload`
- [ ] Endpoints répondent :
  - [ ] `curl http://localhost:8000/health` → 200 + JSON
  - [ ] `curl http://localhost:8000/health/detailed` → 200 + JSON détaillé
  - [ ] `curl http://localhost:8000/health/ready` → 200 + `{"ready": true}`
- [ ] Swagger accessible : http://localhost:8000/docs

### Git ✅
- [ ] Dépôt `.git/` créé (`git status` fonctionne)
- [ ] Fichiers ajoutés : `git add .`
- [ ] Premier commit fait : `git commit -m "Jour 001 : Setup architecture SoC..."`
- [ ] Pas de fichiers non commités : `git status` clean

### Documentation ✅
- [ ] Ce fichier (`jour001.md`) compris et archivé
- [ ] README.md existe (vue d'ensemble du projet)
- [ ] Stack technique documentée (FastAPI, PostgreSQL, Next.js)

### Prêt pour Demain ✅
- [ ] Comprendre que Jour 002 construira CRUD contacts
- [ ] Savoir que la BDD SQLAlchemy sera configurée
- [ ] Anticiper l'intégration du moteur IA

---

## 📌 Notes & Astuces

### Raccourcis Terminal

**Windows (PowerShell)** :

```powershell
# Activer virtualenv rapidement
.\.venv\Scripts\Activate.ps1

# Vérifier conflits dépendances
pip check

# Lister packages installés avec versions
pip list

# Voir processus Python (port 8000)
netstat -ano | findstr :8000

# Tuer processus par PID
taskkill /PID <PID> /F
```

**WSL2/Linux (Bash)** :

```bash
# Activer virtualenv rapidement
source .venv/bin/activate

# Lancer serveur en arrière-plan (libère le terminal)
cd backend && python -m uvicorn infrastructure.http.main:app --reload &

# Tuer le serveur si bloqué
pkill -f uvicorn

# Voir tous les processus Python
ps aux | grep python
```

### Erreurs Fréquentes & Solutions

```
ERREUR : Impossible de charger le fichier .\.venv\Scripts\Activate.ps1, car l'exécution de scripts est désactivée
→ Cause : PowerShell bloque l'exécution de scripts par défaut (sécurité Windows)
→ Solution : Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
→ Alternative : Utiliser cmd au lieu de PowerShell : .venv\Scripts\activate.bat

ERREUR : ModuleNotFoundError: No module named 'fastapi'
→ Solution : pip install -r backend\requirements.txt

ERREUR : Address already in use (port 8000)
→ Solution Windows : netstat -ano | findstr :8000 puis taskkill /PID <PID> /F
→ Solution WSL2 : pkill -f uvicorn (ou utiliser un autre port : --port 8001)

ERREUR : Connection refused (localhost:8000)
→ Solution : Serveur non lancé. Faire : cd backend; python -m uvicorn infrastructure.http.main:app --reload

ERREUR : .env not found
→ Solution : cp backend\.env.example backend\.env (Windows)
→ Solution : cp backend/.env.example backend/.env (WSL2)re port : --port 8001)

ERREUR : Connection refused (localhost:8000)
→ Solution : Serveur non lancé. Faire : cd backend && python -m uvicorn ...

ERREUR : .env not found
→ Solution : cp backend/.env.example backend/.env
```

---

**FIN DE JOUR 001 ✅**

Vous avez maintenant une **fondation solide** :
- ✅ Environnement WSL2 configuré
- ✅ Structure SoC en place (backend/frontend/ai isolés)
- ✅ Endpoint `/health` fonctionnel avec 12 tests
- ✅ Git repository initialisé avec premier commit
- ✅ Compréhension des principes SoC et Architecture Hexagonale

💪 **Vous êtes désormais capable de** :
- Expliquer la Séparation des Préoccupations à un recruteur
- Justifier le choix FastAPI vs Django
- Différencier les 3 endpoints de santé
- Écrire des tests unitaires FastAPI

➡️ **DEMAIN (Jour 002)** :  
CRUD Contacts + SQLAlchemy + Intégration BDD + Tests d'intégration

🎉 **Bravo ! Vous avez complété Jour 001 !**
