# 🧱 Stack Technique NovaCRM + AI Compliance Hub

Ce document décrit la **stack technique figée** du projet NovaCRM + AI Compliance Hub :

- les **modules** principaux (frontend, backend, AI, infra),
- les **technologies choisies** et leurs rôles,
- les **diagrammes d’architecture** (vues haut niveau),
- les **objectifs** techniques et non-fonctionnels,
- les **règles d’utilisation par module** (ce qui est autorisé / interdit).

---

## 🔭 Vue d’Ensemble

NovaCRM est organisé en **quatre grands blocs** :

1. **Frontend** : interface utilisateur (Next.js + TypeScript)
2. **Backend API** : API métier CRM (FastAPI)
3. **AI Compliance Engine** : moteur de détection de risques IA
4. **Infra & Tooling** : CI/CD, observabilité, IaC (Kubernetes, Terraform, Taskfile)

### 📊 Diagramme global (Vue Logique)

```text
                       Utilisateurs (Sales, Ops, Compliance, Direction)
                                        │
                                        ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                             FRONTEND (Next.js)                           │
│  - Dashboard CRM                                                         │
│  - Vue Compliance IA                                                     │
│  - Visualisation logs & risques                                         │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │ HTTP/JSON (REST)
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         BACKEND API (FastAPI)                            │
│  - Auth / RBAC                                                          │
│  - Domain CRM (organisations, contacts, interactions)                   │
│  - Gestion des policies IA                                              │
│  - Orchestration appels vers AI Compliance Engine                       │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │ HTTP interne / Message Bus (futur)     
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                     AI COMPLIANCE ENGINE (Python)                        │
│  - Détecteurs de risques (PII, secrets, ton, etc.)                      │
│  - Moteur de règles (policies)                                          │
│  - Classification IA Act                                                │
│  - Audit trail / export                                                 │
└───────────────────────────────┬──────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                             INFRASTRUCTURE                               │
│  - Base de données (PostgreSQL)                                         │
│  - Message broker (futur)                                               │
│  - Kubernetes / Terraform                                               │
│  - Monitoring, logs, métriques                                         │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🧩 Modules & Technologies

### 1️⃣ Frontend — Next.js + TypeScript

**Objectifs :**

- Offrir un **dashboard CRM moderne** et fluide
- Donner une **vue temps réel de la conformité IA** (risques, alertes, audit)
- Rester **complètement découplé** du backend (API-only)

**Stack :**

- **Framework** : Next.js (app router)
- **Langage** : TypeScript
- **UI** : React, Tailwind CSS
- **Data fetching** : React Query / fetch API
- **Auth** : JWT / cookies (via API backend)

**Diagramme (Vue module frontend)**

```text
/frontend
├── app/                 # Pages & routes
├── components/          # Composants UI mutualisés
├── lib/                 # Helpers (API client, utils)
├── hooks/               # Hooks personnalisés
└── styles/              # Thèmes & styles Tailwind
```

**Règles d’utilisation :**

- ❌ **Interdit** d’appeler directement la base de données ou l’AI Compliance Engine.
- ✅ **Obligatoire** de passer par les **endpoints REST** exposés par le backend.
- ✅ Gestion de la logique métier **côté backend**, jamais dans les composants UI.
- ✅ Toute nouvelle route doit être documentée (description fonctionnelle + besoin métier).

---

### 2️⃣ Backend API — FastAPI

**Objectifs :**

- Servir d’**unique point d’entrée backend** pour le frontend
- Encapsuler la **logique métier CRM** et les règles de sécurité
- Orchestrer les appels vers l’**AI Compliance Engine**
- Offrir une **API REST versionnée, typée, documentée**

**Stack :**

- **Framework** : FastAPI
- **Validation / schémas** : Pydantic
- **ORM** : SQLAlchemy (ou équivalent)
- **DB** : PostgreSQL
- **Auth** : JWT, RBAC (rôles, permissions)

**Diagramme (Vue backend)**

```text
/backend
├── core/                     # Domain & use cases
│   ├── domain/               # Entités métier (CRM, IA)
│   └── services/             # Services applicatifs
├── infrastructure/
│   ├── http/                 # Routers FastAPI, DTO
│   ├── db/                   # Modèles SQLAlchemy, sessions
│   └── integrations/         # Adapters externes (AI, mail, etc.)
└── api/main.py               # Entrée FastAPI
```

**Règles d’utilisation :**

- ✅ Le **domaine** (core/domain) ne doit **jamais dépendre** d’un framework.
- ✅ Toute nouvelle fonctionnalité doit être exposée via un **use case** clair.
- ❌ Interdit de mettre de la **logique métier** dans les routers HTTP (infrastructure/http).
- ✅ Les appels vers l’AI Compliance Engine passent par une **interface dédiée** (adapter).
- ✅ Validation systématique des entrées/sorties via Pydantic.

---

### 3️⃣ AI Compliance Engine — Python

**Objectifs :**

- Fournir un **moteur d’analyse des prompts et données**
- Centraliser la **détection de risques IA** (PII, secrets, conformité IA Act)
- Offrir un **moteur de règles** configurable par l’équipe conformité
- Délivrer un **audit trail complet** pour chaque usage IA

**Stack :**

- **Langage** : Python
- **Librairies possibles** :
  - Regex / NLP pour détection PII
  - Intégration avec LLMs (OpenAI, etc.) pour analyse avancée
- **Pattern** : Pipelines d’analyse + règles déclaratives

**Diagramme (Vue AI Engine)**

```text
/ai
├── detectors/             # "Capteurs" de risques
│   ├── pii_detector.py    # Emails, téléphone, adresses…
│   ├── secret_detector.py # Keys, tokens, secrets
│   ├── risk_classifier.py # Score global de risque
│   └── sentiment.py       # Tonalité & toxicité (futur)
├── pipelines/             # Orchestration des détecteurs
│   └── compliance_pipeline.py
├── policies/              # Règles métier & IA Act
│   ├── policy_engine.py
│   └── rules/             # Fichiers YAML/JSON de règles
└── exporters/             # Export vers SIEM / logs externes
    └── audit_exporter.py
```

**Règles d’utilisation :**

- ✅ Le moteur IA est **indépendant** du CRM : pas d’accès direct aux tables métier.
- ✅ Communication uniquement via **API / messages** depuis le backend.
- ❌ Interdit d’ajouter de la **logique CRM** dans le moteur IA.
- ✅ Toute nouvelle règle IA doit être :
  - documentée (description, risques couverts),
  - versionnée (changement de règles traçable),
  - testée (unit tests minimum).

---

### 4️⃣ Infra, CI/CD & Observabilité

**Objectifs :**

- Standardiser les **environnements de déploiement** (dev, staging, prod)
- Garantir la **reproductibilité** (IaC)
- Offrir **logs, métriques, traces** pour l’ensemble de la plateforme

**Stack :**

- **IaC** : Terraform
- **Orchestration** : Kubernetes (manifests sous /infra/k8s)
- **CI/CD** : GitHub Actions / autre (à préciser)
- **Monitoring** : Prometheus / Grafana (cible), logs centralisés

**Diagramme (Vue infra simplifiée)**

```text
/infra
├── terraform/           # Provisionnement cloud (réseaux, clusters, DB)
├── k8s/                 # Manifests déploiements, services, ingress
└── scripts/             # Scripts d’automatisation (migrations, backups)
```

**Règles d’utilisation :**

- ✅ Tout changement d’infra passe par **merge request** + revue.
- ✅ Pas de création manuelle de ressources en prod (uniquement via Terraform).
- ✅ Les services exposent des **probes** (liveness/readiness).
- ✅ Les logs applicatifs sont **structurés** (JSON) et centralisés.

---

## 🎯 Objectifs Techniques Globaux

1. **API-first** : tout est consommable via API documentée (OpenAPI).
2. **Séparation des responsabilités (SoC)** : frontend, backend, IA, infra bien isolés.
3. **Extensibilité** : ajout de nouveaux modules IA, de nouvelles features CRM sans refonte.
4. **Scalabilité** : chaque bloc peut être scalé indépendamment (pods K8s séparés).
5. **Testabilité** : tests unitaires et d’intégration ciblés par module.
6. **Conformité** : architecture prête pour IA Act, RGPD, ISO 27001.

---

## 📏 Règles Transverses

- ✅ **DRY** : pas de duplication de logique entre backend et AI Engine.
- ✅ **KISS** : pas de sur-ingénierie ; commencer simple, complexifier selon besoin.
- ✅ **YAGNI** : pas de micro-services précipités ; l’architecture est préparée, mais on n’extrait que si la charge / le besoin métier le justifie.
- ✅ **Sécurité by design** : validation des entrées partout, secrets gérés via vault, principe du moindre privilège.
- ✅ **Observabilité by default** : chaque nouveau service doit loguer ce qu’il fait et exposer des métriques clés.

---

## 📚 Liens & Références

- [docs/adr/ADR_01.md](../adr/ADR_01.md) — Architecture globale (si présent)
- [README](../../README) — Présentation haute-niveau du projet
- [infra/](../../infra) — Détails sur l’infrastructure & déploiement

Ce document sert de **référence figée** : tout changement majeur de stack doit faire l’objet :

1. d’une **nouvelle ADR** justifiant la décision,
2. d’une **mise à jour de cette page** si la stack évolue réellement.
