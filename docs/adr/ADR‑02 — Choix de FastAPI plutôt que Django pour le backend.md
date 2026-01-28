# 📘 ADR‑02 — Choix de **FastAPI** plutôt que **Django** pour le backend

*Status : Accepted*  
*Date : 2026‑01‑26*  
*Auteur : René / NovaCRM Core Team*  
*Supersedes : —*  
*Relates to : ADR‑01 (Architecture globale), ADR‑00 (Système d’ADR)*

***

## 1) 🎯 Contexte

Le projet **NovaCRM + AI Compliance Hub** adopte une architecture **API‑first** et **modulaire** (cf. ADR‑01), avec trois blocs :

*   **Backend** (API REST)
*   **Compliance Engine** (moteur IA de règles et scanners)
*   **Frontend** (Next.js)

Contraintes clés :

*   **SoC fort** : isoler clairement l’API CRM et le moteur IA.
*   **Async/performances** : le moteur d’analyse peut effectuer des tâches I/O bound (lecture logs, inspection prompts, intégrations).
*   **Type‑safety & DX** : modèles typés, DTO clairs, génération automatique d’OpenAPI/Swagger.
*   **Time‑to‑value** : MVP rapide, code simple, lisible, testable.
*   **Évolutivité** : capacité à externaliser plus tard le moteur IA (service séparé), sans tout casser.

***

## 2) 🧭 Options envisagées

### Option A — **Django monolithique** (Django “pur” : ORM, templates, admin)

*   **Avantages :** batteries‑incluses (ORM, admin, auth), écosystème mature, communauté massive.
*   **Inconvénients :** orientation monolithique, couplage fort, async non natif historique, sur‑ingénierie pour un **API‑first** léger, friction pour isoler un moteur IA indépendant.

### Option B — **Django + DRF** (Django REST Framework)

*   **Avantages :** outillage REST robuste, sérialisation puissante, permissions fines, admin natif.
*   **Inconvénients :** verbosité, couches multiples (models/serializers/viewsets/permissions), surcoûts de maintenance pour un MVP, async et perfs en retrait vs une stack ASGI native, risque de glisser vers un monolithe malgré l’intention modulaire.

### ✔ Option C — **FastAPI** (ASGI, Pydantic, Starlette, Uvicorn)

*   **Avantages :** async natif, **OpenAPI auto**, Pydantic v2 (validation/typage), performance, surface API minimale (peu de boilerplate), excellente **DX**, naturel pour **API‑first** et services modulaires, s’intègre facilement à un moteur Python pur (Compliance Engine).
*   **Inconvénients :** pas de “batteries‑incluses” type Django admin par défaut, choix des briques (auth, ORM) à composer, besoin d’un minimum de conventions d’équipe.

*(Écartées rapidement : Flask/Quart/Fastify côté Python/JS — non retenues pour alignement stack, support typing, et cohérence avec l’existant.)*

***

## 3) ✅ Décision

Nous **choisissons FastAPI** pour le backend NovaCRM.

Piliers de mise en œuvre :

*   **Serveur** : FastAPI (ASGI) + Uvicorn.
*   **Modèles & validation** : Pydantic v2.
*   **ORM** : SQLAlchemy (+ Alembic pour migrations) — MVP en SQLite, v1 en Postgres.
*   **Auth** : stack composable (FastAPI Users / JWT / OAuth2), RBAC basique au départ.
*   **Contrats** : OpenAPI auto, documentation Swagger/UI livrée d’office.
*   **Adapter** : couche d’adaptation Backend → Compliance Engine (appel local Python, service réseau plus tard si besoin).

***

## 4) 🔍 Justification (critères de décision)

1.  **Architecture & SoC**  
    FastAPI facilite une architecture **service‑based** claire (routers/ services/ adapters) et **isole naturellement** le Compliance Engine en module Python, sans forcer l’intégration dans un cadre d’app “Django”.  
    → Réduction du couplage, **meilleure testabilité**, migration simple vers un service réseau ultérieur.

2.  **Async & performances**  
    **ASGI natif** et gestion asynchrone simplifiée (I/O réseau, scans) pour absorber des appels au moteur IA, des lectures de logs, etc.  
    → **Latence plus faible**, **débit supérieur** qu’un stack WSGI/DRF classique pour ce cas d’usage.

3.  **DX (Developer Experience) & typage**  
    **Pydantic** offre des DTO/validators typés très lisibles, et **la doc OpenAPI est générée automatiquement**.  
    → Onboarding plus rapide, **contrats d’API stables**, génération de types TS côté front si souhaité.

4.  **API‑first & clarté**  
    Le projet est **d’abord une API** consommée par un front Next.js et potentiellement des intégrations (Teams/M365).  
    → FastAPI fournit **exactement** ce dont on a besoin, **sans couche web serveur‑side** inutile (templates, forms).

5.  **Évolutivité & micro‑services futurs**  
    La communication Backend ↔ Compliance Engine peut passer d’un **appel local** à **REST/gRPC** (service séparé) **sans refonte** de l’API publique.  
    → Préparation naturelle à la **scalabilité** (file/queue, workers).

6.  **Simplicité (KISS/YAGNI)**  
    Django/DRF serait **sur‑dimensionné** pour le MVP.  
    → Avec FastAPI, on **garde la stack minimale** et on ajoute au besoin (auth avancée, admin dédié, etc.).

***

## 5) ⚠️ Risques & mitigations

### R1 — **Pas de “Django Admin” out‑of‑the‑box**

*   *Risque* : besoin d’un back‑office rapide pour l’opérationnel.
*   *Mitigation* :
    *   Court terme : **pages d’admin** simples dans le Frontend (rôles RBAC),
    *   Ou adoption d’un **admin léger** (ex. *fastapi‑admin* / générateurs UI),
    *   Ou **outil externe low‑code** (Appsmith/Retool) pour opérations internes.

### R2 — **Auth/permissions à composer**

*   *Risque* : réinventer des briques de sécurité.
*   *Mitigation* :
    *   Utiliser **FastAPI Users** / OAuth2 / JWT éprouvés,
    *   **RBAC** simple dès le MVP,
    *   **ADR Sécurité** dédié pour conventions (hash, tokens, scopes).

### R3 — **Choix de l’ORM et des conventions**

*   *Risque* : divergence de styles, verbosité SQLAlchemy si mal cadré.
*   *Mitigation* :
    *   Conventions **repo/service** définies,
    *   **Alembic** pour migrations,
    *   Gabarits de “service + repo + schema” fournissant un **chemin standard**.

### R4 — **Courbe d’apprentissage si l’équipe est très Django‑native**

*   *Risque* : perte de productivité initiale.
*   *Mitigation* :
    *   **Guides internes** (README/How‑to),
    *   **Exemples** de routers, services, tests,
    *   Pairing & revues ciblées au début.

***

## 6) 🧱 Impacts

### Sur l’architecture

*   Conforte l’**architecture modulaire** (backend / engine / frontend).
*   Simplifie la mise en place de l’**Adapter Backend → Compliance Engine**.

### Sur le développement

*   **Moins de boilerplate** qu’avec DRF, **DX élevée**.
*   **Tests** plus simples (routers/services isolés, mocks engine).

### Sur la roadmap

*   **MVP accéléré** (endpoints, DTO, doc auto).
*   Migration engine → **service dédié** possible sans casser l’API.

### Sur le DevOps

*   **Stack plus légère** : Uvicorn + FastAPI, pas de dépendance à l’écosystème Django.
*   Conteneurisation simple (images plus petites, démarrage rapide).

### Sur la conformité & l’audit

*   **OpenAPI auto** = contrat d’API versionnable/auditable.
*   Facilité à exposer **health/metrics** et journaux structurés.

***

## 7) ✍️ Règles d’implémentation (exécutables)

*   Les endpoints résident dans `backend/api/*` (routers par domaine, **/api/v1/**).
*   Les **DTO Pydantic** vivent dans `backend/api/schemas_*` (lecture seule côté front).
*   La logique métier est dans `backend/app/services/*`.
*   L’accès persistance dans `backend/app/repositories/*` (**SQLAlchemy + Alembic**).
*   L’**Adapter** vers le moteur IA est dans `backend/app/adapters/compliance_adapter.py`.
*   Les tests unitaires ciblent chaque couche séparément (`backend/tests/*`).
*   **Taskfile** pilote `install`, `backend`, `test-backend`, `lint-backend`, `fmt-backend`.

***

## 8) 🔗 Suivis & tâches

*   Rédiger **ADR Sécurité** (auth, tokens, RBAC, CORS, secrets).
*   Rédiger **ADR Persistance** (SQLite → Postgres, schéma, migrations).
*   Implémenter **l’Adapter Engine** (interface + impl. locale).
*   Ajouter **exemples de Strategy/Factory** dans `compliance_engine/`.
*   Générer/valider **types TS** depuis OpenAPI (si choisi).

***

## 9) 📎 Annexes (références internes)

*   ADR‑01 — Architecture globale
*   README — Architecture & Principes (SOLID, SoC, KISS/YAGNI, DRY)
*   Taskfile — cibles `install`, `backend`, `dev`, `test-backend`

***

**Décision entérinée** : FastAPI devient le framework backend pour NovaCRM + AI Compliance Hub.  
Cette décision sera **révisitable** si :

*   la charge nécessite une séparation forte des services dès le court terme,
*   un besoin d’**admin très avancé** émerge (et l’admin front ne suffit plus),
*   une contrainte d’entreprise impose un cadre différent.
