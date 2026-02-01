#!/bin/bash
# Script de démarrage du backend FastAPI NovaCRM

cd "$(dirname "$0")"

# Activer l'environnement virtuel
source .venv/bin/activate

# Définir PYTHONPATH
export PYTHONPATH=/home/renep/dev/nova-crm/backend

# Lancer le serveur
echo "🚀 Démarrage du backend NovaCRM..."
python infrastructure/http/main.py
