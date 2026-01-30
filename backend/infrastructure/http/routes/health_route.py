# backend/infrastructure/http/routes/health_route.py

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