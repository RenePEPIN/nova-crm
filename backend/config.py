"""
Configuration centralisée pour NovaCRM Backend.

Ce module charge toutes les variables d'environnement depuis .env
et les valide avec Pydantic Settings v2.

Usage:
    from config import settings
    
    database_url = settings.database_url
    debug_mode = settings.debug
"""

from typing import List, Literal, Any
from pydantic import Field, field_validator  # type: ignore
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class Settings(BaseSettings):
    """
    Configuration application utilisant Pydantic Settings v2.
    
    Les variables sont chargées automatiquement depuis :
    1. Fichier .env (priorité haute)
    2. Variables d'environnement système
    3. Valeurs par défaut définies ici
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # ===================================================================
    # 🐍 ENVIRONNEMENT PYTHON
    # ===================================================================
    python_version: str = Field(default="3.12.7", description="Version Python requise")
    pythonpath: str = Field(default="/home/renep/dev/nova-crm/backend", description="PYTHONPATH")
    
    # ===================================================================
    # 🌍 ENVIRONNEMENT APPLICATION
    # ===================================================================
    environment: Literal["development", "staging", "production", "testing"] = Field(
        default="development",
        description="Environnement d'exécution"
    )
    debug: bool = Field(default=True, description="Mode debug (désactiver en production)")
    
    # ===================================================================
    # 🖥️ SERVEUR & RÉSEAU
    # ===================================================================
    host: str = Field(default="0.0.0.0", description="Host du serveur")
    port: int = Field(default=8000, ge=1, le=65535, description="Port du serveur")
    reload: bool = Field(default=True, description="Auto-reload (dev only)")
    workers: int = Field(default=1, ge=1, description="Nombre de workers Uvicorn")
    
    # ===================================================================
    # 📊 BASE DE DONNÉES
    # ===================================================================
    database_url: str = Field(
        default="sqlite:///./nova_crm.db",
        description="URL de connexion base de données"
    )
    database_pool_size: int = Field(default=5, ge=1, description="Taille pool connexions")
    database_max_overflow: int = Field(default=10, ge=0, description="Connexions overflow max")
    database_echo: bool = Field(default=False, description="Logger requêtes SQL")
    
    # ===================================================================
    # 🔐 SÉCURITÉ & AUTHENTIFICATION
    # ===================================================================
    secret_key: str = Field(
        default="dev-secret-key-change-me-in-production",
        min_length=32,
        description="Clé secrète JWT (CHANGER EN PRODUCTION)"
    )
    algorithm: str = Field(default="HS256", description="Algorithme JWT")
    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        description="Durée validité access token (minutes)"
    )
    refresh_token_expire_days: int = Field(
        default=7,
        ge=1,
        description="Durée validité refresh token (jours)"
    )
    
    # ===================================================================
    # 🌐 CORS
    # ===================================================================
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Origines CORS autorisées"
    )
    cors_allow_credentials: bool = Field(default=True, description="Autoriser credentials CORS")
    cors_allow_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        description="Méthodes HTTP autorisées"
    )
    cors_allow_headers: List[str] = Field(default=["*"], description="Headers autorisés")
    
    # ===================================================================
    # 🤖 AI COMPLIANCE ENGINE
    # ===================================================================
    ai_engine_url: str = Field(
        default="http://localhost:8001",
        description="URL du moteur IA"
    )
    ai_engine_path: str = Field(default="../ai", description="Chemin vers le moteur IA")
    ai_engine_timeout: int = Field(default=30, ge=1, description="Timeout appels IA (secondes)")
    enable_ai_engine: bool = Field(default=True, description="Activer moteur IA")
    
    # Détection PII
    enable_pii_detection: bool = Field(default=True, description="Activer détection PII")
    pii_mask_char: str = Field(default="*", max_length=1, description="Caractère masquage PII")
    pii_detection_patterns: List[str] = Field(
        default=["email", "phone", "ssn", "credit_card", "iban"],
        description="Types PII à détecter"
    )
    
    # Détection secrets
    enable_secret_detection: bool = Field(default=True, description="Activer détection secrets")
    secret_detection_patterns: List[str] = Field(
        default=["api_key", "token", "password", "secret"],
        description="Types secrets à détecter"
    )
    
    # Audit trail
    enable_audit_trail: bool = Field(default=True, description="Activer audit trail")
    audit_log_path: str = Field(default="./logs/audit", description="Chemin logs audit")
    audit_retention_days: int = Field(default=90, ge=1, description="Rétention logs (jours)")
    
    # ===================================================================
    # ⚖️ CONFORMITÉ & RÉGLEMENTATION
    # ===================================================================
    # RGPD
    gdpr_enabled: bool = Field(default=True, description="Activer conformité RGPD")
    gdpr_data_retention_days: int = Field(
        default=365,
        ge=1,
        description="Durée rétention données (jours)"
    )
    gdpr_right_to_erasure: bool = Field(default=True, description="Droit à l'effacement")
    
    # IA Act
    ia_act_enabled: bool = Field(default=True, description="Activer conformité IA Act")
    ia_act_risk_level: Literal["unacceptable", "high", "limited", "minimal"] = Field(
        default="limited",
        description="Niveau de risque IA Act"
    )
    
    # ISO 27001
    iso27001_enabled: bool = Field(default=False, description="Activer conformité ISO 27001")
    
    # ===================================================================
    # 📝 LOGGING
    # ===================================================================
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Niveau de logging"
    )
    log_format: Literal["json", "text"] = Field(default="json", description="Format logs")
    log_path: str = Field(default="./logs", description="Chemin logs")
    log_file_max_bytes: int = Field(
        default=10485760,
        ge=1024,
        description="Taille max fichier log (bytes)"
    )
    log_file_backup_count: int = Field(default=5, ge=0, description="Nombre backups logs")
    log_to_console: bool = Field(default=True, description="Logger vers console")
    log_to_file: bool = Field(default=True, description="Logger vers fichier")
    
    # ===================================================================
    # 🧪 TESTING
    # ===================================================================
    test_database_url: str = Field(
        default="sqlite:///./test_nova_crm.db",
        description="URL base de données test"
    )
    test_log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="WARNING",
        description="Niveau logging tests"
    )
    
    # ===================================================================
    # 🚀 PERFORMANCE
    # ===================================================================
    enable_cache: bool = Field(default=False, description="Activer cache Redis")
    redis_url: str = Field(default="redis://localhost:6379/0", description="URL Redis")
    cache_ttl: int = Field(default=300, ge=1, description="TTL cache (secondes)")
    
    enable_rate_limiting: bool = Field(default=False, description="Activer rate limiting")
    rate_limit_per_minute: int = Field(default=60, ge=1, description="Requêtes max/minute")
    
    # ===================================================================
    # 🔧 DÉVELOPPEMENT
    # ===================================================================
    enable_swagger: bool = Field(default=True, description="Activer Swagger UI")
    enable_redoc: bool = Field(default=True, description="Activer ReDoc")
    enable_openapi: bool = Field(default=True, description="Activer OpenAPI schema")
    api_docs_url: str = Field(default="/docs", description="URL Swagger")
    api_redoc_url: str = Field(default="/redoc", description="URL ReDoc")
    
    # ===================================================================
    # 📚 METADATA
    # ===================================================================
    app_name: str = Field(default="NovaCRM", description="Nom application")
    app_version: str = Field(default="0.1.0", description="Version application")
    app_description: str = Field(
        default="CRM moderne avec moteur IA de conformité",
        description="Description application"
    )
    api_prefix: str = Field(default="/api/v1", description="Préfixe API")
    contact_email: str = Field(default="admin@novacrm.local", description="Email contact")
    
    # ===================================================================
    # 🔍 VALIDATEURS CUSTOM
    # ===================================================================
    
    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, v: str, info: Any) -> str:
        """Valide que la clé secrète n'est pas celle par défaut en production."""
        environment = info.data.get("environment", "development")
        
        if environment == "production" and "dev-secret-key" in v:
            raise ValueError(
                "⚠️ SECRET_KEY par défaut détectée en production ! "
                "Générer une vraie clé avec : python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        
        if len(v) < 32:
            raise ValueError("SECRET_KEY doit contenir au moins 32 caractères")
        
        return v
    
    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str, info: Any) -> str:
        """Recommandation PostgreSQL en production."""
        environment = info.data.get("environment", "development")
        
        if environment == "production" and v.startswith("sqlite"):
            print(
                "⚠️ WARNING : SQLite détecté en production. "
                "Recommandé d'utiliser PostgreSQL pour la production."
            )
        
        return v
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> List[str]:
        """Parse CORS origins depuis string JSON ou liste."""
        if isinstance(v, str):
            import json
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return parsed
                return [str(parsed)]
            except json.JSONDecodeError:
                # Si c'est une simple string, retourner comme liste
                return [v]
        if isinstance(v, list):
            return v
        return [str(v)]
    
    # ===================================================================
    # 🔧 MÉTHODES UTILITAIRES
    # ===================================================================
    
    @property
    def is_development(self) -> bool:
        """Retourne True si environnement development."""
        return self.environment == "development"
    
    @property
    def is_production(self) -> bool:
        """Retourne True si environnement production."""
        return self.environment == "production"
    
    @property
    def is_testing(self) -> bool:
        """Retourne True si environnement test."""
        return self.environment == "testing"
    
    def get_database_url(self, for_alembic: bool = False) -> str:
        """
        Retourne l'URL de base de données.
        
        Args:
            for_alembic: Si True, adapte l'URL pour Alembic migrations
            
        Returns:
            URL base de données formatée
        """
        url = self.database_url
        
        # Alembic ne supporte pas postgresql+asyncpg, convertir en postgresql
        if for_alembic and "postgresql+asyncpg" in url:
            url = url.replace("postgresql+asyncpg", "postgresql")
        
        return url
    
    def display_config(self) -> None:
        """Affiche la configuration (masque les secrets)."""
        print("\n" + "=" * 70)
        print(f"🚀 {self.app_name} - Configuration")
        print("=" * 70)
        print(f"Environment    : {self.environment}")
        print(f"Debug Mode     : {self.debug}")
        print(f"Host:Port      : {self.host}:{self.port}")
        print(f"Database       : {self.database_url.split('@')[0] if '@' in self.database_url else self.database_url}")
        print(f"AI Engine      : {'Enabled' if self.enable_ai_engine else 'Disabled'}")
        print(f"PII Detection  : {'Enabled' if self.enable_pii_detection else 'Disabled'}")
        print(f"GDPR Compliance: {'Enabled' if self.gdpr_enabled else 'Disabled'}")
        print(f"IA Act         : {'Enabled' if self.ia_act_enabled else 'Disabled'} (Risk: {self.ia_act_risk_level})")
        print(f"Log Level      : {self.log_level}")
        print(f"Swagger UI     : {self.api_docs_url if self.enable_swagger else 'Disabled'}")
        print("=" * 70 + "\n")


# ===================================================================
# 🎯 INSTANCE GLOBALE
# ===================================================================

# Instance unique chargée au démarrage
settings = Settings()


# ===================================================================
# 🧪 FONCTION DE TEST
# ===================================================================

if __name__ == "__main__":
    """Test de chargement de la configuration."""
    print("🔍 Test de chargement de la configuration...\n")
    
    try:
        # Afficher configuration
        settings.display_config()
        
        # Tests basiques
        print("✅ Tests de validation :")
        print(f"   - Python version : {settings.python_version}")
        print(f"   - Environment    : {settings.environment}")
        print(f"   - Is Development : {settings.is_development}")
        print(f"   - Is Production  : {settings.is_production}")
        print(f"   - Database URL   : {settings.get_database_url()}")
        print(f"   - API Prefix     : {settings.api_prefix}")
        print(f"   - CORS Origins   : {settings.cors_origins}")
        
        print("\n✅ Configuration chargée avec succès !")
        
    except Exception as e:
        print(f"\n❌ Erreur lors du chargement : {e}")
        raise
