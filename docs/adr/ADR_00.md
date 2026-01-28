Voici **ADR‑00** rédigé proprement, prêt à être copié-collé dans ton dépôt GitHub (dans `docs/adr/adr-00.md`).  
J’utilise la structure standard **MADR** (Modern ADR), claire, lisible, et adaptée au contexte NovaCRM + AI Compliance Hub.

***

# 📘 **ADR‑00 — Choix d’un Système d’ADR pour la Documentation d’Architecture**

*Status : Accepted*  
*Date : 2026‑01‑27*  
*Décision : Fondation du registre ADR du projet NovaCRM + AI Compliance Hub*

***

## 1. 🎯 Contexte

Le projet **NovaCRM + AI Compliance Hub** est un système modulaire combinant :

*   un backend FastAPI,
*   un frontend Next.js,
*   un moteur AI Compliance,
*   des scripts et pipelines DevOps,
*   une architecture évolutive orientée services.

Comme tout projet destiné à évoluer (fonctionnalités CRM, moteur de règles d’IA, gouvernance, intégrations API, etc.), nous avons besoin :

*   d’un **historique clair des décisions techniques**,
*   d’une **vision transparente pour l'équipe**,
*   d’une **trace écrite permettant d’expliquer les compromis** (trade‑offs),
*   d’un **cadre reproductible** pour toutes les futures décisions.

Sans un système de décision structuré, les choix s’égarent, se mélangent dans les commits, et la dette technique s’accumule silencieusement.

***

## 2. 💡 Décision

Nous adoptons un **système d’ADR (Architecture Decision Records)** basé sur le format **MADR 3.x**, stocké dans :

    /docs/adr/

Chaque décision sera enregistrée dans un fichier séparé suivant la convention :

    adr-XX-[nom-de-la-decision].md

Exemples :

*   `adr-01-choix-du-framework-backend.md`
*   `adr-02-architecture-des-modules-compliance.md`
*   `adr-03-storage-et-base-de-donnees.md`

Le présent document constitue **ADR‑00**, servant de fondation et de référence.

***

## 3. 🧭 Options envisagées

### **Option A — Aucune documentation de décision**

❌ Trop risqué pour un projet multi‑modules  
❌ Aucune traçabilité  
❌ Conflits entre développeurs  
❌ Mauvaise transférabilité / onboarding

### **Option B — Documentation dispersée dans le wiki ou Notion**

❌ Risque de perte d'information  
❌ Surcoût de maintenance  
❌ Pas versionné avec le code source  
❌ Pas adapté au workflow Git

### **✔ Option C — Utiliser des ADR versionnés avec le code (MADR)**

✔ Réside dans le repo, versionné via Git  
✔ Standard reconnu en entreprise & en DevOps  
✔ Format simple pour les PR  
✔ Permet de revenir sur une décision (via superseding ADR)  
✔ Compatible GitHub, GitLab, Azure DevOps  
✔ Excellente base pour auditer les choix techniques

***

## 4. 📌 Décision finale

Nous retenons **Option C : Utiliser ADR + format MADR**.

Toutes les futures décisions structurantes du projet **doivent** être documentées comme ADR, notamment :

*   choix techniques majeurs (framework, library critique, architecture),
*   choix de sécurité ou conformité,
*   décisions impactant la scalabilité ou la maintenance,
*   adoption de nouveaux services (queue, cache, DB, observabilité…),
*   organisation des modules (CRM, Rules Engine, Ingestion…).

***

## 5. 🧱 Conséquences

### **Conséquences positives**

*   Documentation propre, partagée, durable
*   Réduction des désaccords techniques
*   Facilite onboarding + maintien de la cohérence
*   Support des audits internes (IA compliance, sécurité)
*   Historique clair des migrations et évolutions

### **Conséquences négatives**

*   Légère charge d’écriture supplémentaire
*   Nécessite de la discipline d’équipe
*   Peut ralentir une décision si mal géré (à éviter)

***

## 6. 📄 Gabarit ADR standard (MADR)

Un fichier ADR suivra la structure :

```markdown
# ADR-XX — [Titre de la décision]

*Status : Proposed | Accepted | Deprecated | Superseded*
*Date : YYYY-MM-DD*

## Contexte
[Pourquoi cette décision doit exister]

## Décision
[La décision prise]

## Options envisagées
[A, B, C...]

## Conséquences
[Impacts positifs / négatifs]

## Liens
[Docs, PR, références...]
```

***

## 7. 🔗 Liens

*   Répertoire ADR du projet : `/docs/adr/`
*   Format MADR officiel : <https://adr.github.io/madr/>
*   Modèle GitHub : <https://github.com/joelparkerhenderson/architecture_decision_record>

***

# 🎉 ADR‑00 est prêt.

Souhaites‑tu que je génère maintenant :

### 🔨 **ADR‑01 — Choix de l’architecture globale du projet (backend / frontend / moteur IA)**

ou

### 🧱 **ADR‑02 — Choix de FastAPI pour le backend**

ou

### 🧠 **ADR‑03 — Séparation du moteur IA et du CRM (SoC)** ?

Dis‑moi lequel tu veux rédiger en priorité.
