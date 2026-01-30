# backend/infrastructure/http/dto.py

"""
DTOs (Data Transfer Objects) pour l'API HTTP.
Ce module contient les classes utilisées pour transférer les données

Pydantic effectue l validation automatique des données.

Principes Soc : éparation entre Contrat HTTP (DTO) et Logique Métier (Domain Models).

"""

from pydantic import BaseModel, Field
from typing import Optional


# ===== DTOs HEALTH CHECK =====

class HealthCheckResponse(BaseModel):
    """
    Utilisation : Contrôle rapide de santé (load balancer, monitoring).
    """
    status: str = Field(...,description="Etat du sytème (healthy/unhealthy)", example="healthy")
    timestamp: str = Field(..., description="Date/heure du contrôle (format ISO 8601)", example="2026-01-28T10:15:23:123456")
    version: str = Field(..., description="Version de l'application", example="1.0.0")

class Config:
    schema_extra = {
        "example": {
            "status": "healthy",
            "timestamp": "2026-01-28T10:15:23:123456",
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

    