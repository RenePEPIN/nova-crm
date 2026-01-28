# 📘 **ADR‑03 — Stack Technique Figée (FastAPI / Next.js / Engine Python)**

*Status : Accepted*  
*Date : 2026‑01‑27*  
*Auteur : René / NovaCRM Core Team*  
*Relates to : ADR‑01 (Architecture Globale), ADR‑02 (Choix FastAPI)*

***

## 1. 🎯 Contexte

Le projet NovaCRM + AI Compliance Hub repose sur une architecture modulaire composée :

*   d’un **backend FastAPI** pour l’API CRM, l’authentification et l’orchestration métier,
*   d’un **moteur IA autonome** écrit en Python (policies, scanners, audit),
*   d’un **frontend Next.js** pour le dashboard et l’interface utilisateur.

Dans le cadre de la gouvernance technique et pour respecter les contraintes internes (notamment les politiques IT d’entreprise), nous devons **figer la stack technique**, sans mentionner de versions, et définir les technologies officiellement approuvées pour toute l’équipe.

Cet ADR fixe définitivement les choix technologiques, leurs rôles, leurs contraintes et leurs périmètres, afin d’offrir une base stable et durable.

***

## 2. 💡 Décision

Nous adoptons la **stack technique suivante**, figée et stable, utilisée dans l’ensemble du projet :

### **Backend (API CRM)**

*   Langage : **Python**
*   Framework : **FastAPI**
*   Serveur : **Uvicorn**
*   ORM : **SQLAlchemy**
*   Migrations : **Alembic**
*   Validation : **Pydantic**
*   Tests : **Pytest**
*   Qualité : **Ruff**, **Black**, **Mypy**

### **Frontend (Dashboard & UI)**

*   Framework : **Next.js**
*   Langage : **TypeScript**
*   Style : **Tailwind CSS**
*   Linting / Format : **ESLint**, **Prettier**

### **Compliance Engine (Moteur IA)**

*   Langage : **Python**
*   Patterns : **Strategy**, **Factory**, **Adapter**, **Decorator**, **Observer (futur)**
*   Structure : `ai/detectors/`, `ai/pipelines/`, `ai/policies/`, `ai/exporters/`

### **Orchestration & Dev**

*   Outil principal : **Taskfile** (Task)
*   Shell de dev : **WSL2 Ubuntu**
*   Éditeur recommandé : **VS Code** (extensions Python, Pylance, ESLint, Prettier)

### **Base de données**

*   Dev : **SQLite**
*   Production : **PostgreSQL**

### **Conteneurisation & Infra (futur)**

*   Conteneur : **Docker**
*   Orchestration : **Kubernetes** (optionnel, futur)
*   Observabilité : logs JSON + endpoints santé + OpenTelemetry (futur)

Cette stack constitue la **référence stable** du projet.  
Toute divergence doit passer par un ADR dédié.

***

## 3. 🧭 Options Envisagées

### A — Stack Django monolithique

❌ Pas adaptée à l’architecture modulaire  
❌ Couplage trop fort avec ORM / Apps Django  
❌ Peu compatible avec un moteur IA indépendant  
❌ Sur‑ingénierie pour un API-first moderne

### B — Stack Node.js full‑stack (Express ou Nest)

❌ Manque de maturité pour un moteur IA Python  
❌ Perte du langage unique pour l’Engine (Python)  
❌ Nest trop structurant pour un MVP modulaire

### ✔ C — FastAPI (Backend) + Python Engine + Next.js (Front)

✔ API-first moderne  
✔ Python natif pour l’IA  
✔ Modulaire, évolutif, simple  
✔ Typage fort (Pydantic + TS)  
✔ Supporte une architecture service-based  
✔ Déploiement léger (ASGI + Uvicorn)

***

## 4. 🔍 Justification

1.  **Alignement architecture (ADR‑01)**  
    Cette stack correspond parfaitement au triptyque :  
    **API propre → Engine IA isolé → UI moderne**.

2.  **Cohérence linguistique**  
    L’essentiel du métier et du moteur IA doit rester en **Python**,  
    langage optimum pour l’analyse, la sécurité et les règles.

3.  **Séparation des responsabilités (SoC)**  
    Next.js s’occupe uniquement de la présentation.  
    FastAPI expose uniquement l’API.  
    Le moteur IA opère indépendamment comme un *service logique*.

4.  **Performance & Async**  
    FastAPI + Uvicorn sont optimisés pour du trafic API et logique événementielle.

5.  **Scalabilité future**  
    La stack peut facilement évoluer vers un découpage par services :  
    Backend → Service API  
    Engine → Service IA  
    Front → WebApp statique ou hybride SSR.

6.  **Facilité DevOps**  
    Docker + ASGI + Next.js → pipeline simple, images petites, démarrage rapide.

7.  **Conformité entreprise**  
    Stack simple, stable, non exotique, facile à auditer.

***

## 5. ⚠️ Risques & Mitigations

### R1 — Absence d’un admin natif comme Django

*Mitigation :* développer un module Admin dans le frontend ou un outil interne low‑code.

### R2 — ORM à composer manuellement

*Mitigation :* conventions strictes dans le backend (`services/`, `repositories/`, `schemas/`).

### R3 — Multiplicité des outils Python

*Mitigation :* Taskfile + README détaillé + structure figée.

### R4 — Stack front moderne (Next.js) non maîtrisée par tous

*Mitigation :* créer des services API centralisés, architecture claire.

***

## 6. 🧱 Impacts

### Positifs

*   Architecture claire et durable
*   Onboarding rapide
*   Tests simples (backend / engine / frontend isolés)
*   API documentée automatiquement
*   Compatibilité totale avec patterns IA

### Négatifs

*   Plus de choix techniques initiaux (à cadrer par conventions)
*   Pas d’outil admin clé en main
*   Nécessité de maîtriser deux technologies (Python + TS)

***

## 7. 🔗 Conséquences

*   Toute fonctionnalité future doit respecter cette **stack figée**.
*   Aucun changement de framework ne sera envisagé sans **ADR formel**.
*   Les modules doivent s’intégrer correctement dans les dossiers existants.
*   Le code doit rester compatible **Taskfile**.

***

## 8. 📎 Liens

*   ADR‑01 — Architecture globale
*   ADR‑02 — Choix FastAPI
*   Stack figée — `/docs/architecture/stack.md`
*   AI Rules — `/AI-RULES.md`
*   README du projet

***

