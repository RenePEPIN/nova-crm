
Il définit le **cadre d’usage IA**, les **règles applicables**, les **niveaux de risque**, les **mécanismes d’enforcement**, la **collecte d’audit**, et des **exemples concrets** (y compris des snippets utilisables dans `ai/` et côté Front).

> 🎯 Objectif : un document **opérationnel** (pas seulement juridique) que l’équipe peut réellement suivre et que le moteur applique.

***

# 🧠 AIrules — Politique & Règles d’Usage de l’IA

**Projet** : NovaCRM + AI Compliance Hub  
**Propriétaire** : Product & Security (NovaCRM Core Team)  
**Audience** : Développeurs, Ops, Data, Produit, Sec/Compliance  
**Statut** : Draft opérationnel accepté (révisions via PR + ADR)

***

## 1) Périmètre & Définitions

*   **IA Générative** : systèmes (internes/externe) générant ou transformant du texte, du code, des images, des plans d’action.
*   **Prompt** : toute entrée envoyée à un modèle (contexte + instruction + données).
*   **Sortie (Completion)** : toute réponse du modèle.
*   **PII** (Données personnelles) : emails, numéros de téléphone, adresses, IBAN, identifiants uniques, etc.
*   **Secrets** : mots de passe, clés API, tokens OAuth, certificats, clés privées.
*   **Audit Trail** : journal technique attestant des inputs/outputs (redactés), décisions, règles déclenchées, identités, horodatage.

**Environnements visés** :

*   **Dev** (local WSL2), **Test/CI**, **Prod** (SaaS ou On‑prem), **Backoffice** (restreint).

***

## 2) Principes Directeurs

1.  **Privacy by Design** : minimiser, masquer, ou ne pas transmettre de PII/Secrets.
2.  **Least Privilege** : l’IA n’accède qu’au strict nécessaire.
3.  **Explainability** : toutes les décisions IA **doivent** être auditables (rule → finding → action).
4.  **SoC** : le **Compliance Engine** contrôle et journalise ; le **Backend** orchestre ; le **Frontend** affiche.
5.  **Fail‑safe** : en cas de doute ou d’erreur d’analyse, **bloquer** et escalader (ne jamais exposer des secrets par défaut).
6.  **KISS/YAGNI** : commencer simple, étendre par **policies** versionnées, non par exceptions ad‑hoc.

***

## 3) Niveaux de Risque & Actions

| Niveau       | Définition                                                                 | Action par défaut                                            | Exemple                                                   |
| ------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------- |
| **Low**      | Aucune PII/Secret, contexte non sensible                                   | Autoriser + Auditer                                          | Reformulation de texte marketing                          |
| **Medium**   | Éléments sensibles possibles mais non critiques                            | Autoriser + Avertir (UI) + Auditer                           | Analyse d’une spec partielle contenant emails « masqués » |
| **High**     | PII/Secret identifié, demande d’export massif, contournement de politiques | **Bloquer** + Motif + Auditer + Notifier                     | « Donne-moi toutes les adresses email clients »           |
| **Critical** | Secret exposé, données réglementées, tentative d’exfiltration              | **Bloquer** + **Escalade** (Sec/Compliance) + Freeze session | Prompt contenant un token de prod                         |

> ℹ️ Les règles ci-dessous mappent à ces niveaux et définissent les **actions**.

***

## 4) Règles (Policies) — Catalogue de Référence

> Les règles sont **déclaratives**, versionnées et activées par **key**.  
> Leur logique d’évaluation est implémentée dans `ai/policies/`.

### 4.1 Règles de Données Sensibles

*   **`no_pii_in_prompts`** : détecte emails, téléphone, IBAN, adresse postale → **High** (bloquer) si trouvé **non masqué**.
*   **`no_secrets_in_prompts`** : détecte tokens, mots de passe, clés privées → **Critical** (bloquer + escalade).
*   **`mask_before_store`** : toute donnée sensible détectée est **masquée** avant stockage audit.

### 4.2 Règles d’Usage & Export

*   **`no_mass_export_requests`** : interdit les demandes type « export tous les emails/numéros ». **High** (bloquer).
*   **`scope_check`** : action limitée au **scope** (compte/équipe/utilisateur). **Medium** (avertir) si ambigu, **High** (bloquer) si hors scope clair.
*   **`no_external_paste`** : interdit coller du contenu classé « interne » vers un outil IA externe non approuvé. **High** (bloquer).

### 4.3 Règles de Sécurité & Conformité

*   **`redact_outputs`** : masquer toute PII dans la **réponse** modèle si non justifiée. **Medium/High** selon contexte.
*   **`traceability_required`** : toutes les requêtes IA **doivent** produire un `auditId`. **High** (bloquer) si échec d’audit.
*   **`policy_version_pin`** : exécuter les policies **par version** (pinned) pour reproductibilité.

***

## 5) Enforcement — Comment ces règles s’appliquent

*   **À l’entrée** (pre‑prompt) : le Compliance Engine **scanne** & **classe** (Strategy).
*   **Décision** : en fonction des findings → **authorize / warn / block / escalate**.
*   **À la sortie** (post‑completion) : application de `redact_outputs` si nécessaire.
*   **Audit** : toujours écrire une entrée (avec masquage), y compris pour les **bloquages**.

> **Point de contrôle unique** : `backend/infrastructure/http/compliance_adapter.py`  
> Si l’adapter échoue → **bloquer** (fail‑safe) + log critique.

***

## 6) Journalisation & Audit Trail

*   **Champs minimum** : `auditId`, `timestamp`, `actor.userId`, `actor.orgId`, `source` (web, api, cli), `ruleset`, `risk`, `findings[]`, `action` (allow/warn/block/escalate), `redactions[]`.
*   **Stockage** : fichier append‑only (dev), table dédiée (prod).
*   **PII/Secrets** : **jamais** stockés en clair ; masque (`***` ou hash) + type (`email`, `token`).
*   **Conservation** : configurable (ex. 180 jours dev/test, 365/720 jours prod selon politique).

***

## 7) Exemples de Configuration (YAML Policies)

> Exemple à placer dans `ai/policies/policy_set.yaml`

```yaml
rules:
  - key: no_pii_in_prompts
    level: high
    action: block
    params:
      patterns:
        email: "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}\\b"
        phone: "\\b(\\+\\d{1,3}[- ]?)?\\d{9,}\\b"
        iban: "\\b[A-Z]{2}\\d{2}[A-Z0-9]{1,30}\\b"
  - key: no_secrets_in_prompts
    level: critical
    action: escalate
    params:
      patterns:
        token_like: "(?i)(api[ _-]?key|secret|token|passwd|password)"
  - key: no_mass_export_requests
    level: high
    action: block
    params:
      phrases:
        - "tous les emails"
        - "toutes les adresses"
        - "export complet"
  - key: scope_check
    level: medium
    action: warn
    params:
      require_org_scope: true
  - key: redact_outputs
    level: medium
    action: allow
    params:
      pii_types: ["email", "phone", "iban"]
  - key: traceability_required
    level: high
    action: block
    params:
      require_audit_id: true
```

***

## 8) Snippets d’Implémentation (Python & Front)

### 8.1 Python — Interface d’évaluation (Strategy)

`ai/pipelines/interface.py`

```python
from typing import Protocol, List, Dict, Any

class Rule(Protocol):
    key: str
    level: str  # "low" | "medium" | "high" | "critical"

    def evaluate(self, prompt: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Retourne une liste de findings: {type, message, span, pii?, secret?}"""
        ...
```

`ai/pipelines/engine.py`

```python
import re
from typing import Dict, Any, List

class Engine:
    def __init__(self, rules: List):
        self.rules = rules

    def analyze(self, prompt: str, ctx: Dict[str, Any]) -> Dict[str, Any]:
        findings: List[Dict[str, Any]] = []
        for rule in self.rules:
            findings.extend(rule.evaluate(prompt, ctx))

        risk = self._aggregate_risk(findings)
        action = self._decide_action(findings, ctx.get("policy", {}))
        redactions = self._redactions(prompt, findings)
        return {"risk": risk, "findings": findings, "action": action, "redactions": redactions}

    def _aggregate_risk(self, findings):
        order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        lvl = max([order.get(f.get("level","low"),1) for f in findings], default=1)
        rev = {v:k for k,v in order.items()}
        return rev[lvl]

    def _decide_action(self, findings, policy):
        highest = self._aggregate_risk(findings)
        if highest in ("high","critical"):
            # Bloque par défaut, peut escalader selon policy
            return "escalate" if highest == "critical" else "block"
        return "warn" if findings else "allow"

    def _redactions(self, prompt, findings):
        # Exemple minimal : retourne des spans à masquer
        spans = []
        for f in findings:
            if f.get("pii") or f.get("secret"):
                spans.append({"start": f.get("start", 0), "end": f.get("end", 0), "type": f.get("type")})
        return spans
```

`ai/policies/no_pii_in_prompts.py`

```python
import re
from typing import Dict, Any, List

class NoPiiRule:
    key = "no_pii_in_prompts"
    level = "high"

    def __init__(self, patterns: Dict[str, str]):
        self.patterns = {k: re.compile(v) for k, v in patterns.items()}

    def evaluate(self, prompt: str, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        findings = []
        for ptype, rx in self.patterns.items():
            for m in rx.finditer(prompt):
                findings.append({
                    "rule": self.key, "level": self.level,
                    "type": ptype, "message": f"PII détectée: {ptype}",
                    "start": m.start(), "end": m.end(), "pii": True
                })
        return findings
```

### 8.2 Backend — Adapter unique (fail‑safe)

`backend/infrastructure/http/compliance_adapter.py`

```python
from typing import Dict, Any
from ai.pipelines.engine import Engine
from ai.policies.no_pii_in_prompts import NoPiiRule

ENGINE = Engine(rules=[NoPiiRule(patterns={
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
})])

def analyze(prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
    # Fail-safe : si erreur, bloquer et auditer
    try:
        result = ENGINE.analyze(prompt, context)
        return result
    except Exception as e:
        return {"risk": "high", "findings": [{"rule":"adapter_error","level":"high","message":str(e)}], "action":"block"}
```

### 8.3 Frontend — Affichage clair des avertissements

`frontend/lib/compliance.ts`

```ts
export type ComplianceResult = {
  risk: "low"|"medium"|"high"|"critical";
  action: "allow"|"warn"|"block"|"escalate";
  findings: { rule: string; level: string; message: string }[];
  redactions?: { start: number; end: number; type: string }[];
};

export function shouldBlock(c: ComplianceResult) {
  return c.action === "block" || c.action === "escalate";
}
```

`frontend/components/ComplianceBanner.tsx`

```tsx
import { ComplianceResult, shouldBlock } from "@/lib/compliance";

export default function ComplianceBanner({ c }: { c: ComplianceResult }) {
  if (!c || c.action === "allow") return null;
  const color = shouldBlock(c) ? "bg-red-100 text-red-800" : "bg-yellow-100 text-yellow-800";
  const label = shouldBlock(c) ? "Action bloquée" : "Attention requise";

  return (
    <div className={`p-3 rounded border ${color}`}>
      <strong>{label}</strong>
      <ul className="list-disc pl-6 mt-1">
        {c.findings.map((f, i) => (
          <li key={i}>{f.message} <em>({f.rule})</em></li>
        ))}
      </ul>
    </div>
  );
}
```

***

## 9) Cas d’Usage — Bonnes & Mauvaises Pratiques

**❌ Mauvais :**

> « Donne‑moi la liste complète des emails de tous les clients *avec domaines* »  
> → `no_mass_export_requests` = **High** → **block**

**✅ Bon :**

> « Résume la politique de confidentialité *sans* inclure de données personnelles »  
> → `risk: low`, `action: allow`, `auditId` créé, sortie non sensible.

***

## 10) Gouvernance & Rôles

*   **Owner** : Product + Security
*   **Maintainers** : Core Team Backend + Compliance
*   **Contributions** : via PR + **ADR** si nouvelle catégorie de règle
*   **Versionnement des policies** : pin par `policy_version_pin`
*   **Revue sécurité** : trimestrielle (ou ad‑hoc lors d’incident)

***

## 11) Incident Response (extrait)

1.  **Détection** : `critical` ou `high` répétés → alerte Slack/Teams (futur Observer).
2.  **Containment** : freeze session utilisateur (si applicable), blocage règles.
3.  **Forensics** : extraction audit (redacté), timeline, règles déclenchées.
4.  **Remédiation** : durcir patterns, ajouter tests, communiquer.
5.  **Leçons** : mise à jour AIrules + ADR si changement structurel.

***

## 12) Conformité & DPIA (note)

*   **PII** : minimisation, masquage systématique, rétention limitée.
*   **Traçabilité** : audit complet, reproductible, horodaté.
*   **Évaluation d’impact** (DPIA) : à tenir à jour lors d’évolutions majeures du moteur/périmètre.

***

## 13) Checklist d’Intégration (Definition of Done)

*   [ ] `traceability_required` actif (génère `auditId` par requête IA)
*   [ ] `no_pii_in_prompts` & `no_secrets_in_prompts` actifs
*   [ ] Actions **block**/**escalate** testées (unit + intégration)
*   [ ] Redaction PII **pré‑stockage** (logs/audit)
*   [ ] Bannière d’avertissement visible côté Front quand `warn/block/escalate`
*   [ ] Taskfile : tâches `test-backend`, `lint-backend`, `fmt-backend` OK

***

## 14) Évolution

Les changements significatifs (nouvelle catégorie de risques, changement d’actions par défaut, ajout d’un provider IA externe) **doivent** passer par un **ADR** dédié et une PR sur ce fichier.

***

## 15) Références & Alignement Docs

Ce document est aligné avec :

- `README` (vision produit & architecture globale)
- `docs/architecture/stack.md` (stack technique figée)
- `docs/adr/ADR‑01 — Choix de l’Architecture Globale du Projet NovaCRM + AI Compliance Hub.md`
- `docs/adr/ADR‑03 — Stack Technique.md`

En cas de divergence, **mettre à jour ce fichier et/ou créer une ADR**.

***

**Fin du document — AIrules.md**

