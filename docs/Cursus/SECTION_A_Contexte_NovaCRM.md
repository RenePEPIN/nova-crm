# 📍 SECTION A : Contexte NovaCRM + AI Compliance Hub

**Durée estimée** : 3-4 heures  
**Prérequis** : Aucun (démarrage du cursus)  
**Objectif** : Comprendre QUOI nous construisons et POURQUOI

---

## 📍 LEÇON 1 : Vision & Positioning — Qu'est-ce que NovaCRM?

### 📍 Le Concept (Théorie)

**Qu'est-ce qu'un CRM?**

Un CRM (Customer Relationship Management) est une plateforme centralisée pour gérer :
- 👥 **Contacts** : Personnes (mails, phones, historique)
- 🏢 **Clients** : Entreprises (contrats, revenus, opportunités)
- 📊 **Interactions** : Emails, calls, meetings (traçabilité)
- 📈 **Pipeline** : Opportunités commerciales (valeur, probabilité, stage)

**Analogie concrète** : Un CRM c'est comme un **carnet d'adresse sur stéroïdes**. Au lieu de juste noter "Jean Dupont - jean@example.com", vous stockez :
- Tous ses emails reçus
- Historique des appels (durée, sujets)
- Compagnie, poste, secteur d'activité
- Dernière interaction (date, contexte)
- Valeur commerciale estimée
- Prochaines étapes (follow-up, livrable)

**Cas classique** : Un commercial appelle un prospect. Sans CRM : "Qui c'est? Quand j'ai parlé last time? Quel était mon offer?" → **temps perdu, relation brisée**. Avec CRM : **Un clic → tout l'historique → vente plus rapide**.

---

### 🚀 Cas d'usage Réel (NovaCRM + AI Hub)

NovaCRM = CRM traditionnel **+ AI Compliance Hub** pour réguler l'usage de l'IA.

**Scenario concret** :

```
T=0 : Commerciante Sophie ouvre NovaCRM
      → Voit client "Banque Nationale" (historique 50 interactions)
      → Demande à l'AI Assistant : "Resume les risques compliance de ce client"

T=0.5s : AI Compliance Engine analyse :
        - Email mentionnant "IBAN 123456789" → 🚨 Données financières sensibles
        - Chat mentionnant "Divorce Jean Dupont" → 🚨 Données personnelles sensibles
        - Document "Contract_signed_2025.pdf" → ✅ Non-sensible

T=1s : Engine rapporte à Sophie :
      "⚠️ 2 données sensibles (PII) détectées → redactées avant stockage audit"

T=2s : Audit trail immuable enregistre :
      "[2026-01-28 10:15:23] Sophie requested compliance_check on contact:892 
       → 2 PII detected → masking applied → stored securely"
```

**Pourquoi ça change tout** :

1. **Compliance automatique** : Sophie ne peut pas accidentellement envoyer PII en email (masqué avant)
2. **Audit immuable** : "Qui a vu quelles données? Quand?" → Historique inviolable
3. **Conformité IA Act EU 2024** : Si procès, prouvez que vous avez protégé PII → Vous êtes couvert légalement

**NovaCRM = CRM + Compliance Enforcer pour IA Act compliance**

---

### 💻 Le Lab Pratique — Contexte & Navigation

#### **LAB 1.1 : Démarrer le projet, explorer la structure**

**Objectif** : Comprendre où est chaque code, où est chaque service.

**Étape 1 : Clone et naviguez**
```powershell
# Terminal WSL2
cd /home/renep/dev/nova-crm

# Listez la structure
ls -la
# Vous verrez :
# - backend/       → API FastAPI (contactez données, compliance)
# - frontend/      → Dashboard Next.js (interface graphique)
# - ai/            → Engine IA (analyses compliance, détecteurs)
# - docs/          → Documentation (ce que vous lisez)
# - scripts/       → Utilitaires
# - infra/         → Kubernetes, Terraform

# Explorez le backend
cd backend
ls -la
# Vous verrez :
# - core/          → Logique métier (domains, services)
# - infrastructure/→ Couche technique (DB, HTTP, logs)
# - main.py ou app.py → Démarrage FastAPI

# Explorez le frontend
cd ../frontend
ls -la
# Vous verrez :
# - app/           → Pages Next.js, composants React
# - lib/           → Utilities (API client, auth, hooks)
# - public/        → Assets (images, logos)

# Explorez l'Engine IA
cd ../ai
ls -la
# Vous verrez :
# - detectors/     → Détecteurs de risques (PII, secrets, scope)
# - pipelines/     → Flux de traitement (input → detection → masking → output)
# - policies/      → Règles déclaratives (YAML)

# Explorez la documentation
cd ../docs
tree
# Vous verrez :
# - adr/           → Architecture Decision Records (pourquoi FastAPI? pourquoi 3 modules?)
# - architecture/  → stack.md (qui fait quoi)
# - Planning/      → Sprints 1-12 (roadmap)
# - Compréhension/ → Ce cursus

echo "✅ Exploration terminée"
```

**Étape 2 : Lisez les fichiers clés (10 min)**
```powershell
# Lisez la vision (README)
cat README.md | head -50

# Lisez l'architecture figée (stack.md)
cat docs/architecture/stack.md | head -100

# Lisez les règles IA (AI-RULES.md)
cat AI-RULES.md | head -80
```

**Résultat attendu** : Vous comprenez
- ✅ Où est le code
- ✅ Qu'est-ce que chaque module fait (backend = API, frontend = UI, ai = compliance)
- ✅ Qu'est-ce que NovaCRM + AI Hub = CRM + compliance enforcer

---

#### **LAB 1.2 : Lire les ADR (Architecture Decision Records)**

**Objectif** : Comprendre les choix technologiques et POURQUOI.

```powershell
# Allez au dossier ADR
cd docs/adr

# Lisez les décisions
cat "ADR‑01 — Choix de l'Architecture Globale du Projet NovaCRM + AI Compliance Hub.md" | head -80
# Vous apprendrez : Pourquoi 3 modules (backend/frontend/ai)?

cat "ADR‑02 — Choix de FastAPI plutôt que Django pour le backend.md" | head -60
# Vous apprendrez : Pourquoi FastAPI et pas Django?

cat "ADR‑03 — Stack Technique.md" | head -60
# Vous apprendrez : Toutes les techno (PostgreSQL, Next.js, Python, Alembic, etc)
```

**Points clés à noter** :

| ADR | Décision | Raison |
|-----|----------|--------|
| 01 | 3 modules : backend/frontend/ai | Séparation des préoccupations (SoC), scaling indépendant |
| 02 | FastAPI vs Django | Performance, async/await, type hints, compliance checks temps réel |
| 03 | Stack complet | PostgreSQL (production), Alembic (migrations), Docker (déploiement) |

**Résultat attendu** : Vous comprenez QUE ces choix sont documentés et PAS aléatoires.

---

#### **LAB 1.3 : Glossaire du Projet**

**Objectif** : Mémoriser les termes clés de NovaCRM (utilisés partout dans le code/docs).

**À retenir** :

| Terme | Définition | Exemple |
|-------|-----------|---------|
| **auditId** | ID unique pour chaque action compliance | `audit_20260128_152034_sophie_contact_892_view` |
| **requestId** | ID unique pour chaque requête API | `req_1234567890_GET_/api/v1/contacts` |
| **scope** | Permissions (contact, client, audit, settings) | Sophie peut voir Contacts mais pas Settings (admin-only) |
| **rule** | Une détection de risque (PII, secret, hors-scope) | `no_pii_in_prompts`, `no_api_keys_exposed` |
| **policy** | Ensemble de règles déclaratives (YAML) | `compliance_policy_v1.yaml` = [no_pii, no_secrets, max_token_limit] |
| **redaction** | Masquage de données sensibles | "IBAN 123456789" → "IBAN xxxxxx789" |
| **PII** | Personally Identifiable Information | Emails, phones, IBANs, SS#, addresses |
| **IA Act** | EU Regulation 2024 (compliance artificielle) | Obligations : traçabilité, PII protection, audit immuable |
| **append-only audit** | Logs immuables (impossible de modifier) | Une fois enregistré, immodifiable (sauf destruction totale DB) |

**Ressource** : Voir [AI-RULES.md](../../AI-RULES.md) section 1 pour détails complets.

---

### 💼 Préparation Entretien (Q&A)

#### **Q1 : "Décrivez NovaCRM en 1 minute. Qu'est-ce qui le différencie d'un CRM classique?"**

**Réponse attendue** :

> "NovaCRM est un CRM traditionnel pour gérer contacts/clients/opportunités, mais enrichi d'un **AI Compliance Hub** qui applique automatiquement la conformité IA Act.
>
> **Différenciation clé** :
> 1. **Compliance automatique** : Avant de stocker une donnée, l'Engine IA analyse si elle contient PII/secrets. Si oui → redaction avant stockage.
> 2. **Audit immuable** : Chaque action (qui a vu quoi, quand) est enregistrée dans un audit trail append-only. Immodifiable, conforme IA Act.
> 3. **4-role RBAC** : Admin/Manager/Analyst/Viewer avec permissions granulaires sur contact/client/audit.
> 4. **Data protection by design** : PII est masquée par défaut, visible seulement si role + scope l'autorise + audit trail enregistré.
>
> **Use case** : Un commercial utilise NovaCRM. L'Engine détecte automatiquement si un email contient un IBAN (PII). Avant de le stocker, il redacte l'IBAN. L'audit trail enregistre : '[2026-01-28] User:sophie saw PII in email:123 → redacted'. Si un client demande 'qui a vu mes données?', réponse immuable : juste sophie, 28 jan, pour contact check. Zéro violation possible."

**Score** : ✅ Vous montrez
- Compréhension du produit (CRM + compliance)
- Connaissance des différenciateurs (audit immuable, PII masking, IA Act)
- Pensée produit (use case concret)

---

#### **Q2 : "Pourquoi 3 modules (backend/frontend/ai) plutôt qu'une monolith?"**

**Réponse attendue** :

> "3 modules = **Separation of Concerns (SoC)** appliquée à NovaCRM.
>
> 1. **Backend** (FastAPI) : API REST pour contacts/clients/audit. Rôle = orchestration, persistance, validation métier.
> 2. **Frontend** (Next.js) : UI dashboard. Rôle = affichage, UX, state management client.
> 3. **AI Engine** (Python) : Analyse compliance. Rôle = détection risques (PII, secrets), redaction, policy evaluation.
>
> **Avantages SoC** :
> - **Scaling indépendant** : Engine reçoit 10M requêtes/jour? On scale juste Engine, pas frontend.
> - **Équipes isolées** : Team backend peut déployer sans toucher à l'Engine. Zéro couplage.
> - **Réutilisabilité** : Engine peut servir d'autres produits (pas juste NovaCRM). API universelle.
> - **Testing** : Chaque module a tests indépendants. Zéro effet de bord.
>
> **Si c'était une monolith** : Modification Engine → rebuild tout → redéployer tout. Risque 100x plus grand. SoC = risk mitigation."

**Score** : ✅ Vous montrez
- Compréhension architecture (SoC pattern)
- Pensée scaling & operations
- Risk awareness (pourquoi découpler)

---

#### **Q3 : "Expliquez l'audit trail immuable. Pourquoi append-only et pas modifiable?"**

**Réponse attendue** :

> "**Audit trail immuable** = log d'actions qui ne peut pas être modifié une fois écrit. Append-only = on peut juste ajouter, jamais modifier/effacer.
>
> **Pourquoi append-only?**
>
> Imagine une monnaie : si vous pouviez modifier votre compte bancaire, la banque serait inutile. De même, si vous pouviez modifier l'audit trail, la traçabilité serait inutile.
>
> **Exemple concret** :
> - [2026-01-28 10:00] Sophie opened contact:892 (Client: Jean Dupont)
> - [2026-01-28 10:01] Engine detected PII (IBAN) → redacted
> - [2026-01-28 10:02] Audit recorded : 'Sophie viewed redacted contact:892'
>
> Si plus tard Sophie dit 'Je n'ai jamais vu PII', vous vérifiez audit trail → ✅ Preuve immuable. Impossible de falsifier.
>
> **Conformité IA Act** : EU demande traçabilité complète pour data processing IA. Append-only audit = preuve légale que vous avez respecté le réglement.
>
> **Implémentation** : Stockage dans DB append-only (ex: Event Sourcing, immutable logs). Pas d'UPDATE SQL, juste INSERT. Archive immédiate pour compliance."

**Score** : ✅ Vous montrez
- Compréhension compliance (pourquoi immuable)
- Pensée légale (IA Act)
- Implémentation awareness

---

#### **Q4 : "Qu'est-ce que PII? Donnez des exemples pour NovaCRM."**

**Réponse attendue** :

> "**PII** (Personally Identifiable Information) = toute donnée identifiant une personne physique.
>
> **Exemples NovaCRM** :
>
> | PII | Raison | Exemple |
> |-----|--------|---------|
> | Email | Identifie personne | sophie@example.com |
> | Phone | Identifie personne | +33 6 12 34 56 78 |
> | IBAN | Données bancaires sensibles | FR76 30003 00010 xxxxxxxx |
> | SS# | Identité sociale sensibles | 1 87 12 34 567 xxxxxx |
> | Address | Localisation sensible | 123 Rue de la Paix, Paris |
> | Company + Name | Combinaison identifiante | Sophie Martin @ Google Paris |
>
> **Stratégie NovaCRM** :
> 1. **Detection** : Engine détecte PII via regex/ML (emails = `.*@.*\\..*`, IBANs = `^[A-Z]{2}[0-9]{2}`, etc)
> 2. **Masking** : Avant stockage, redacte. sophie@example.com → sophi\*@\*\*\*\*ple.com
> 3. **Access control** : Seul role:admin + scope:pii peut voir non-masqué. Audit trail enregistre accès.
> 4. **Retention** : PII supprimé après 365 jours (GDPR).
>
> **Pourquoi?** IA Act EU demande protection active de PII. Passif (firewall) = insuffisant. Actif (masking) = conforme."

**Score** : ✅ Vous montrez
- Connaissance PII définitions
- Stratégie de protection multi-couches
- Compliance thinking

---

### ✅ Validation de l'étape

**Checklist — Vous avez compris SECTION A quand** :

- [ ] Vous pouvez **expliquer NovaCRM en 1 phrase** : "CRM + AI Compliance Hub pour gérer contacts/clients avec protection PII automatique"
- [ ] Vous connaissez les **3 modules** (backend, frontend, ai) et leur rôle respectif
- [ ] Vous comprenez **pourquoi SoC** (séparation concerns = scaling, testing, risk mitigation)
- [ ] Vous connaissez au moins **5 termes du glossaire** (auditId, requestId, rule, PII, append-only audit)
- [ ] Vous savez **pourquoi audit trail immuable** (conformité IA Act + preuve légale)
- [ ] Vous avez **exploré la structure du projet** (backend/, frontend/, ai/, docs/)
- [ ] Vous avez **lu ADR-01, ADR-02, ADR-03** (architecture decisions)
- [ ] Vous comprenez **PII definition + examples** (emails, phones, IBANs, addresses)
- [ ] Vous répondriez aux **4 questions entretien** ci-dessus avec confiance

**Validation pratique** :

```powershell
# Terminal : vérifiez que git est clean
cd /home/renep/dev/nova-crm
git status
# Doit montrer "On branch main, nothing to commit"

# Vérifiez que vous pouvez lister la structure
ls -la
# backend/, frontend/, ai/, docs/, README.md, AI-RULES.md présents ✅

# Vérifiez que vous avez lu au moins un ADR
grep -r "Architecture Decision" docs/adr/ | head -1
# Doit trouver au least un ADR ✅

echo "✅ SECTION A validée"
```

**Prochaine étape** : SECTION B — Architecture Appliquée (comment la structure se traduit en code)

---

## 📍 LEÇON 2 : Glossaire complet & Termes clés

**Durée** : 30 min (lecture)

### Glossaire complet du projet

```
🏗️ ARCHITECTURE
├─ SoC (Separation of Concerns)     = Modularity principle, chaque module une responsabilité
├─ Monolith                         = Tout le code dans une seule app (risqué)
├─ Hexagonal Architecture           = Ports & adapters, isoler logique métier
├─ API-first design                 = Contracts définis avant code

🗄️ DATA & PERSISTENCE
├─ Entity                           = Classe mappée à table DB (ex: Contact, Client)
├─ Repository pattern               = Abstraction pour requêtes DB (ex: ContactRepository)
├─ ORM (Object-Relational Mapping)  = SQLAlchemy, mappe objets → SQL (ex: Contact.name → SQL SELECT)
├─ Migration                        = Changement versionnié de schéma DB (Alembic)
├─ Append-only audit                = Logs immuables, INSERT only, jamais DELETE/UPDATE

🔐 SECURITY & COMPLIANCE
├─ PII (Personally Identifiable Information) = Données identifiant personne (emails, phones, IBANs)
├─ Redaction                        = Masquage données sensibles (secret@example.com → sec\*@\*\*\*\*\*\.com)
├─ RBAC (Role-Based Access Control) = Permissions par rôle (admin/manager/analyst/viewer)
├─ JWT (JSON Web Token)             = Token stateless pour authentification
├─ scope                            = Granularité permissions (contact/client/audit/settings)
├─ IA Act                           = EU Regulation 2024, compliance IA obligatoire
├─ DPIA (Data Protection Impact Assessment) = Évaluation risques données

🤖 AI & COMPLIANCE ENGINE
├─ Rule                             = Détection unique (no_pii_in_prompts, no_secrets)
├─ Detector                         = Classe implémentant une rule (PII detector, secrets detector)
├─ Policy                           = Ensemble de rules déclaratives (YAML)
├─ Strategy pattern                 = Design pattern pour rules pluggables
├─ Factory pattern                  = Pattern pour créer objets (RuleFactory crée rules)
├─ Adapter pattern                  = Pattern pour adapter deux interfaces (Backend ↔ Engine)

📊 OPERATIONS & MONITORING
├─ Correlation ID                   = ID unique pour tracer requête cross-modules
├─ auditId                          = ID unique pour chaque action compliance
├─ requestId                        = ID unique pour chaque requête API
├─ Structured logging               = Logs en JSON (pas plain text), queryable
├─ Instrumentation                  = Decoration avec timings, counters, traces

🚀 DEVOPS & DEPLOYMENT
├─ Taskfile                         = Orchestration tasks (install, backend, frontend, dev, test)
├─ Docker                           = Containerization pour deployment
├─ Alembic                          = Migration tool pour SQLAlchemy
├─ CI/CD                            = Continuous Integration/Deployment (GitHub Actions)
```

**À mémoriser avant SECTION B** : 
- SoC, monolith, hexagonal, API-first
- Entity, repository, ORM, migration
- PII, redaction, RBAC, JWT, scope
- Rule, detector, policy, strategy, factory, adapter
- auditId, requestId, correlation ID
- Structured logging, instrumentation

---

## 📍 LEÇON 3 : Planning & Roadmap (12 sprints)

**Objectif** : Comprendre QUAND on fait quoi dans les 6 mois (Février-Juillet 2026).

```
SPRINT 1 (Feb 3-14) — Setup & Audit Trail
├─ Backend : FastAPI hello world, SQLAlchemy setup, DB init
├─ Engine : Audit trail immuable design & first detector (no_pii)
├─ Frontend : Next.js hello world, auth UI skeleton
├─ ✅ Go/no-go checkpoint : Audit trail works + tests pass
└─ Deliverable : Backend + Engine + Frontend run locally

SPRINT 2 (Feb 17-28) — Core CRUD & Compliance
├─ Backend : Contacts CRUD endpoints, Repository pattern
├─ Engine : 3 rules (no_pii, no_secrets, scope_check)
├─ Frontend : Contacts list, create form
├─ ✅ Go/no-go checkpoint : Contacts CRUD + compliance working
└─ Deliverable : Backend ↔ Engine adapter, end-to-end flow

SPRINT 3-4 (Mar 3-28) — Clients & Testing
├─ Backend : Clients CRUD, refactor SOLID (SRP, OCP)
├─ Engine : Policy loader (YAML), decorator instrumentation
├─ Frontend : Clients list, dashboards, design tokens
├─ Deliverable : Clients module + test coverage 80%+

SPRINT 5 (Mar 31-Apr 11) — Auth & JWT
├─ Backend : JWT tokens, auth middleware, login endpoint
├─ Frontend : Auth flow, token storage, logout
├─ ✅ Go/no-go checkpoint : JWT auth works, tokens valid
└─ Deliverable : Protected endpoints, auth UI complete

SPRINT 6 (Apr 14-25) — RBAC & Permissions
├─ Backend : 4-role RBAC (admin/manager/analyst/viewer), guards
├─ Engine : Scope validation (can user see this contact?)
├─ Frontend : Role-based menu, audit trail viewer
├─ ✅ Go/no-go checkpoint : RBAC enforcement tested, no bypass
└─ Deliverable : Role-based access working end-to-end

SPRINT 7 (Apr 28-May 9) — Logging & Observability
├─ Backend : JSON structured logs, correlation IDs
├─ Engine : Instrumentation (timings, counters)
├─ Logging : requestId, auditId, actor propagation
├─ Deliverable : Cross-module tracing working

SPRINT 8 (May 12-23) — Advanced Features
├─ Backend : Opportunities CRUD, analytics endpoints
├─ Frontend : Opportunity dashboard, pipeline visualization
├─ Deliverable : Full CRM feature set

SPRINT 9 (May 26-Jun 6) — Performance & Scaling
├─ Backend : Query optimization (N+1 fixes), caching
├─ Engine : Performance tests (< 500ms compliance check)
├─ Deliverable : Performance baselines met

SPRINT 10 (Jun 9-20) — Data Migration & PostgreSQL
├─ Infra : PostgreSQL setup, migration scripts
├─ Backend : SQLite → PostgreSQL switch
├─ Testing : E2E tests on PostgreSQL
├─ Deliverable : Production DB ready

SPRINT 11 (Jun 23-Jul 4) — Security & DPIA
├─ Security : OWASP hardening, PII retention policy
├─ Compliance : DPIA template, IA Act audit
├─ Incident playbook : Detection, containment, recovery
├─ ✅ Go/no-go checkpoint : DPIA passed, no critical security gaps
└─ Deliverable : Security audit report clean

SPRINT 12 (Jul 7-18) — Deployment & Hardening
├─ DevOps : Docker, Kubernetes (basic), GitHub Actions CI/CD
├─ Deployment : Dev→staging→prod pipeline
├─ Hardening : Secrets vault, SSL/TLS, rate limiting
├─ Deliverable : Production-ready system
└─ ✅ Final Go : System ready for first beta users
```

**3 Critical Path Checkpoints** :
1. **Sprint 2** : Audit trail must be immuable ✅ or restart S1
2. **Sprint 5-6** : Auth + RBAC must be bypass-proof ✅ or restart S5
3. **Sprint 11** : DPIA + security audit clean ✅ or delay launch

**Ressource** : Voir `docs/Planning/nova_crm_sprints.ics` (calendar avec tous les événements).

---

**Fin de SECTION A**

✅ **Vous savez maintenant** :
- Qu'est-ce que NovaCRM + AI Hub
- Pourquoi 3 modules (SoC)
- Pourquoi audit trail immuable (IA Act)
- Glossaire clé (PII, rules, RBAC, etc)
- Roadmap 12 sprints (critères go/no-go)

➡️ **Prochaine** : SECTION B — Architecture appliquée (comment structure se traduit en code)
