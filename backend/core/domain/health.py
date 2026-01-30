# baackend/core/domain/health.py

"""
Module domaine : statut de santé du système.

Ce module contient la logique métier PURE (pas de dépendances HTTP, base de données, etc.)
Principe SoC (Séparation des préoccupations): Séparation entre logique métier et infrastructure.
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class HealthStatus:
    """
    Représente le statut de santé du système.(structure de données immuable)

    Attributes:
        status (str): Etat du système ("healthy" ou "unhealthy").
        timestamp (datetime): Date:heure du contrôle de santé.
        version (str): Version actuelle de l'application.
    """

    status: str
    timestamp: datetime
    version: str

    def is_healthy(self) -> bool:
        """
        Vérifie si le système est en bonne santé.

        Returns:
            bool: True si le statut est "healthy", sinon False.
        """
        return self.status == "healthy"
    
    def to_dict(self) -> dict:
        """
        Convertit l'objet HealthStatus en dictionnaire.

        Returns:
            dict: Représentation dictionnaire de l'objet HealthStatus.
        """
        return {
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
            "version": self.version
        }
    
# TODO JOUR 002 : Créer classe Contact dans core/domain/contact.py
# TODO JOUR 003 : Créer classe Client dans core/domain/client.py