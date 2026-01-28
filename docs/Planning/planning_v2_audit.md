# 📅 Planning NovaCRM v2 (POST-AUDIT) — 6 mois

**Statut** : Planning RÉVISÉ suite audit de cohérence (voir rapport audit 2026-01-28)
**Audience** : Team, Product, Stakeholders
**Dates** : 02 Février 2026 → 17 Juillet 2026

---

## 🔴 CHEMIN CRITIQUE (3 étapes « go/no-go »)

Ces 3 étapes déterminent le succès du projet. **Aucun compromis autorisé** :

### 1️⃣ **Sprint 2 : Audit Trail Immuable**
- **Pourquoi ?** C'est la fondation conformité IA Act. Sans trace immuable, pas de v1.0.
- **Success Criteria** : Audit append-only fonctionnelle, PII masquée avant stockage, tests 100%.
- **Risk** : Découvrir trop tard qu'audit est cassée = refactorisation massive.
- **Mitigation** : Review architecte jour 1, pas d'exceptions ad-hoc, tests immuabilité.

### 2️⃣ **Sprint 5-6 : Auth & RBAC Robustes**
- **Pourquoi ?** JWT/RBAC = socle sécurité. Une faille auth = incident grave, perte confiance.
- **Success Criteria** : JWT issuance/verification 100% testée, RBAC guards sur tous endpoints, external security review OK.
- **Risk** : Auth faible découverte en prod = catastrophe légale.
- **Mitigation** : External expert review (pas review interne), test RBAC exhaustifs, token security hardened.

### 3️⃣ **Sprint 11 : DPIA & Hardening Sécurité**
- **Pourquoi ?** IA Act exige DPIA. Redaction PII = preuve conformité. Sans cela, pas de v1.0.
- **Success Criteria** : DPIA document complété, redaction PII 100% couverture, security checklist validée, playbook deployement OK.
- **Risk** : Déployer sans DPIA = non-conformité légale.
- **Mitigation** : Template DPIA pré-rempli, security expert validation, pentest léger interne.

**Dépendances critiques** :
```
Sprint 1  →  Sprint 2 (audit)  →  Sprints 3-4 (CRM)  →  Sprints 5-6 (auth/RBAC)  →  Sprint 7-8 (E2E)  →  Sprint 11 (DPIA)  →  Sprint 12 (release)
```

---

## 🗺️ Macro-timeline

| Mois                          | Objectif principal                                            | Jalons                                                        |
| ----------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| **Fév 2026 (Sprints 1–2)**    | **MVP technique** : structure, endpoints de base, 1 règle IA  | ADR-00/01 + README, `/health`, Rule `no_pii`, Audit v1, UI skeleton |
| **Mars 2026 (Sprints 3–4)**   | **MVP fonctionnel** : CRUD 1 entité, 3 rules IA, YAML policies| CRUD Contacts, Rules (PII/mass-export/secrets), Policy loader |
| **Avr 2026 (Sprints 5–6)**    | **Sécurité & Compliance** : Auth, RBAC, Audit complet, masking| JWT/OAuth2, RBAC 4 rôles, Audit JSON export, redaction PII   |
| **Mai 2026 (Sprints 7–8)**    | **Qualité & Observabilité** : E2E, logs JSON, couverture 75%+ | Structured logging, E2E flows, 75-80% test coverage, AIrules  |
| **Juin 2026 (Sprints 9–10)**  | **Scalabilité & Persistance** : Engine adapter, PostgreSQL    | Adapter REST PoC, PostgreSQL migration, Redis Queue PoC        |
| **Juil 2026 (Sprints 11–12)** | **Hardening & Release v1.0** : DPIA, playbook, démo interne   | DPIA doc, playbook déploiement, revue sécu, tag v1.0-ready    |

---

## 📌 Détail par sprint (2 semaines) — VERSION AUDITÉE

> **DoD commun** : lint & format OK, tests unitaires OK, endpoints stables documentés (OpenAPI), ADR mis à jour si décision structurante.
> 
> **POST-AUDIT** : Sprints 3-6 decomposés pour réalisme. Chemin critique = Sprint 2 (audit) → Sprint 5-6 (auth/RBAC) → Sprint 11 (hardening).

### ✅ Sprint 1 (02–13 Fév) — Fondation & Architecture

**Objectif** : Socle technique API + structure modules + ADRs fondamentaux.

*   **Backend** :
    *   Router `GET /api/v1/health` + structuration (`infrastructure/http/`, `core/domain/`, `core/services/`)
    *   Schémas Pydantic v1 (DTO minimaux)
*   **Engine** :
    *   Squelette `Engine.analyze()` → retourne `{risk, findings, action}`
    *   Préparation Rule interface (Strategy pattern)
*   **Frontend** :
    *   Setup Next.js + `lib/api.ts` + page Dashboard (placeholder)
*   **Docs** :
    *   **ADR‑00** (système ADR) + **ADR‑01** (architecture globale)
    *   **README** (enrichi avec vision + stack)
*   **Livrables** : `/health` OK, `task install` + `task dev` OK
*   **DoD** : lint/format OK, stub tests, architecture stable
*   **Durée estimée** : 10j (débutant avec mentorat)

### ✅ Sprint 2 (16–27 Fév) — Compliance Engine Core & Audit (🔴 CRITIQUE)

**Objectif** : Premier moteur IA opérationnel + journalisation immuable (CHEMIN CRITIQUE).

*   **Engine (priorité 1)** :
    *   **Rule `no_pii_in_prompts`** (détection emails/téléphone via regex)
    *   Audit append-only (fichier) + masquage PII avant stockage
    *   Tests unitaires règle (100% couverture)
*   **Backend** :
    *   `POST /api/v1/compliance/check` (contrat stable)
    *   Logger JSON minimal avec `requestId` + `auditId`
*   **Frontend** :
    *   Component **ComplianceBanner** (affiche risk/action)
*   **Docs** :
    *   **ADR‑02** (FastAPI), **ADR‑03** (stack technique)
*   **Livrables** : Rule 1 opérationnelle, audit immuable, E2E `/compliance/check`
*   **DoD** : PII detection 95%+ accurate, audit append-only testée, lint 100%
*   **Durée estimée** : 10j (ENGINE = priorité absolue)
*   **🔴 ALERT** : Ne pas sauter l'audit immuable = fondation conformité

### ✅ Sprint 3 (02–13 Mar) — CRUD CRM Entities (Contacts)

**Objectif** : Première entité CRM métier (Contacts seulement, pas Clients).

*   **Backend (CRM)** :
    *   CRUD Contacts : `GET`, `POST`, `PUT`, `DELETE` + SQLite
    *   Repository pattern + Pydantic schemas
    *   Tests CRUD (repository + endpoint)
*   **Engine** :
    *   **Rule `no_mass_export_requests`** (détection mots-clés : "tous", "export", "complet")
*   **Frontend** :
    *   Page List Contacts (simple table) + Create (form)
*   **DoD** : OpenAPI stable, CRUD 100% couverture, Engine rule 2 opérationnelle
*   **Durée estimée** : 10j
*   **Note** : Reporter Clients → Sprint 4 pour éviter surcharge

### ✅ Sprint 4 (16–27 Mar) — CRUD CRM (Clients) & Policy Engine

**Objectif** : Deuxième entité + règles déclaratives (YAML).

*   **Backend** :
    *   CRUD Clients (identique à Contacts)
    *   Adapter Engine (interface stable pour règles)
*   **Engine** :
    *   **Rule `no_secrets_in_prompts`** (tokens, keys, passwords via regex)
    *   **YAML policy loader** : charger `ai/policies/policy_set.yaml`
    *   Factory pattern pour instancier règles
*   **Frontend** :
    *   Pages Edit Clients/Contacts
    *   Vue Compliance basique (afficher findings + risk)
*   **DoD** : YAML parser OK, Factory pattern stable, 3 rules opérationnelles
*   **Durée estimée** : 10j

### ✅ Sprint 5 (30 Mar–10 Avr) — Auth & JWT (🔴 CRITIQUE)

**Objectif** : Authentification robuste = prérequis sécurité v1.0.

*   **Sécurité** :
    *   **JWT** : issuer token, verify token, refresh logic
    *   **OAuth2 scaffold** : préparation intégration MS/Google (pas implémenté)
    *   Middleware CORS + rate limiting basique
*   **Backend** :
    *   Endpoint `POST /api/v1/auth/login` + `POST /refresh`
    *   Tests auth (token validation, expiry)
*   **Frontend** :
    *   Page Connexion + token storage (localStorage → httpOnly later)
    *   Guard route (redirect non-auth)
*   **DoD** : JWT génération/vérification 100% testée, CORS OK, no secret en clair
*   **Durée estimée** : 10j
*   **🔴 ALERT** : External security review recommandée avant merge

### ✅ Sprint 6 (13–24 Avr) — RBAC & Audit Details (🔴 CRITIQUE)

**Objectif** : Contrôle d'accès granulaire + audit traçable complet.

*   **Sécurité** :
    *   **RBAC** : 4 rôles (admin/manager/analyst/viewer)
    *   Guards par rôle (endpoint `/api/v1/admin/*` → admin only)
*   **Engine** :
    *   **Decorator instrumentation** : timings, counters pour perf
    *   **`redact_outputs`** : masquage PII en output (post-completion)
*   **Backend** :
    *   Endpoint `GET /api/v1/compliance/audit/:id` (retrieve single audit)
    *   Audit export JSON (structure complète avec redaction)
*   **Frontend** :
    *   Page Audit détaillée (findings, redactions visibles)
    *   Affichage conditionnel par rôle (analyst ne voit pas admin panel)
*   **DoD** : RBAC guards 100% couverture, audit export testée, masking PII 100%
*   **Durée estimée** : 10j
*   **🔴 ALERT** : Ne pas sauter PII redaction = fondation conformité IA Act

### ✅ Sprint 7 (27 Avr–08 Mai) — Observabilité & E2E Tests

**Objectif** : Logs structurés + tests intégration complets.

*   **Observabilité** :
    *   Logs JSON uniformes (API + Engine) : champs `requestId`, `auditId`, `actor`, `timestamp`
    *   Setup pour futurs SIEM (Splunk/ELK)
*   **Tests** :
    *   E2E auth → compliance check → audit export (happy path + error cases)
    *   Bench scan (latence engine < 200ms dev, < 500ms stress)
*   **Frontend** :
    *   Improve tables (pagination, filtres par risk/rule)
*   **DoD** : E2E pass, logs JSON parsables, latence < 500ms
*   **Durée estimée** : 10j

### ✅ Sprint 8 (11–22 Mai) — Qualité & Finalization Documentation

**Objectif** : Couverture tests 75-80% + politiques documentées.

*   **Qualité** :
    *   Durcir lint : Ruff 100% + Black format (backend)
    *   ESLint + Prettier 100% (frontend)
    *   Tests intégration : compliance + CRUD + auth flows
*   **Docs** :
    *   **AIrules.md** finalisé (politiques, exemples, incident playbook)
    *   Procédures incident (false positive handling)
*   **DoD** : 75-80% test coverage, lint 100%, AIrules complete
*   **Durée estimée** : 10j

### ✅ Sprint 9 (25 Mai–05 Juin) — Scalabilité Option & Architecture

**Objectif** : Préparer séparation Engine en service (PoC).

*   **Backend** :
    *   **Adapter réseau** : interface Engine via REST interne (préparation)
    *   Feature flag `COMPLIANCE_MODE=local|service` (pas activé yet)
*   **Engine** :
    *   Simple HTTP interface : `POST /analyze` (PoC)
*   **DB** :
    *   PostgreSQL schémas (copie SQLite, structuré pour prod)
*   **DoD** : Adapter REST PoC working, PostgreSQL schema valid
*   **Durée estimée** : 10j
*   **Note** : Pas d'activation service full (YAGNI) tant que load ne l'exige

### ✅ Sprint 10 (08–19 Juin) — Database Migration & Async

**Objectif** : Persistance prod-ready + background jobs.

*   **Backend** :
    *   Alembic migrations (SQLite → PostgreSQL)
    *   Deploy Postgres locally (compose pour dev)
*   **Async (optionnel)** :
    *   Redis Queue PoC (tâches lourdes : export audit, batch analysis)
*   **Frontend** :
    *   UX improvements : tables sortables, filtres avancés
*   **DoD** : migration testée, Postgres startup OK, queue PoC stable
*   **Durée estimée** : 10j

### ✅ Sprint 11 (22 Juin–03 Juil) — Hardening & Conformité (🔴 CRITIQUE)

**Objectif** : Sécurité renforcée + DPIA documentée = prérequis v1.0.

*   **Sécurité** :
    *   Redaction renforcée : patterns supplémentaires (numéro SS, IBAN...)
    *   Révision règles : ajuster taux faux positifs
*   **Conformité** :
    *   **DPIA** (Data Protection Impact Assessment) : document template
    *   Revue interne sécurité (checklist)
*   **Docs** :
    *   **Playbook déploiement** : dev → staging → prod (scripts, checklist)
    *   Procédures incident finalisées
*   **DoD** : DPIA complétée, playbook deployement OK, security checklist validée
*   **Durée estimée** : 10j
*   **🔴 ALERT** : DPIA = fondation IA Act, ne pas ignorer

### ✅ Sprint 12 (06–17 Juil) — Release v1.0 & Demo

**Objectif** : Stabilisation, démo, taggage release.

*   **Stabilisation** :
    *   Bugfix critiques identifiés en Sprint 11
    *   Performance final check
*   **Démo** :
    *   Internal demo (stakeholders) : use-cases clés
    *   Recueil feedback
*   **Release** :
    *   Tag `v1.0-ready`
    *   ADRs finalisés
    *   Docs review final
*   **DoD** : tag créé, démo pass, docs complètes, no critical bugs
*   **Durée estimée** : 10j

---

## 🎯 KPIs & HEALTH CHECK Par Sprint

| Sprint | Health Check Principal | Success Criteria | Red Flag | Target |
|---|---|---|---|---|
| **1** | `/health` OK + ADR-00/01 | `task dev` runs, lint passes | Deadline docs missed | 100% |
| **2** | Engine `analyze()` stable | PII detect 95%+ accurate, audit append-only | False positives > 10% | 95%+ |
| **3** | CRUD contacts opérationnel | OpenAPI stable, repos pattern OK | Schema unstable | 100% |
| **4** | YAML policies loaded | Factory pattern works, 3 rules active | Adapter Engine breaks | 100% |
| **5** | JWT generation/verification | Auth e2e pass, tokens expire correctly | JWT bypass found | 100% |
| **6** | RBAC guards enforced | Admin/viewer access controlled, PII redacted | Redaction missed | 100% |
| **7** | E2E tests pass | Logs JSON parsable, latency < 500ms | Latency > 1s | < 500ms |
| **8** | Coverage 75-80% + lint 100% | Tests pass, no warnings | Coverage < 70% | 75-80% |
| **9** | Adapter REST PoC | PostgreSQL schema valid, feature flag ready | Migration broken | 100% |
| **10** | Postgres migration OK | Queue PoC stable, zero data loss | Deadlocks/stalls | 100% |
| **11** | DPIA completed | Security checklist OK, redaction hardened | DPIA incomplete | 100% |
| **12** | v1.0 tag, demo OK | Docs final, no critical bugs | Blockers unresolved | 100% |

**Global KPIs (par sprint)** :
- **Stabilité API** : Breaking changes = 0 sur `/api/v1/*`
- **Couverture tests backend** : ≥ 75% à S8, ≥ 80% à S12
- **Latence Engine** : < 200 ms (dev), < 500 ms (stress)
- **Faux positifs rules** : < 5% (surveiller chaque sprint)
- **Incidents sécurité** : 0 secrets en clair, 0 PII non masquée

---

## 📐 MATRICE DE COUVERTURE CONCEPTS TECHNIQUES

| Concept Documenté | Sprint Intro | Sprint Maîtrise | Status |
|---|---|---|---|
| **API-first** | 1 | 5 | ✅ Fondation jour 1 |
| **SoC (Backend/Engine/Frontend)** | 1 | 6 | ✅ Structuré immédiatement |
| **SOLID (Repository/Factory/Strategy)** | 1 | 8 | ✅ Patterns appliqués progressivement |
| **Strategy Pattern (Rules)** | 2 | 4 | ✅ Règles déclaratives YAML |
| **Adapter Pattern (Backend→Engine)** | 2 | 9 | ✅ Scalable vers service |
| **JWT/RBAC** | 5 | 6 | 🔴 **CRITÈRE GO/NO-GO** |
| **PII Masking & Redaction** | 2 | 11 | 🔴 **CRITÈRE GO/NO-GO** |
| **Audit Trail Immuable** | 2 | 6 | 🔴 **CRITÈRE GO/NO-GO** |
| **Structured Logging** | 7 | 8 | ✅ JSON logs complets |
| **IA Act Conformité** | 2 | 11 | 🔴 **DPIA obligatoire** |
| **PostgreSQL Migration** | 9 | 10 | ✅ Alembic + Compose |
| **Docker & K8s Ready** | 11 | 12 | ⚠️ Playbook seulement (pas d'images) |

---

## ⚠️ Risques & Plans de mitigation (POST-AUDIT)

| Risque | Probabilité | Impact | Mitigation | Sprint Focus |
|---|---|---|---|---|
| **Sprints 3-6 trop denses** | 🟡 Moyen | 🔴 Critique (slips) | Decomposition complète, ressource additionnelle si besoin | 3-6 |
| **Audit Trail cassée découverte tard** | 🟡 Moyen | 🔴 Critique | Review architecte S1, tests immuabilité, pas exceptions | **2** |
| **Auth/RBAC faible en prod** | 🟡 Moyen | 🔴 Critique | External expert review, RBAC guards exhaustifs | **5-6** |
| **Faux positifs compliance (< 5%)** | 🟢 Bas | 🟡 Moyen (UX) | Observer KPI S2-S8, tuner patterns, exceptions contrôlées | 2-8 |
| **Performance regex** | 🟢 Bas | 🟡 Moyen | Bench S7, fallback algos robustes | 7 |
| **DPIA incomplete ou superficielle** | 🟡 Moyen | 🔴 Critique (légal) | Template pré-rempli, expert légal review | **11** |
| **Sur-ingénierie micro-services trop tôt** | 🟡 Moyen | 🟡 Moyen | YAGNI strict, feature flags, décision data-driven | 9+ |
| **Défaut couverture tests (< 75%)** | 🟡 Moyen | 🟡 Moyen | CI obligatoire S1, cible 75% S8 | 8 |

**Escalade** : Chaque risque 🔴 Critique → daily stand-up, blockers aired immédiatement.

---

## 📚 Documentation & Livrables

*   **README** (enrichi : Architecture, Stack figée, Principes) ✅
*   **ADRs** : 00 (système), 01 (architecture), 02 (FastAPI), 03 (stack figée)
*   **AIrules.md** (politiques IA & enforcement) ✅
*   **docs/architecture/stack.md** (diagrammes, règles par module) ✅
*   **Playbook déploiement** (prod)
*   **DPIA document** (IA Act)

---

## 🧭 Gouvernance & Rituels

*   **Planning Sprint** : Lundi matin (30 min)
*   **Stand-up** : Quotidien (15 min)
*   **Revue** : Vendredi fin de sprint (démo + métriques)
*   **Rétrospective** : 45 min (améliorations)
*   **ADR** : Toute décision structurante → ADR avant merge
*   **Qualité** : PRs avec lint/test obligatoires (Taskfile)

---

## ✅ À la fin des 6 mois (v1.0-ready)

*   **API CRM stable** : auth, CRUD clients/contacts, RBAC 4 rôles
*   **Compliance Engine opérationnel** : ≥ 4 règles clés (PII, mass-export, secrets, scope), audit complet, masking PII 100%
*   **Dashboard Next.js fonctionnel** : CRM CRUD, Compliance Vue, Audit détaillé, filtres
*   **Stack figée** : ADRs 0-3 complets, README enrichi, docs/architecture/stack.md détaillé
*   **Observabilité de base** : logs JSON structurés, latence mesurée, traces corrélées
*   **Sécurité durcie** : DPIA complétée, JWT/RBAC validée, redaction PII 100%
*   **Option Engine service** : Adapter REST PoC ready (activation si charge l'exige)
*   **Playbook déploiement** : procédures dev→staging→prod documentées

---

## 🚀 RECOMMANDATIONS FINALES (ACTION ITEMS)

### **IMMÉDIAT (Avant Sprint 1) :**
- [ ] Valider réalisme avec équipe (2-3 devs : back/engine/front) ou ajuster ressources
- [ ] **Assigner mentors par module** (Backend expert, Engine expert, Frontend expert)
- [ ] Créer **ADR-04 : Plan DevOps/Déploiement** (hors scope MVP, critique pour v1.0)
- [ ] Setup **CI léger** (linting pre-commit, GitHub Actions stub)
- [ ] Planifier **external security review** pour Sprint 5 (auth)

### **SPRINT 1 :**
- [ ] Daily stand-up 15min (async status si asynchrone)
- [ ] **ADR-00/01 finish par J2** (pas de drift)
- [ ] Setup monitoring KPIs (spreadsheet ou dashboard)
- [ ] Tester Taskfile → `/health` dès J3

### **CRITICAL PATH (ne pas échouer) :**
- [ ] **Sprint 2** : Audit trail immuable = fondation, pas de compromis
- [ ] **Sprint 5-6** : Auth/RBAC + external review = prérequis sécurité
- [ ] **Sprint 11** : DPIA + hardening = prérequis IA Act

---

## 🛠️ Checklist Détaillée par Module (DoD spécifique)

### Backend (FastAPI) — AVANT v1.0

*   [ ] Routers sous `infrastructure/http/`, DTO Pydantic (core/domain/)
*   [ ] Services isolés (`core/services`), aucune logique dans routers
*   [ ] Repository pattern SQLAlchemy (`infrastructure/db/repositories`)
*   [ ] Adapter Engine stable (`infrastructure/http/compliance_adapter.py`)
*   [ ] Tests unitaires & intégration (Pytest, ≥ 75% coverage S8)
*   [ ] OpenAPI auto-documentation (endpoints documentés)
*   [ ] Logging JSON structuré (requestId, auditId, actor)
*   [ ] CORS middleware + rate limiting basique
*   [ ] JWT auth + RBAC guards sur endpoints sensibles
*   [ ] Secrets never in logs or responses
*   [ ] Error handling uniforme (HTTP status, messages clairs)
*   [ ] Database migrations (Alembic) testées

### Compliance Engine (Python) — AVANT v1.0

*   [ ] Rules implémentées en Strategy pattern + Factory
*   [ ] Chaque rule : interface stable, tests 100%
*   [ ] Audit append-only : jamais écrasable, immuable
*   [ ] PII masquage AVANT stockage audit (jamais en clair)
*   [ ] Decorator instrumentation : timings, counters
*   [ ] Redaction outputs : post-completion
*   [ ] Policy YAML loader (ai/policies/policy_set.yaml)
*   [ ] Tests par règle + orchestration pipeline
*   [ ] Faux positifs monitored (< 5% cible)
*   [ ] Logging JSON structuré (règles tracées)

### Frontend (Next.js/TypeScript) — AVANT v1.0

*   [ ] Services API centralisés (`lib/api.ts`), pas appels directs
*   [ ] Types TypeScript alignés avec backend (DTO mappés)
*   [ ] ComplianceBanner component (risk/findings affichés)
*   [ ] Pages : Dashboard, Contacts CRUD, Clients CRUD, Audit détaillé
*   [ ] Auth : Connexion, token storage (localStorage), refresh
*   [ ] RBAC : affichage conditionnel par rôle
*   [ ] ESLint + Prettier 100% (CI obligatoire)
*   [ ] E2E tests légers (auth + compliance flow)
*   [ ] Responsive design (mobile-ready)
*   [ ] Error handling : messages clairs à l'utilisateur

### DevOps/Infra — AVANT v1.0

*   [ ] Taskfile : tasks install, backend, frontend, dev, test-*, lint-*, fmt-*
*   [ ] Dockerfile sketch (not built, but prepared)
*   [ ] docker-compose.yml pour Postgres + Redis (dev)
*   [ ] GitHub Actions CI : lint + test backend/frontend
*   [ ] Playbook déploiement (dev→staging→prod) documenté
*   [ ] Environment variables (.env.example fourni)
*   [ ] PostgreSQL migrations (Alembic, testées)

### Docs — AVANT v1.0

*   [ ] **ADR-00** (système ADR) ✅
*   [ ] **ADR-01** (architecture globale) ✅
*   [ ] **ADR-02** (FastAPI choice) ✅
*   [ ] **ADR-03** (stack technique) ✅
*   [ ] **README** (enrichi : vision, stack, installation) ✅
*   [ ] **docs/architecture/stack.md** (diagrammes, règles par module) ✅
*   [ ] **AI-RULES.md** (politiques, examples, incident playbook) ✅
*   [ ] **Playbook déploiement** (procédures, checklist)
*   [ ] **DPIA document** (IA Act compliance attestation)
*   [ ] **API docs** (OpenAPI, Swagger UI)
*   [ ] **Contributing guide** (pour futurs contributeurs)

---

**Fin du planning v2 (post-audit)**
