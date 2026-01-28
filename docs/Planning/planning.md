# 📅 Planning NovaCRM + AI Compliance Hub — v2 (POST-AUDIT)

**Statut** : Planning RÉVISÉ suite audit de cohérence (28 Janvier 2026)  
**Raison** : Sprints 3-6 trop denses, manque d'intégrations externes, chemin critique non explicité  
**Lire aussi** : `planning_v2_audit.md` (version complète avec matrice technique, risques détaillés)

Le planning démarre **semaine du 2 février 2026** et s'étend jusqu'à **fin juillet 2026** (aligné sur ta timezone).  
**Cette version** : sprints decomposés, 3 critères go/no-go, health checks par sprint, checklists finalisées.

---

# 🔴 CHEMIN CRITIQUE (3 go/no-go)

| Étape | Sprint | Raison | Success Criteria | Risque | Mitigation |
|---|---|---|---|---|---|
| **Audit Immuable** | 2 | Fondation IA Act | Append-only OK, PII masked, 100% tests | Découverte tard = refactorisation massive | Review J1, pas exceptions, tests complets |
| **Auth/RBAC** | 5-6 | Socle sécurité | JWT/RBAC 100% tested, external review OK | Auth faible = incident grave | Expert externe, guards exhaustifs |
| **DPIA & Hardening** | 11 | Conformité légale | DPIA complétée, redaction 100%, checklist OK | Déployer sans DPIA = non-conformité | Template pré-rempli, expert légal |

**Si l'une échoue → impossible de continuer. Escalade immédiate.**

---

# 📅 Vue d’ensemble (6 mois)

*   **Cadence** : sprints de **2 semaines**
*   **Organisation** : 3 flux parallèles
    1.  **Backend (FastAPI)** — API CRM, auth, orchestration, persistance
    2.  **Compliance Engine (Python)** — policies, scanner, audit trail
    3.  **Frontend (Next.js)** — dashboard CRM + compliance
*   **Orchestration** : **Taskfile** pour toutes les actions (install, dev, test, lint, fmt)
*   **Docs & Décisions** : ADRs (MADR), README, guides d’archi

***

## 🗺️ Macro‑timeline & Jalons clés (POST-AUDIT)

**Note audit** : Planning original trop dense. Sprints 3-6 decomposés pour réalisme. Chemin critique identifié = Auth (S5-6) + Audit (S6-8).

| Mois                          | Objectif principal                                            | Jalons                                                        |
| ----------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| **Fév 2026 (Sprints 1–2)**    | **MVP technique** : structure, endpoints de base, 1 règle IA  | ADR-00/01 + README, `/health`, Rule `no_pii`, Audit v1, UI skeleton |
| **Mars 2026 (Sprints 3–4)**   | **MVP fonctionnel** : CRUD 1 entité, 3 rules IA, YAML policies| CRUD Contacts, Rules (PII/mass-export/secrets), Policy loader |
| **Avr 2026 (Sprints 5–6)**    | **Sécurité & Compliance** : Auth, RBAC, Audit complet, masking| JWT/OAuth2, RBAC 4 rôles, Audit JSON export, redaction PII   |
| **Mai 2026 (Sprints 7–8)**    | **Qualité & Observabilité** : E2E, logs JSON, couverture 75%+ | Structured logging, E2E flows, 75-80% test coverage, AIrules  |
| **Juin 2026 (Sprints 9–10)**  | **Scalabilité & Persistance** : Engine adapter, PostgreSQL    | Adapter REST PoC, PostgreSQL migration, Redis Queue PoC        |
| **Juil 2026 (Sprints 11–12)** | **Hardening & Release v1.0** : DPIA, playbook, démo interne   | DPIA doc, playbook déploiement, revue sécu, tag v1.0-ready    |

***

# 📌 Détail par sprint (2 semaines)

> **DoD commun** : lint & format OK, tests unitaires OK, endpoints stables documentés (OpenAPI), ADR mis à jour si décision structurante.

### ✅ Sprint 1 (02–13 Fév)

*   **Backend** :
    *   Router `GET /api/v1/health` + structuration de base (`api/`, `app/`, `repositories/`)
    *   Schémas Pydantic initiaux (DTO de base)
*   **Engine** :
    *   Squelette `Engine.analyze()` + **Rule `no_pii_in_prompts`**
*   **Frontend** :
    *   Setup Next.js + `src/lib/api.ts` + page Dashboard (placeholder)
*   **Docs** :
    *   **ADR‑00**, **ADR‑01**, **ADR‑02**, **ADR‑03**, **README**, **docs/architecture/stack.md**
*   **DoD** : `task install`, `task backend`, `task frontend`, `task dev` → OK

### ✅ Sprint 2 (16–27 Fév)

*   **Backend** :
    *   `POST /api/v1/compliance/check` (contrat basique)
    *   Logger JSON minimal (corrélation `requestId`)
*   **Engine** :
    *   **Rule `no_mass_export_requests`** + aggregation `risk`/`action`
    *   Audit append-only (fichier) + masquage PII avant stockage
*   **Frontend** :
    *   Component **ComplianceBanner** (affiche warn/block/escalate)
*   **DoD** : tests unité (backend/engine), 60% lint OK

### ✅ Sprint 3 (02–13 Mars)

*   **Backend (CRM)** :
    *   CRUD `clients`, `contacts` (SQLite) + services/repositories
*   **Engine** :
    *   **Rule `no_secrets_in_prompts`** (Critical) + escalate
*   **Frontend** :
    *   Pages CRUD (List/Create/Edit) clients/contacts
*   **DoD** : OpenAPI stable, CI minimal (lint + test backend)

### ✅ Sprint 4 (16–27 Mars)

*   **Backend** :
    *   `scope_check` (parametré par org/user) côté engine via adapter
*   **Engine** :
    *   YAML `policy_set.yaml` + loader
*   **Frontend** :
    *   Vue Compliance détaillée (findings list), filtres par règle
*   **DoD** : Audit trail enrichi (auditId), 65% coverage

### ✅ Sprint 5 (30 Mars–10 Avr)

*   **Sécurité** :
    *   Auth **JWT/OAuth2** + middleware CORS strict
    *   RBAC : rôles `admin/manager/analyst/viewer` + guards
*   **Frontend** :
    *   Connexion / session, rôles en UI (affichage conditionnel)
*   **DoD** : e2e léger (auth + call compliance), 70% coverage

### ✅ Sprint 6 (13–24 Avr)

*   **Engine** :
    *   **Decorator** instrumentation (timings, counters)
    *   `redact_outputs` (post‑completion)
*   **Backend** :
    *   Endpoint `GET /api/v1/compliance/audit/:id`
*   **Frontend** :
    *   Page Audit — visualisation détaillée (findings, redactions)
*   **DoD** : tests masking/PII, audit export JSON

### ✅ Sprint 7 (27 Avr–08 Mai)

*   **Observabilité** :
    *   Logs JSON uniformes (API & Engine) + champs (`requestId`, `auditId`)
    *   **Draft `/metrics`** (latences moyennes, taux de block/warn)
*   **Perf** :
    *   Bench scan (scripts dev), tuning regex / I/O
*   **DoD** : traces basiques, rapport perf sprint

### ✅ Sprint 8 (11–22 Mai)

*   **Qualité** :
    *   Durcissement lint (Ruff/ESLint), format (Black/Prettier)
    *   Tests intégration plus complets (compliance + CRUD + auth)
*   **Docs** :
    *   Guide **AIrules.md** finalisé, procédures incident
*   **DoD** : 75–80% coverage, checklists sécurité

### ✅ Sprint 9 (25 Mai–05 Juin)

*   **Scalabilité option** :
    *   **Adapter réseau** Engine (REST interne ou gRPC) — PoC
    *   Basculer `COMPLIANCE_MODE=local|service` (feature flag)
*   **DB** :
    *   Migration **PostgreSQL** (prod) — schémas + Alembic
*   **DoD** : tests sur les deux modes (local/service), migration testée

### ✅ Sprint 10 (08–19 Juin)

*   **Queue (option)** :
    *   Job asynchrone simple (ex. Redis Queue/FIFO) pour tâches lourdes
*   **Frontend** :
    *   UX amélioration (tables, filtres, pagination)
*   **DoD** : charge test basique, timeouts gérés, stabilité

### ✅ Sprint 11 (22 Juin–03 Juil)

*   **Hardening sécurité** :
    *   Redaction renforcée, règles durcies, DPIA note
*   **Docs** :
    *   Playbook déploiement (dev → prod), opérabilité
*   **DoD** : pentest léger interne, checklists conformité

### ✅ Sprint 12 (06–17 Juil)

*   **Release** :
    *   Stabilisation, bugfix, performance
    *   **Démo interne** (use-cases clés), feedbacks
*   **DoD** : tag `v1.0-ready`, ADRs finalisés, doc complète

***

# 🎯 KPIs (à suivre à chaque sprint)

*   **Stabilité API** : Breaking changes ≤ 0 sur `/api/v1/*`
*   **Couverture tests backend** : **≥ 75%** à M8, **≥ 80%** à M12
*   **Latence moyenne analyse** (Engine) : **< 200 ms** (dev), **< 500 ms** (stress)
*   **Taux de faux positifs** (rules) : surveiller & < 5% (cible)
*   **Incidents sécurité** : 0 secrets stockés en clair, 0 PII non masquée
*   **Adoption interne** : pages clés utilisées (audit/compliance/CRM)

***

# 🧠 Gouvernance & Rituels

*   **Planning Sprint** : Lundi matin (30 min)
*   **Stand-up** : Quotidien (15 min)
*   **Revue** : Vendredi fin de sprint (démo + métriques)
*   **Rétrospective** : 45 min (améliorations)
*   **ADR** : Toute décision structurante → ADR avant merge
*   **Qualité** : PRs avec lint/test obligatoires (Taskfile)

***

# 🛠️ Checklist par module (DoD spécifique)

### Backend (FastAPI)

*   [ ] Routers sous `api/v1`, DTO Pydantic
*   [ ] Services isolés (`app/services`)
*   [ ] Repos SQLAlchemy (`app/repositories`)
*   [ ] Adapter Engine stable (`app/adapters/compliance_adapter.py`)
*   [ ] Tests unitaires & intégration (Pytest)

### Compliance Engine (Python)

*   [ ] Rules en Strategy + Factory (clé `key`)
*   [ ] Masking PII avant stockage audit
*   [ ] Decorator instrumentation (timings)
*   [ ] Audit append-only (fichier/dev ; table/prod)
*   [ ] Tests par règle + orchestration

### Frontend (Next.js/TS)

*   [ ] Services API centralisés (`src/lib/api.ts`)
*   [ ] Types TS alignés (OpenAPI ou types déclarés)
*   [ ] UI ComplianceBanner + pages Audit/CRM
*   [ ] ESLint + Prettier OK

***

# 📚 Documentation & Livrables

*   **README** (enrichi : Architecture, Stack figée, Principes)
*   **ADRs** : 00 (système), 01 (architecture), 02 (FastAPI), 03 (stack figée), + futurs (sécurité, persistance, scalabilité)
*   **AIrules.md** (politiques IA & enforcement)
*   **docs/architecture/stack.md** (diagrammes, règles par module)
*   **Playbook déploiement** (prod)

***

# ⚠️ Risques & Plans de mitigation

*   **Sur‑ingénierie micro‑services** (trop tôt)  
    → Rester en **mode module local**, activer service **seulement si besoin** (ADR + perf data).
*   **Faux positifs compliance** (UX frustrante)  
    → Ajuster patterns, ajouter exceptions contrôlées, **observer KPI**.
*   **Sécurité auth/RBAC insuffisante**  
    → ADR sécurité, revue régulière, tests e2e sur flows sensibles.
*   **Performance regex**  
    → Bench & tuning (Sprints 7–8), fallback sur algos plus robustes si nécessaire.

***

# ✅ À la fin des 6 mois (v1.0-ready)

*   API CRM stable (auth, CRUD)
*   Compliance Engine opérationnel (≥ 4 règles clés, audit complet, masking PII)
*   Dashboard Next.js fonctionnel (CRM + Compliance + Audit)
*   Stack figée, ADRs à jour, docs robustes
*   Observabilité de base + sécurité durcie
*   Option Engine **service séparé** prête si la charge l’exige

***

Si tu veux, je peux **générer un calendrier iCal** des sprints, ou créer **des issues GitHub** automatiquement par sprint (Backlog → En cours → Done) avec les titres/livrables ci‑dessus.

---

**📌 VOIR AUSSI** : `planning_v2_audit.md` pour version audit complète (matrice technique, health checks détaillés, checklists par module, recommendations finales).
