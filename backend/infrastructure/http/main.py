# `backend/infrastructure/http/main.py

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
from infrastructure.http.routes.health_route import router as health_router

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