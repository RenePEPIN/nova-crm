# 0. Vision & Axes directeurs

**Sommaire de la section**:
- [0.1. Ce que couvre le plan d’action](#01-ce-que-couvre-le-plan-daction)
> **Roadmap validée à 95%** — les **5% restants** viendront de l’**expérience terrain**.

## 0.1. Ce que couvre le plan d’action
- **Robustesse** : Architecture (S.O.L.I.D., Clean/Hexagonal), Tests (Unit/Int/E2E, contrat, charge), Performance (profiling back/front), Sécurité (OWASP, headers, AuthN/Z).
- **Visibilité** : Observabilité (logs structurés, metrics, traces **OpenTelemetry**), **SLI/SLO** & alerting, **post-mortems** actionnables, **documentation vivante** (README, wiki, ADR).
- **Avenir** : **IA (RAG/LLM)** pragmatique, **Edge & CDN** (SWR/ISR, cache HTTP), **Green IT** (code splitting, images multi-stage, coûts/FinOps, perf CPU/mémoire).

_👉 Cette section formalise ta synthèse « Robustesse / Visibilité / Avenir » et sert d’introduction exécutive à la checklist._

---


# Sommaire

- [0. Vision & Axes directeurs](#0-vision-axes-directeurs)
  - [0.1. Ce que couvre le plan d’action](#01-ce-que-couvre-le-plan-daction)
- [Sommaire](#sommaire)
- [1. Architecture & Conception](#1-architecture-conception)
  - [1.1. Principes fondamentaux](#11-principes-fondamentaux)
  - [1.2. Styles d’architecture](#12-styles-darchitecture)
  - [1.3. Pratiques d’implémentation](#13-pratiques-dimplémentation)
- [2. Backend (Python/Django & Web)](#2-backend-pythondjango-web)
  - [2.1. Python avancé](#21-python-avancé)
  - [2.2. Django](#22-django)
  - [2.3. Web & API](#23-web-api)
- [3. Frontend (React / Next.js / TypeScript)](#3-frontend-react-nextjs-typescript)
  - [3.1. JavaScript & TypeScript](#31-javascript-typescript)
  - [3.2. React – fondamentaux](#32-react-fondamentaux)
  - [3.3. Next.js – rendu & data](#33-nextjs-rendu-data)
  - [3.4. UI/UX & accessibilité](#34-uiux-accessibilité)
  - [3.5. Mobile (optionnel)](#35-mobile-optionnel)
- [4. Bases de données & Données](#4-bases-de-données-données)
  - [4.1. SQL (PostgreSQL recommandé)](#41-sql-postgresql-recommandé)
  - [4.2. NoSQL & cache](#42-nosql-cache)
  - [4.3. Gouvernance & conformité](#43-gouvernance-conformité)
- [5. DevOps & Cloud](#5-devops-cloud)
  - [5.1. Contrôle de version & qualité locale](#51-contrôle-de-version-qualité-locale)
  - [5.2. Conteneurs & déploiement](#52-conteneurs-déploiement)
  - [5.3. CI/CD & IaC](#53-cicd-iac)
  - [5.4. Cloud public (un provider au choix)](#54-cloud-public-un-provider-au-choix)
- [6. Qualité & Tests](#6-qualité-tests)
  - [6.1. Stratégie de test](#61-stratégie-de-test)
  - [6.2. Types de tests complémentaires](#62-types-de-tests-complémentaires)
- [7. Observabilité & Fiabilité (SRE)](#7-observabilité-fiabilité-sre)
  - [7.1. Télémetrie unifiée](#71-télémetrie-unifiée)
  - [7.2. Opérations](#72-opérations)
- [8. Sécurité](#8-sécurité)
  - [8.1. Application](#81-application)
  - [8.2. Supply-chain & déploiement](#82-supply-chain-déploiement)
  - [8.3. Conformité](#83-conformité)
- [9. Architecture d’intégration & Messaging](#9-architecture-dintégration-messaging)
  - [9.1. Intégration](#91-intégration)
  - [9.2. Messaging & événements](#92-messaging-événements)
- [10. IA & LLM (pragmatisme 2026)](#10-ia-llm-pragmatisme-2026)
  - [10.1. Intégration produit](#101-intégration-produit)
  - [10.2. Pipelines](#102-pipelines)
- [11. Soft Skills & Méthodes](#11-soft-skills-méthodes)
  - [11.1. Méthode & collaboration](#111-méthode-collaboration)
  - [11.2. Leadership individuel](#112-leadership-individuel)
- [12. Roadmap d’acquisition (suggestion)](#12-roadmap-dacquisition-suggestion)
  - [12.1. Phase 0 — Fondations (4–6 semaines)](#121-phase-0-fondations-46-semaines)
  - [12.2. Phase 1 — Productionisation (6–8 semaines)](#122-phase-1-productionisation-68-semaines)
  - [12.3. Phase 2 — Scale & sécurité (6–8 semaines)](#123-phase-2-scale-sécurité-68-semaines)
  - [12.4. Phase 3 — Différenciants 2026 (4–6 semaines)](#124-phase-3-différenciants-2026-46-semaines)
- [13. Checklist rapide “Job-ready 2026”](#13-checklist-rapide-job-ready-2026)

# 1. Architecture & Conception

**Sommaire de la section**:
- [1.1. Principes fondamentaux](#11-principes-fondamentaux)
- [1.2. Styles d’architecture](#12-styles-darchitecture)
- [1.3. Pratiques d’implémentation](#13-pratiques-dimplémentation)
> **Objectif** : concevoir des systèmes maintenables, testables et évolutifs.

## 1.1. Principes fondamentaux
- **[Must]** S.O.L.I.D.
- **[Must]** Séparation des responsabilités (SoC)
- **[Must]** KISS / YAGNI
- **[Important]** DRY (en gardant du contexte)
- **[Important]** Design Patterns (GoF) utiles web (Factory, Strategy, Adapter, Observer, Decorator)

## 1.2. Styles d’architecture
- **[Important]** Architecture hexagonale (Ports & Adapters)
- **[Important]** Clean Architecture
- **[Important]** Domain-Driven Design (DDD) — stratégies de découpage (Bounded Contexts, Ubiquitous Language)

## 1.3. Pratiques d’implémentation
- **[Must]** Inversion de dépendances (DI) et injection
- **[Important]** ADR (Architectural Decision Records)
- **[Bonus]** CQRS (selon contexte)
- **[Bonus]** Event Sourcing (contexte très spécifique)

---

# 2. Backend (Python/Django & Web)

**Sommaire de la section**:
- [2.1. Python avancé](#21-python-avancé)
- [2.2. Django](#22-django)
- [2.3. Web & API](#23-web-api)
## 2.1. Python avancé
- **[Must]** Typage statique et type hinting (mypy, Protocols)
- **[Must]** Exceptions & erreurs custom
- **[Important]** Décorateurs, context managers
- **[Important]** Itérateurs & générateurs
- **[Important]** Packaging (pyproject.toml, wheels)
- **[Important]** Async/await (asyncio) pour IO intensif
- **[Important]** Profiling & optimisation (CPU/Mémoire)

## 2.2. Django
- **[Must]** MVT, cycle requête/réponse
- **[Must]** ORM (requêtes complexes, F-expressions)
- **[Must]** Optimisation (select_related, prefetch_related)
- **[Must]** Auth personnalisée (AbstractUser)
- **[Important]** Migrations avancées (data migrations, rollbacks)
- **[Important]** DRF (Serializers, ViewSets, throttling, versioning)
- **[Must]** Cache (Redis / Memcached)
- **[Important]** Middlewares & Signals (usage parcimonieux)

## 2.3. Web & API
- **[Must]** RESTful API design (pagination, tri, filtrage, idempotence)
- **[Must]** Authentification & Autorisation (OAuth2, JWT)
- **[Important]** GraphQL (selon besoins) ; gRPC pour interne
- **[Important]** WebSockets / SSE (temps réel)

---

# 3. Frontend (React / Next.js / TypeScript)

**Sommaire de la section**:
- [3.1. JavaScript & TypeScript](#31-javascript-typescript)
- [3.2. React – fondamentaux](#32-react-fondamentaux)
- [3.3. Next.js – rendu & data](#33-nextjs-rendu-data)
- [3.4. UI/UX & accessibilité](#34-uiux-accessibilité)
- [3.5. Mobile (optionnel)](#35-mobile-optionnel)
## 3.1. JavaScript & TypeScript
- **[Must]** Closures, portée, event loop, microtasks
- **[Must]** Promises, async/await, gestion d’erreurs
- **[Must]** ES Modules, destructuring, spread/rest
- **[Must]** TypeScript : interfaces/types, generics, unions/intersections
- **[Important]** TS : mapped/conditional/utility types, type guards
- **[Important]** tsconfig avancé, @types

## 3.2. React – fondamentaux
- **[Must]** Hooks de base (useState, useEffect, useContext)
- **[Important]** Hooks avancés (useMemo, useCallback, useId)
- **[Important]** Custom hooks & composition
- **[Important]** Portals & Error Boundaries
- **[Must]** Optimisation de rendu (React.memo, useMemo, useCallback)
- **[Important]** Concurrent features : Suspense & transitions

## 3.3. Next.js – rendu & data
- **[Important]** Server vs Client Components
- **[Important]** Server Actions & mutations
- **[Important]** Data fetching côté client (SWR/TanStack Query)
- **[Important]** Hydratation & sérialisation
- **[Bonus]** Routing SPA (React Router) si pas sur Next.js

## 3.4. UI/UX & accessibilité
- **[Must]** Responsive design (mobile-first)
- **[Important]** Design system & tokens (couleurs, espaces, typographies)
- **[Important]** Tailwind CSS (utility-first) ou équivalent
- **[Must]** Accessibilité (WCAG) & navigation clavier
- **[Important]** Skeletons, loading patterns, optimistic updates
- **[Bonus]** Animations & micro-interactions (Framer Motion)
- **[Bonus]** PWA, offline-first (Service Workers)

## 3.5. Mobile (optionnel)
- **[Important]** React Native : New Architecture (JSI/Fabric)
- **[Important]** Navigation (React Navigation), gestures/animations (Reanimated)
- **[Important]** Accès APIs natives (caméra, GPS), stockage (MMKV/SQLite)
- **[Important]** OTA (CodePush), Expo vs Bare, déploiements (Xcode/Gradle/Fastlane)

---

# 4. Bases de données & Données

**Sommaire de la section**:
- [4.1. SQL (PostgreSQL recommandé)](#41-sql-postgresql-recommandé)
- [4.2. NoSQL & cache](#42-nosql-cache)
- [4.3. Gouvernance & conformité](#43-gouvernance-conformité)
## 4.1. SQL (PostgreSQL recommandé)
- **[Must]** Modélisation, normalisation
- **[Must]** Index (B-Tree, composés, partiels), EXPLAIN/ANALYZE
- **[Must]** Transactions, niveaux d’isolation, verrous
- **[Important]** Partitionnement, réplication de base
- **[Important]** Sauvegarde/restore, PITR

## 4.2. NoSQL & cache
- **[Important]** Redis (cache, rate limiting, queues)
- **[Bonus]** MongoDB (documents) selon use case
- **[Bonus]** Time-series (TimescaleDB) selon besoins

## 4.3. Gouvernance & conformité
- **[Must]** RGPD : bases (minimisation, DPO, DPIA, droits des personnes)
- **[Important]** Chiffrement au repos/en transit, rotation des clés

---

# 5. DevOps & Cloud

**Sommaire de la section**:
- [5.1. Contrôle de version & qualité locale](#51-contrôle-de-version-qualité-locale)
- [5.2. Conteneurs & déploiement](#52-conteneurs-déploiement)
- [5.3. CI/CD & IaC](#53-cicd-iac)
- [5.4. Cloud public (un provider au choix)](#54-cloud-public-un-provider-au-choix)
## 5.1. Contrôle de version & qualité locale
- **[Must]** Git avancé (rebase, cherry-pick, bisect)
- **[Important]** Trunk-Based vs Git Flow (choix argumenté)
- **[Must]** Lint/format (Ruff, Black, Pre-commit)

## 5.2. Conteneurs & déploiement
- **[Must]** Docker (images minces, multi-stage, healthchecks)
- **[Important]** Docker Compose (dev/test)
- **[Important]** Kubernetes (notions, déploiement basique) selon taille d’orga

## 5.3. CI/CD & IaC
- **[Must]** CI/CD (pipelines, tests, build, release)
- **[Important]** Infrastructure as Code (Terraform, Ansible)
- **[Important]** Gestion des secrets (Vault, Secret Manager, .env sécurisé)

## 5.4. Cloud public (un provider au choix)
- **[Important]** IAM, VPC/réseau, compute (containers, serverless), stockage objet
- **[Important]** Monitoring natif, registres d’images, coûts (FinOps basique)

---

# 6. Qualité & Tests

**Sommaire de la section**:
- [6.1. Stratégie de test](#61-stratégie-de-test)
- [6.2. Types de tests complémentaires](#62-types-de-tests-complémentaires)
## 6.1. Stratégie de test
- **[Must]** Tests unitaires, d’intégration, end-to-end
- **[Important]** AAA (Arrange, Act, Assert)
- **[Important]** Mocking, stubbing, faking
- **[Important]** Couverture (sans fétichisme des %)
- **[Important]** TDD (selon culture d’équipe)

## 6.2. Types de tests complémentaires
- **[Important]** Tests de contrat (Pact)
- **[Important]** Tests de charge & perf (k6, Locust)
- **[Bonus]** Chaos testing (basique)
- **[Must]** Code reviews (donner/recevoir)

---

# 7. Observabilité & Fiabilité (SRE)

**Sommaire de la section**:
- [7.1. Télémetrie unifiée](#71-télémetrie-unifiée)
- [7.2. Opérations](#72-opérations)
## 7.1. Télémetrie unifiée
- **[Must]** Logs structurés (correlation IDs)
- **[Must]** Metrics (techniques & business)
- **[Important]** Traces distribuées (OpenTelemetry)

## 7.2. Opérations
- **[Important]** SLI/SLO, error budgets
- **[Important]** Alerting (réduction du bruit), dashboards
- **[Important]** Runbooks & post-mortems actionnables

---

# 8. Sécurité

**Sommaire de la section**:
- [8.1. Application](#81-application)
- [8.2. Supply-chain & déploiement](#82-supply-chain-déploiement)
- [8.3. Conformité](#83-conformité)
## 8.1. Application
- **[Must]** OWASP Top 10, validation côté serveur & client
- **[Must]** Headers de sécurité (CSP, HSTS), rate limiting, bruteforce protection
- **[Important]** Threat modeling (STRIDE)

## 8.2. Supply-chain & déploiement
- **[Important]** SBOM (CycloneDX), scanners de dépendances (Dependabot/Renovate)
- **[Important]** SAST/DAST en CI
- **[Important]** Signature d’images (Sigstore/Cosign), policy admission
- **[Important]** Rotation de secrets, gestion des clés

## 8.3. Conformité
- **[Important]** Notions ISO 27001 / SOC 2, journalisation & rétention

---

# 9. Architecture d’intégration & Messaging

**Sommaire de la section**:
- [9.1. Intégration](#91-intégration)
- [9.2. Messaging & événements](#92-messaging-événements)
## 9.1. Intégration
- **[Important]** Versioning d’API, compatibilité, dépréciation
- **[Important]** Idempotence, pagination, ETags, cache HTTP
- **[Important]** CDN, edge caching, stale-while-revalidate

## 9.2. Messaging & événements
- **[Important]** Kafka / RabbitMQ (pub/sub, work queues)
- **[Important]** Patterns : circuit breaker, retry/backoff, bulkheads
- **[Bonus]** Event-driven (outbox, transactionnelle)

---

# 10. IA & LLM (pragmatisme 2026)

**Sommaire de la section**:
- [10.1. Intégration produit](#101-intégration-produit)
- [10.2. Pipelines](#102-pipelines)
## 10.1. Intégration produit
- **[Important]** RAG (embeddings, vector DB : pgvector/Weaviate)
- **[Important]** Évaluation & observabilité LLM (traces/prompts)
- **[Important]** Guardrails & sécurité de prompt
- **[Important]** Maîtrise coût/latence, stratégie de cache

## 10.2. Pipelines
- **[Bonus]** Orchestration (LangChain/LlamaIndex) — garder léger et mesuré

---

# 11. Soft Skills & Méthodes

**Sommaire de la section**:
- [11.1. Méthode & collaboration](#111-méthode-collaboration)
- [11.2. Leadership individuel](#112-leadership-individuel)
## 11.1. Méthode & collaboration
- **[Must]** Agilité (Scrum/Kanban), gestion du backlog
- **[Must]** Documentation vivante (README, wiki), ADR
- **[Important]** Estimation (story points, T-shirt sizing)
- **[Important]** Gestion de la dette technique
- **[Important]** SemVer, Conventional Commits
- **[Bonus]** Pair/Mob programming

## 11.2. Leadership individuel
- **[Important]** Communication claire (écrite/orale)
- **[Important]** Mentorat/feedback, négociation produit
- **[Important]** Gestion d’incidents (on-call)

---

# 12. Roadmap d’acquisition (suggestion)

**Sommaire de la section**:
- [12.1. Phase 0 — Fondations (4–6 semaines)](#121-phase-0-fondations-46-semaines)
- [12.2. Phase 1 — Productionisation (6–8 semaines)](#122-phase-1-productionisation-68-semaines)
- [12.3. Phase 2 — Scale & sécurité (6–8 semaines)](#123-phase-2-scale-sécurité-68-semaines)
- [12.4. Phase 3 — Différenciants 2026 (4–6 semaines)](#124-phase-3-différenciants-2026-46-semaines)
## 12.1. Phase 0 — Fondations (4–6 semaines)
- Git avancé, CI/CD, Docker
- JS/TS fondamentaux, React hooks, Next.js (rendu & data)
- Python avancé, Django ORM/DRF/caching
- Tests unitaires/intégration, OWASP, RGPD de base

## 12.2. Phase 1 — Productionisation (6–8 semaines)
- Observabilité (logs/metrics/traces), OpenTelemetry
- DB avancée (index, EXPLAIN, transactions), migrations maîtrisées
- Perf front (CWV, code splitting) & back (profiling)
- Accessibilité AA, i18n

## 12.3. Phase 2 — Scale & sécurité (6–8 semaines)
- IaC (Terraform), secrets, supply-chain (SBOM, SAST)
- Messaging (Kafka/RabbitMQ), patterns (circuit breaker, cache-aside)
- Cloud (IAM, réseau, stockage), FinOps basique

## 12.4. Phase 3 — Différenciants 2026 (4–6 semaines)
- LLM/RAG (vecteurs, observabilité LLM, évaluation)
- gRPC/GraphQL (selon besoin), PWA/offline (pertinent), mobile RN (si ciblé)

---

# 13. Checklist rapide “Job-ready 2026”

- **Frontend Must** : React + TS (hooks, perf, accessibilité), Next.js (rendu & data), CWV
- **Backend Must** : Python avancé, Django ORM/DRF/caching, REST, AuthN/Z, OWASP, RGPD
- **Data Must** : Postgres (index, EXPLAIN, transactions), sauvegarde/restore
- **DevOps Must** : Git avancé, Docker, CI/CD, secrets, IaC basique
- **Observabilité Must** : logs/metrics/traces (OpenTelemetry), SLI/SLO
- **Tests Must** : Unit/Int/E2E, contrat, charge (k6/Locust)
- **Sécurité Important** : SBOM, SAST/DAST, signature images, rotation secrets
- **Différenciants 2026** : Messaging (Kafka/RabbitMQ), GraphQL/gRPC, LLM/RAG