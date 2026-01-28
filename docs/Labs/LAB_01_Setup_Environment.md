# 🧪 LAB 1 — Setup Environment Local (WSL2, Taskfile, Git)

**Durée estimée** : 1-2 heures  
**Prérequis** : Windows avec WSL2 configuré, Visual Studio Code  
**Objectif** : Préparer environnement local pour développement NovaCRM

**Résultat final** : 
- ✅ Virtualenv Python activé
- ✅ Dependencies FastAPI/SQLAlchemy/Pytest installées
- ✅ Git repository cloné (si première fois)
- ✅ Docker lanceable (optionnel)
- ✅ Prêt pour LAB 2 (/health endpoint)

---

## Étape 1 : Vérifier WSL2 & Git

### 1.1 Vérifier WSL2 installé

```powershell
# Terminal PowerShell (Windows)
wsl --list --verbose

# Résultat attendu:
# NAME                   STATE           VERSION
# Ubuntu                 Running         2

# Si absent, installer:
# wsl --install

echo "✅ WSL2 check done"
```

### 1.2 Cloner le repository (si première fois)

```bash
# Terminal WSL2
cd /mnt/c/Perso

# Cloner (si repository remote existant)
git clone https://github.com/your-org/nova-crm.git
cd nova-crm

# Ou initialiser si local seul
cd nova-crm
git init
git add .
git commit -m "Initial commit: project structure"

# Vérifier status
git status
# Doit montrer: "On branch main, nothing to commit"

echo "✅ Git repository ready"
```

---

## Étape 2 : Setup Backend Python

### 2.1 Vérifier Python 3.10+

```bash
# Terminal WSL2
python --version

# Doit afficher:
# Python 3.10.x ou supérieur

# Si absent, installer:
# sudo apt update && sudo apt install python3.10 python3.10-venv python3-pip

python -m pip --version
# Doit voir pip 20.0+
```

### 2.2 Créer virtualenv

```bash
# Terminal WSL2
cd /mnt/c/Perso/nova-crm/backend

# Créer virtualenv
python -m venv .venv

# Activer virtualenv (WSL2/Linux)
source .venv/bin/activate

# Ou PowerShell Windows:
# .venv\Scripts\Activate.ps1

# Vérifier activation
which python
# Doit montrer: /mnt/c/Perso/nova-crm/backend/.venv/bin/python

echo "✅ Virtualenv created and activated"
```

### 2.3 Installer dependencies

```bash
# Terminal (virtualenv activé)
cd /mnt/c/Perso/nova-crm/backend

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Installer dependencies
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv pytest pytest-asyncio

# Vérifier installation
pip list | grep -E "fastapi|uvicorn|sqlalchemy"

# Output attendu:
# fastapi          0.104.1
# uvicorn          0.24.0
# sqlalchemy       2.0.23

echo "✅ Backend dependencies installed"
```

### 2.4 Créer .env pour config local

```bash
# Terminal
cd /mnt/c/Perso/nova-crm/backend

# Créer fichier .env
cat > .env << 'EOF'
# Backend Configuration
ENVIRONMENT=development
DEBUG=true

# Database
DATABASE_URL=sqlite:///./nova_crm.db
# Pour PostgreSQL later: postgresql://user:pass@localhost/nova_crm

# JWT
SECRET_KEY=dev_secret_key_change_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Engine IA
ENGINE_URL=http://localhost:8001
ENGINE_TIMEOUT=5

# Logging
LOG_LEVEL=DEBUG
EOF

# Vérifier création
cat .env
# Doit voir les variables au-dessus

echo "✅ .env file created"
```

### 2.5 Créer structure de base

```bash
# Terminal
cd /mnt/c/Perso/nova-crm/backend

# Créer dossiers (s'il n'existent pas)
mkdir -p core/domain
mkdir -p core/services
mkdir -p infrastructure/http/routes
mkdir -p infrastructure/db/migrations
mkdir -p shared
mkdir -p tests

# Créer fichiers __init__.py pour packages Python
touch core/__init__.py
touch core/domain/__init__.py
touch core/services/__init__.py
touch infrastructure/__init__.py
touch infrastructure/http/__init__.py
touch infrastructure/http/routes/__init__.py
touch infrastructure/db/__init__.py
touch shared/__init__.py
touch tests/__init__.py

# Vérifier structure
tree -L 3 -I '__pycache__|*.pyc'
# Doit montrer structure de répertoires

echo "✅ Backend structure created"
```

---

## Étape 3 : Setup Frontend (Next.js)

### 3.1 Vérifier Node.js 18+

```bash
# Terminal WSL2 (ou PowerShell pour Node installé Windows)
node --version
# Doit afficher v18.x ou supérieur

npm --version
# Doit afficher 9.x ou supérieur

# Si absent:
# curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
# sudo apt install nodejs
```

### 3.2 Installer dependencies Frontend

```bash
# Terminal WSL2
cd /mnt/c/Perso/nova-crm/frontend

# Installer dependencies
npm install

# Vérifier installation
npm list react next
# Doit voir react et next versions

# Créer .env.local pour config local
cat > .env.local << 'EOF'
# Frontend Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENV=development
EOF

echo "✅ Frontend dependencies installed"
```

---

## Étape 4 : Setup AI Engine (Python)

### 4.1 Créer virtualenv pour Engine

```bash
# Terminal WSL2
cd /mnt/c/Perso/nova-crm/ai

# Créer virtualenv
python -m venv .venv

# Activer
source .venv/bin/activate

# Installer dependencies
pip install pydantic pytest pyyaml

# Vérifier
pip list | grep -E "pydantic|pyyaml"

echo "✅ Engine virtualenv created"
```

---

## Étape 5 : Setup Taskfile (Orchestration)

### 5.1 Installer Taskfile (optionnel, pour automation)

```bash
# Terminal WSL2
# Install Taskfile CLI (https://taskfile.dev)
sh -c 'curl -sL https://taskfile.dev/install.sh | sh && sudo mv ./task /usr/local/bin/'

# Vérifier
task --version

# Si succès, vous pouvez utiliser:
# task backend    # Démarre backend
# task frontend   # Démarre frontend
# task dev        # Démarre tout en parallèle
# task test       # Run tests

echo "✅ Taskfile installed"
```

### 5.2 Créer Taskfile.yml (si absent)

```bash
# Terminal
cd /mnt/c/Perso/nova-crm

# Vérifier si Taskfile.yml existe
test -f Taskfile.yml && echo "Taskfile.yml exists" || echo "Creating Taskfile.yml"

# Créer (ou remplacer)
cat > Taskfile.yml << 'EOF'
version: '3'

tasks:
  default:
    desc: "Show available tasks"
    cmds:
      - task --list

  backend:
    desc: "Start FastAPI backend"
    cmds:
      - cd backend && source .venv/bin/activate && uvicorn infrastructure.http.main:app --reload --host 0.0.0.0 --port 8000

  frontend:
    desc: "Start Next.js frontend"
    cmds:
      - cd frontend && npm run dev

  engine:
    desc: "Start AI Engine (placeholder)"
    cmds:
      - cd ai && source .venv/bin/activate && echo "Engine would start here"

  dev:
    desc: "Start all services in parallel"
    cmds:
      - task backend &
      - task frontend &
      - wait
    ignore_error: true

  test:
    desc: "Run all tests"
    cmds:
      - cd backend && source .venv/bin/activate && pytest -v
      - cd ai && source .venv/bin/activate && pytest -v

  lint:
    desc: "Lint code"
    cmds:
      - cd backend && source .venv/bin/activate && python -m ruff check .
      - cd frontend && npm run lint

  format:
    desc: "Format code"
    cmds:
      - cd backend && source .venv/bin/activate && python -m ruff format .
      - cd frontend && npm run format
EOF

echo "✅ Taskfile.yml created"
```

---

## Étape 6 : Setup Git Hooks (optionnel, pour quality)

### 6.1 Créer pre-commit hook

```bash
# Terminal
cd /mnt/c/Perso/nova-crm

# Créer hooks directory
mkdir -p .git/hooks

# Créer pre-commit script
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash

# Pre-commit hook: run linting before commit

echo "🔍 Running lint checks..."

cd backend
source .venv/bin/activate
python -m ruff check . --select E9,F63,F7,F82 --show-source --statistics

if [ $? -ne 0 ]; then
    echo "❌ Lint failed. Fix errors before commit."
    exit 1
fi

echo "✅ Lint passed"
exit 0
EOF

# Make executable
chmod +x .git/hooks/pre-commit

echo "✅ Git hooks installed"
```

---

## Étape 7 : Validation de Setup

### 7.1 Checklist finale

```bash
# Terminal WSL2
cd /mnt/c/Perso/nova-crm

# ✅ Backend ready?
test -d backend/.venv && echo "✅ Backend virtualenv exists"
test -f backend/.env && echo "✅ Backend .env exists"
test -f backend/infrastructure/http/main.py && echo "✅ Backend main.py structure ready"

# ✅ Frontend ready?
test -d frontend/node_modules && echo "✅ Frontend dependencies installed"
test -f frontend/package.json && echo "✅ Frontend package.json exists"

# ✅ Engine ready?
test -d ai/.venv && echo "✅ Engine virtualenv exists"

# ✅ Git ready?
test -d .git && echo "✅ Git repository initialized"

# ✅ Structure ready?
test -d docs/Labs && echo "✅ Labs directory exists"
test -d docs/Cursus && echo "✅ Cursus directory exists"

echo ""
echo "🎉 SETUP COMPLETE"
```

---

## Étape 8 : Test Rapide (sanity check)

### 8.1 Test Python import

```bash
# Terminal
cd /mnt/c/Perso/nova-crm/backend
source .venv/bin/activate

# Test FastAPI import
python -c "import fastapi; print(f'FastAPI {fastapi.__version__} ready')"
# Output: FastAPI 0.104.1 ready

# Test SQLAlchemy import
python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__} ready')"
# Output: SQLAlchemy 2.0.23 ready

echo "✅ Python imports OK"
```

### 8.2 Test Node import

```bash
# Terminal WSL2
cd /mnt/c/Perso/nova-crm/frontend

# Test Next.js
npm list next
# Doit montrer version

echo "✅ Node imports OK"
```

---

## 🎯 Résumé — Vous êtes prêt quand

- ✅ WSL2 running, Git initialized
- ✅ Backend virtualenv active, FastAPI/SQLAlchemy/Pytest installed
- ✅ Backend .env created with DATABASE_URL, SECRET_KEY, etc
- ✅ Backend folder structure created (core/, infrastructure/, etc)
- ✅ Frontend node_modules installed
- ✅ AI Engine virtualenv created
- ✅ Taskfile.yml created (optionnel, mais recommandé)
- ✅ Git hooks installed (optionnel)

**Validation finale** :

```bash
# Vous pouvez crier:
echo "🎉 ENVIRONNEMENT SETUP COMPLETE"
echo "✅ Prêt pour LAB 2 : Créer /health endpoint"
```

---

## ❓ FAQ & Troubleshooting

### Q : Virtualenv pas trouvé après redémarrage terminal?
**A** : Réactivez-le : `source backend/.venv/bin/activate`

### Q : pip install échoue (permission denied)?
**A** : Utilisez `pip install --user` ou créez/activez virtualenv correctement

### Q : Node.js not found?
**A** : Installer dans WSL2 : `curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install nodejs`

### Q : Can't activate virtualenv en PowerShell Windows?
**A** : Utilisez `.venv\Scripts\Activate.ps1` au lieu de bash

### Q : Database file location?
**A** : SQLite par défaut créé dans `backend/nova_crm.db`. OK pour dev, mais PostgreSQL recommandé pour prod.

---

**Fin de LAB 1 — Setup Environment**

✅ **Vous êtes maintenant prêt pour LAB 2 : Créer le endpoint /health**
