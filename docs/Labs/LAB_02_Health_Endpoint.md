# 🧪 LAB 2 — Créer Endpoint /health + Tests

**Durée estimée** : 2-3 heures  
**Prérequis** : LAB 1 (environment setup)  
**Objectif** : Créer premier endpoint FastAPI avec tests unitaires + validation

**Résultat final** :
- ✅ FastAPI server qui démarre (`uvicorn`)
- ✅ GET `/health` endpoint qui retourne JSON
- ✅ Unit tests pour l'endpoint
- ✅ Swagger docs accessible (`/docs`)
- ✅ Prêt pour LAB 3 (compliance engine)

---

## Étape 1 : Créer structure FastAPI

### 1.1 Créer main.py (FastAPI app)

**Fichier** : `backend/infrastructure/http/main.py`

```python
"""
NovaCRM Backend - FastAPI Application

Main entry point pour API REST.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from datetime import datetime

# ===== STARTUP / SHUTDOWN =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events.
    
    Startup: Log, initialize DB connections, etc.
    Shutdown: Close connections, cleanup resources.
    """
    # Startup
    print("=" * 60)
    print("🚀 NovaCRM Backend Starting...")
    print(f"   Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"   Debug: {os.getenv('DEBUG', 'true')}")
    print(f"   Time: {datetime.utcnow().isoformat()}")
    print("=" * 60)
    yield
    # Shutdown
    print("=" * 60)
    print("🛑 NovaCRM Backend Shutting Down...")
    print("=" * 60)

# ===== CREATE APP =====

app = FastAPI(
    title="NovaCRM API",
    description="Customer Relationship Management + AI Compliance Hub",
    version="0.1.0",
    lifespan=lifespan
)

# ===== MIDDLEWARE : CORS =====

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MIDDLEWARE : REQUEST LOGGING (optional) =====

from fastapi import Request
import time
import logging

logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log HTTP requests and responses.
    
    Logs:
    - Method + path
    - Query params
    - Response status + duration
    """
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    logger.info(
        f"{request.method} {request.url.path} → {response.status_code} ({duration:.3f}s)"
    )
    
    return response

# ===== INCLUDE ROUTES =====

# Import routers (créés dans les étapes suivantes)
from infrastructure.http.routes import health
# from infrastructure.http.routes import contacts

app.include_router(health.router)
# app.include_router(contacts.router)

# ===== ROOT ENDPOINT =====

@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns: API info
    """
    return {
        "message": "Welcome to NovaCRM API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

# ===== EXCEPTION HANDLERS =====

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions (400, 404, 500, etc)."""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "path": str(request.url.path)
    }

# ===== RUN =====

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload on file change
    )

# Usage: uvicorn infrastructure.http.main:app --reload --port 8000
```

---

### 1.2 Créer routes/health.py (health endpoint)

**Fichier** : `backend/infrastructure/http/routes/health.py`

```python
"""
Health check routes.

Endpoints:
- GET /health : Simple status check
- GET /health/detailed : Detailed status (DB, Engine, etc)
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/health",
    tags=["health", "monitoring"]
)

# ===== SIMPLE HEALTH CHECK =====

@router.get("/", response_model=Dict[str, Any])
async def health_check() -> Dict[str, Any]:
    """
    Simple health check endpoint.
    
    Purpose: Monitor if backend is alive and responding.
    Use case: Kubernetes liveness probe, load balancer health checks.
    
    Returns:
        status: "ok" if healthy
        timestamp: Server timestamp (ISO 8601)
        version: API version
        service: Service name
    
    Example response:
        {
            "status": "ok",
            "timestamp": "2026-01-28T10:15:23.123456",
            "version": "0.1.0",
            "service": "NovaCRM Backend"
        }
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0",
        "service": "NovaCRM Backend"
    }

# ===== DETAILED HEALTH CHECK =====

async def check_database() -> Dict[str, Any]:
    """
    Check if database is healthy.
    
    TODO: Actually connect to DB and run query
    For now, return mock data.
    """
    try:
        # TODO: await db.execute("SELECT 1")
        return {
            "status": "ok",
            "type": "SQLite",
            "location": "nova_crm.db"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

async def check_engine() -> Dict[str, Any]:
    """
    Check if AI Engine is accessible.
    
    TODO: Actually call engine health endpoint
    For now, return mock data.
    """
    try:
        # TODO: await engine_adapter.health()
        return {
            "status": "ok",
            "type": "Python Engine",
            "url": "http://localhost:8001"
        }
    except Exception as e:
        logger.error(f"Engine health check failed: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/detailed", response_model=Dict[str, Any])
async def health_detailed() -> Dict[str, Any]:
    """
    Detailed health check endpoint.
    
    Purpose: Monitor all system components (backend, DB, Engine, etc).
    Use case: Monitoring dashboards, debugging startup issues.
    
    Returns:
        status: "ok" if all healthy, "degraded" if some failing
        backend: Health of this service
        database: Health of database connection
        engine: Health of AI Engine connection
        timestamp: Server timestamp
    
    Example response:
        {
            "status": "ok",
            "backend": {"status": "ok"},
            "database": {"status": "ok", "type": "SQLite"},
            "engine": {"status": "ok", "type": "Python Engine"},
            "timestamp": "2026-01-28T10:15:23.123456"
        }
    """
    # Check all components
    db_status = await check_database()
    engine_status = await check_engine()
    
    # Determine overall status
    overall_status = "ok"
    if db_status.get("status") == "error" or engine_status.get("status") == "error":
        overall_status = "degraded"
    
    return {
        "status": overall_status,
        "backend": {
            "status": "ok",
            "service": "NovaCRM Backend",
            "version": "0.1.0"
        },
        "database": db_status,
        "engine": engine_status,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/ready", response_model=Dict[str, Any])
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check endpoint.
    
    Purpose: Check if service is ready to accept traffic.
    Use case: Kubernetes readiness probe (direct traffic only if returns 200).
    
    Returns 200 only if all components ready.
    Returns 503 if any component not ready.
    """
    db_status = await check_database()
    engine_status = await check_engine()
    
    if db_status.get("status") != "ok" or engine_status.get("status") != "ok":
        raise HTTPException(
            status_code=503,
            detail="Service not ready (DB or Engine unavailable)"
        )
    
    return {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

### 1.3 Créer routes/__init__.py

**Fichier** : `backend/infrastructure/http/routes/__init__.py`

```python
"""
HTTP routes package.

Makes routes/ a Python package so FastAPI can import routers.
"""
```

---

## Étape 2 : Créer Tests

### 2.1 Créer tests/test_health.py

**Fichier** : `backend/tests/test_health.py`

```python
"""
Unit tests for health check endpoints.

Test framework: pytest
Run with: pytest tests/test_health.py -v
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime

# Import the app
from infrastructure.http.main import app

# Create test client
client = TestClient(app)

# ===== TESTS : GET /health =====

class TestHealthCheck:
    """Test suite for simple health check."""
    
    def test_health_check_returns_200(self):
        """Test that /health returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_response_schema(self):
        """Test that /health returns correct schema."""
        response = client.get("/health")
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "service" in data
        
        # Check field types
        assert isinstance(data["status"], str)
        assert isinstance(data["timestamp"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["service"], str)
    
    def test_health_check_status_ok(self):
        """Test that /health returns status=ok."""
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "ok"
    
    def test_health_check_timestamp_valid_iso(self):
        """Test that timestamp is valid ISO 8601."""
        response = client.get("/health")
        data = response.json()
        
        # Try to parse timestamp
        try:
            datetime.fromisoformat(data["timestamp"].replace('Z', '+00:00'))
            assert True
        except ValueError:
            assert False, f"Invalid ISO timestamp: {data['timestamp']}"
    
    def test_health_check_version_format(self):
        """Test that version is semantic versioning."""
        response = client.get("/health")
        data = response.json()
        
        # Should be like "0.1.0"
        parts = data["version"].split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

# ===== TESTS : GET /health/detailed =====

class TestHealthDetailed:
    """Test suite for detailed health check."""
    
    def test_health_detailed_returns_200(self):
        """Test that /health/detailed returns 200 OK."""
        response = client.get("/health/detailed")
        assert response.status_code == 200
    
    def test_health_detailed_response_schema(self):
        """Test that /health/detailed returns correct schema."""
        response = client.get("/health/detailed")
        data = response.json()
        
        # Check required fields
        assert "status" in data
        assert "backend" in data
        assert "database" in data
        assert "engine" in data
        assert "timestamp" in data
    
    def test_health_detailed_backend_status(self):
        """Test that backend status is ok."""
        response = client.get("/health/detailed")
        data = response.json()
        
        assert data["backend"]["status"] == "ok"
        assert "service" in data["backend"]
        assert "version" in data["backend"]
    
    def test_health_detailed_db_status_present(self):
        """Test that database status is present."""
        response = client.get("/health/detailed")
        data = response.json()
        
        assert "status" in data["database"]
        # Status should be "ok" or "error"
        assert data["database"]["status"] in ["ok", "error"]

# ===== TESTS : GET /health/ready =====

class TestHealthReady:
    """Test suite for readiness check."""
    
    def test_health_ready_returns_200_when_ready(self):
        """Test that /health/ready returns 200 when ready."""
        # In mock, everything is "ok"
        response = client.get("/health/ready")
        assert response.status_code == 200
    
    def test_health_ready_response_schema(self):
        """Test that /health/ready returns correct schema."""
        response = client.get("/health/ready")
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "ready"
        assert "timestamp" in data

# ===== TESTS : GET / (root) =====

class TestRoot:
    """Test suite for root endpoint."""
    
    def test_root_returns_200(self):
        """Test that / returns 200 OK."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_response_has_message(self):
        """Test that / returns welcome message."""
        response = client.get("/")
        data = response.json()
        
        assert "message" in data
        assert "Welcome" in data["message"]

# ===== PERFORMANCE TESTS =====

class TestHealthPerformance:
    """Test that endpoints respond quickly."""
    
    def test_health_check_fast(self):
        """Test that /health responds within 100ms."""
        import time
        
        start = time.time()
        response = client.get("/health")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 0.1  # 100ms
        print(f"✅ /health responded in {duration*1000:.2f}ms")
    
    def test_health_detailed_reasonable(self):
        """Test that /health/detailed responds within 500ms."""
        import time
        
        start = time.time()
        response = client.get("/health/detailed")
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 0.5  # 500ms
        print(f"✅ /health/detailed responded in {duration*1000:.2f}ms")

# ===== INTEGRATION TESTS =====

class TestHealthIntegration:
    """Test that health endpoints integrate correctly."""
    
    def test_sequential_requests(self):
        """Test that multiple requests work sequentially."""
        # Request 1
        r1 = client.get("/health")
        assert r1.status_code == 200
        
        # Request 2
        r2 = client.get("/health/detailed")
        assert r2.status_code == 200
        
        # Request 3
        r3 = client.get("/health/ready")
        assert r3.status_code == 200
    
    def test_concurrent_requests(self):
        """
        Test that multiple concurrent requests work (simulated).
        Real concurrency test would need async test client.
        """
        responses = [
            client.get("/health"),
            client.get("/health/detailed"),
            client.get("/health/ready"),
        ]
        
        assert all(r.status_code == 200 for r in responses)

# ===== RUN TESTS =====

if __name__ == "__main__":
    # Run with pytest
    # pytest tests/test_health.py -v
    pytest.main([__file__, "-v"])
```

---

## Étape 3 : Démarrer et Tester

### 3.1 Démarrer FastAPI server

```bash
# Terminal WSL2
cd /home/renep/dev/nova-crm/backend

# Activer virtualenv (si pas déjà fait)
source .venv/bin/activate

# Démarrer server
uvicorn infrastructure.http.main:app --reload --host 0.0.0.0 --port 8000

# Output:
# INFO:     Uvicorn running on http://0.0.0.0:8000
# INFO:     Application startup complete
# ========================================================
# 🚀 NovaCRM Backend Starting...
#    Environment: development
#    Debug: true
#    Time: 2026-01-28T10:15:23.123456
# ========================================================
```

### 3.2 Tester les endpoints avec curl

```bash
# Terminal (nouvelle window)

# ===== Test /health =====
echo "=== Testing /health ==="
curl -i http://localhost:8000/health

# Response:
# HTTP/1.1 200 OK
# {
#   "status": "ok",
#   "timestamp": "2026-01-28T10:15:23.123456",
#   "version": "0.1.0",
#   "service": "NovaCRM Backend"
# }

# ===== Test /health/detailed =====
echo "=== Testing /health/detailed ==="
curl http://localhost:8000/health/detailed | python -m json.tool

# Response:
# {
#   "status": "ok",
#   "backend": {
#     "status": "ok",
#     "service": "NovaCRM Backend",
#     "version": "0.1.0"
#   },
#   "database": {
#     "status": "ok",
#     "type": "SQLite",
#     "location": "nova_crm.db"
#   },
#   "engine": {
#     "status": "ok",
#     "type": "Python Engine",
#     "url": "http://localhost:8001"
#   },
#   "timestamp": "2026-01-28T10:15:23.123456"
# }

# ===== Test /health/ready =====
echo "=== Testing /health/ready ==="
curl http://localhost:8000/health/ready | python -m json.tool

# ===== Test / (root) =====
echo "=== Testing / (root) ==="
curl http://localhost:8000/ | python -m json.tool
```

### 3.3 Accéder à Swagger UI

```bash
# Ouvrir browser
http://localhost:8000/docs

# Vous verrez:
# - Swagger UI interactive API docs
# - List tous les endpoints (/health, /health/detailed, etc)
# - Bouton "Try it out" pour chaque endpoint
# - Auto-génération des paramètres
```

### 3.4 Accéder à ReDoc (alternative docs)

```bash
# Browser
http://localhost:8000/redoc

# Documentation alternative avec meilleure organisation
```

---

## Étape 4 : Lancer les Tests

### 4.1 Exécuter tests unitaires

```bash
# Terminal
cd /home/renep/dev/nova-crm/backend

# Activer virtualenv
source .venv/bin/activate

# Lancer pytest
pytest tests/test_health.py -v

# Output:
# ====== test session starts ======
# collected 15 items
#
# tests/test_health.py::TestHealthCheck::test_health_check_returns_200 PASSED [ 6%]
# tests/test_health.py::TestHealthCheck::test_health_check_response_schema PASSED [ 13%]
# tests/test_health.py::TestHealthCheck::test_health_check_status_ok PASSED [ 20%]
# tests/test_health.py::TestHealthCheck::test_health_check_timestamp_valid_iso PASSED [ 26%]
# tests/test_health.py::TestHealthCheck::test_health_check_version_format PASSED [ 33%]
# tests/test_health.py::TestHealthDetailed::test_health_detailed_returns_200 PASSED [ 40%]
# ... (more tests)
#
# ====== 15 passed in 0.45s ======
# ✅ All tests passed!
```

### 4.2 Exécuter avec couverture (optionnel)

```bash
# Terminal
pip install coverage

# Lancer tests avec couverture
pytest tests/test_health.py --cov=infrastructure.http.routes.health

# Output:
# Name                                           Stmts   Miss  Cover
# ================================================================
# infrastructure/http/routes/health.py             50      2    96%
# ================================================================
# TOTAL                                            50      2    96%
```

---

## Étape 5 : Validation Finale

### 5.1 Checklist

```bash
# ✅ FastAPI server démarre sans erreur
curl http://localhost:8000/health | grep -q "ok" && echo "✅ Server runs"

# ✅ /health endpoint retourne 200 + correct schema
curl -s http://localhost:8000/health | grep -q '"status":"ok"' && echo "✅ /health endpoint works"

# ✅ /health/detailed retourne status complets
curl -s http://localhost:8000/health/detailed | grep -q '"database"' && echo "✅ /health/detailed works"

# ✅ Swagger docs accessible
curl -s http://localhost:8000/docs | grep -q "swagger" && echo "✅ Swagger docs accessible"

# ✅ All tests pass
cd backend && source .venv/bin/activate && pytest tests/test_health.py -q && echo "✅ All tests pass"

echo ""
echo "🎉 LAB 2 COMPLETE"
```

---

## 🚀 Résumé

**Vous avez créé** :
- ✅ FastAPI main app (infrastructure/http/main.py)
- ✅ Health routes (infrastructure/http/routes/health.py)
- ✅ 15+ unit tests (tests/test_health.py)
- ✅ Swagger docs auto-generated (/docs)

**Endpoints maintenant disponibles** :
- `GET /` : Root endpoint
- `GET /health` : Simple health check
- `GET /health/detailed` : Detailed status
- `GET /health/ready` : Readiness probe (K8s)

**Skills acquis** :
- ✅ Créer endpoint FastAPI async
- ✅ Structured response via return dict
- ✅ Écrire tests pytest
- ✅ Router pattern (grouping endpoints)
- ✅ Middleware (CORS, logging)
- ✅ Exception handling

---

## ➡️ Prochaines Étapes

**LAB 3** : Intégrer l'AI Engine + audit trail immuable
- Créer endpoint `/api/v1/contacts`
- Appeler Engine pour compliance check
- Masquer PII avant stockage
- Logger audit trail

---

**Fin de LAB 2 — Endpoint /health + Tests**

✅ **Vous êtes maintenant prêt pour LAB 3 : Compliance Engine Integration**
