Voici **ADR‑01**, rédigé proprement selon le format MADR, prêt à être copié dans :  
`/docs/adr/adr-01-architecture-globale.md`

Aucune recherche externe n’est nécessaire : ceci relève d’un design interne à ton projet.

***

# 📘 **ADR‑01 — Choix de l’Architecture Globale du Projet NovaCRM + AI Compliance Hub**

*Status : Accepted*  
*Date : 2026‑01‑27*  
*Supersedes : Aucun*  
*Auteur : René / NovaCRM Core Team*

***

# 1. 🎯 Contexte

NovaCRM + AI Compliance Hub est un système composé de deux domaines fonctionnels principaux :

1.  **NovaCRM** → Application CRM moderne (gestion clients, utilisateurs, équipes, interactions).
2.  **AI Compliance Hub** → Moteur d’inspection, gouvernance, analyse des prompts et reporting de conformité IA.

Ces deux blocs doivent :

*   **évoluer indépendamment**,
*   permettre **itération rapide**,
*   supporter **intégrations tierces** (Teams, M365, API internes),
*   garantir **maintenabilité**,
*   offrir une **cloison technique** entre les responsabilités (SoC),
*   être prêts pour un futur découpage micro‑services si nécessaire.

Sans une architecture modulaire, le projet risquerait rapidement de devenir un monolithe rigide, difficile à tester, et presque impossible à faire évoluer sans régression — surtout dans les zones sensibles liées à la conformité IA.

***

# 2. 💡 Décision

Nous adoptons une **architecture modulaire orientée services**, structurée autour de **trois blocs principaux**, chacun isolé dans son propre répertoire :

    /backend            → API REST (FastAPI)
    /frontend           → Interface web (Next.js)
    /ai                 → Moteur IA (policies, règles, scanners)

Ces trois modules communiquent via :

*   **HTTP/REST** (API du backend utilisée par le frontend),
*   **Appels internes Python** (backend → ai),
*   **Connecteurs futurs** (Kafka / queues / events si nécessaire).

### En résumé, l’architecture suit :

⚙ **Backend = cœur métier**  
🎨 **Frontend = presentation layer**  
🧠 **Compliance Engine = moteur expert isolé**

Cette architecture est volontairement **simple, modulaire, évolutive** :  
elle respecte SoC, KISS, SOLID, DRY et prépare le terrain pour la scalabilité.

***

# 3. 🧭 Options Envisagées

## **Option A — Monolithe complet (backend + compliance dans un seul module)**

❌ Couplage très fort entre CRM et conformité IA  
❌ Difficulté d’évolution de la partie AI (nouveaux scanners, règles…)  
❌ Risque de dette technique accélérée  
❌ Tests plus complexes  
❌ Impossible de substituer le moteur IA indépendamment

## **Option B — Micro‑services dès le départ**

❌ Sur‑ingénierie (YAGNI)  
❌ Besoin de DevOps plus lourd (Docker, orchestration, queues, observabilité)  
❌ Tuning, monitoring, coûts  
❌ Complexité inutile pour un MVP

## **✔ Option C — Architecture modulaire orientée services (structuration interne)**

✔ Code organisé par responsabilités (SoC)  
✔ Backend léger → API FastAPI  
✔ Compliance Engine isolé → plug & play  
✔ Pas de sur‑complexité DevOps  
✔ Compatible future migration micro‑services  
✔ Testabilité accrue (unit tests séparés, mocks, scanners isolés)  
✔ Intégration claire avec le frontend Next.js via REST

***

# 4. 📌 Décision Finale

Nous adoptons **Option C** :  
➡ une architecture **3 modules** : backend, frontend, ai.  
➡ communication **simple**, **testable**, **faiblement couplée** (REST + appels internes).  
➡ extensible vers du micro‑service uniquement si la charge l’exige.

L’objectif : **construire vite, rester propre, ne pas sur‑architecturer**.

***

# 5. 🧱 Conséquences

### ✔ Conséquences Positives

*   Séparation claire du domaine CRM et du domaine Compliance IA
*   Tests unitaires propres (moteur IA testable sans lancer l’API)
*   Possibilité de faire évoluer le moteur IA vers un service dédié plus tard
*   Développement parallèle possible (backend team / IA team / frontend team)
*   Frontend découplé → Next.js peut évoluer librement
*   Support naturel des pipelines CI/CD modulaires

### ❌ Conséquences Négatives

*   Légère duplication de certains modèles (DTO backend vs models internes compliance)
*   Quelques couches d’adaptation sont nécessaires (Adapter/Factory)
*   Plus de dossiers → structure plus “granulaire” à expliquer aux nouveaux entrants

***

# 6. 📁 Arborescence retenue

    novaCRM/
    ├── backend/             → API FastAPI + Domain CRM
    │   ├── core/
    │   └── infrastructure/
    ├── frontend/            → Next.js (UI/UX)
    │   └── app/
    ├── ai/                  → Moteur IA (policies + pipelines)
    │   ├── detectors/
    │   ├── pipelines/
    │   └── policies/
    ├── docs/
    │   ├── adr/
    │   └── architecture/
    └── infra/
        ├── k8s/
        └── terraform/

***

# 7. 🔗 Liens

*   ADR‑00 — Mise en place du système d’ADR
*   Stack technique : `/docs/architecture/stack.md`
*   Politique IA : `/AI-RULES.md`

***


