# 🤖 SECTION D : AI Compliance Engine

**Durée estimée** : 12-15 heures  
**Prérequis** : SECTION A (contexte), SECTION B (architecture), SECTION C (FastAPI)  
**Objectif** : Comprendre et implémenter le moteur IA qui détecte et maîtrise les risques de conformité

**⚠️ IMPORTANCE CRITIQUE** : 
- Engine = 25% du projet NovaCRM
- S1 go/no-go dépend de l'audit trail immuable (Engine core)
- PII detection = GDPR compliance (fondation légale)

---

## 🤖 LEÇON 1 : Concepts Fondamentaux du Moteur IA

### 📍 Le Concept (Théorie)

**AI Compliance Engine** = Système qui analyse du texte/données pour détecter risques de conformité.

**Architecture générale** :

```
INPUT (texte, données)
  ↓
[Detector 1: PII]        ← Cherche emails, phones, IBANs
[Detector 2: Secrets]    ← Cherche API keys, tokens
[Detector 3: Scope]      ← Cherche données hors-périmètre
  ↓
FINDINGS (détections, sévérité, positions)
  ↓
[Masking]         ← Redacte PII (sophi*@**mple.com)
[Audit Trail]     ← Enregistre qui a vu quoi, quand
  ↓
OUTPUT (données masquées, audit record)
```

**Analogie concrète** : Scanner d'aéroport

```
❌ SANS Engine (douane manuelle) :
  Douanier lit chaque bagage → "Ah, cette valise contient une bombe?"
  → Lent, erreurs humaines, couteux

✅ AVEC Engine (scanner automatisé) :
  Scanner RX → détecte métaux, explosifs
  → Rapide, précis, reproductible
  → Enregistre "Valise 123 scannée à 10:15, nothing found"
```

**Composants clés** :

| Composant | Rôle | Exemple |
|-----------|------|---------|
| **Detector** | Classe qui détecte un risque spécifique | PiiDetector, SecretsDetector |
| **Rule** | Nomination d'une détection | "no_pii_in_prompts", "no_api_keys" |
| **Policy** | Ensemble de rules déclaratives (YAML) | compliance_policy_v1.yaml = [no_pii, no_secrets] |
| **Pipeline** | Orchestration : exécute détecteurs, masque, audit | CompliancePipeline |
| **Audit Trail** | Log immuable : qui a vu quoi, quand | append-only database |

**Cycle de vie d'une analyse** :

```
1. Input : "My email is sophie@example.com and IBAN is FR76..."
2. Load policy : "Apply no_pii + no_secrets rules"
3. Run detectors :
   - PiiDetector finds : [email=sophie@example.com, iban=FR76...]
   - SecretsDetector finds : nothing
4. Mask : "My email is sophi*@**mple.com and IBAN is FR76xxxxx"
5. Audit : "[2026-01-28 10:15] User:sophie analyzed text, 2 PII found → masked"
6. Output : masked_text + findings + audit_id
```

---

### 🚀 Cas d'usage Réel (NovaCRM + AI Hub)

**Scénario 1 : Contact creation (S1-S2)**

```
Frontend user types: "Sophie Martin, sophie@example.com, IBAN FR76123456"

POST /api/v1/contacts {
  name: "Sophie Martin",
  email: "sophie@example.com",
  iban: "FR76123456"
}

Backend receives → calls engine:
  engine.analyze(text="sophie@example.com FR76123456")

Engine pipeline:
  1. PiiDetector finds: email, iban (severity: HIGH)
  2. SecretsDetector finds: nothing
  3. Mask: email="sophi*@**mple.com", iban="FR76xxxxxx"
  4. Audit: "[2026-01-28 10:15:23] actor:sophie action:contact_create contact_id:123 pii_found:2 audit_id:audit_001]"

Backend receives response:
  { 
    pii_found: 2,
    masked_data: {
      email: "sophi*@**mple.com",
      iban: "FR76xxxxxx"
    },
    findings: [
      { type: "email", severity: "HIGH", position: 0 },
      { type: "iban", severity: "HIGH", position: 20 }
    ],
    audit_id: "audit_001"
  }

Backend stores masked contact + audit record
Response to frontend: masked data only
```

**Scénario 2 : Scope check (S5-S6 RBAC)**

```
User Sophie (analyst, scope=contacts_only) tries to view Client record.

GET /api/v1/clients/456

Backend checks RBAC:
  1. Role: analyst → scope: contacts_only
  2. Resource: clients → requires scope: clients
  3. Call engine: engine.scope_check(user_scope="contacts_only", resource="clients")

Engine detector (ScopeDetector):
  scope_found_violation: true
  severity: CRITICAL (RBAC bypass risk!)

Backend:
  - Returns 403 Forbidden
  - Logs audit: "[2026-01-28 10:15:50] actor:sophie action:unauthorized_access resource:clients audit_id:audit_002]"
  - Alert: RBAC violation detected, escalate to admin
```

**Scénario 3 : LLM prompt masking (future, S9-S10)**

```
User wants AI assistant to summarize contact Sophie Martin's data.

Prompt: "Summarize this contact: sophie@example.com, IBAN FR76..."

Backend calls engine before sending to LLM:
  engine.analyze_prompt(prompt)

Engine:
  1. PiiDetector: finds email, iban
  2. Mask: "Summarize this contact: sophi*@**mple.com, IBAN FR76xxxxx"
  3. Return masked_prompt

Backend sends masked_prompt to LLM (not original)
LLM never sees real PII
```

**Why Engine = critical for NovaCRM**:
- ✅ **Compliance** : PII protection (GDPR, IA Act)
- ✅ **Audit** : Immuable trail (legal defense: "we logged everything")
- ✅ **Safety** : LLM doesn't leak PII
- ✅ **Control** : RBAC violations detected + blocked

---

### 💻 Le Lab Pratique — Structure du Moteur

#### **LAB 3.1 : Explorez la structure réelle du moteur**

```bash
# Terminal WSL2
cd /home/renep/dev/nova-crm/ai

# Listez la structure
tree -L 3 -I '__pycache__|*.pyc'

# Vous devez voir (ou créer):
# ai/
# ├─ __init__.py
# │
# ├─ detectors/                        ← Implémentations des détecteurs
# │  ├─ __init__.py
# │  ├─ base.py                        ← Abstract base class (interface)
# │  ├─ pii_detector.py                ← Détecteur PII (emails, phones, IBANs)
# │  ├─ secrets_detector.py            ← Détecteur secrets (API keys, tokens)
# │  ├─ scope_detector.py              ← Détecteur scope (RBAC violations)
# │  └─ test_*.py                      ← Tests pour chaque détecteur
# │
# ├─ pipelines/                        ← Orchestration
# │  ├─ __init__.py
# │  ├─ compliance_pipeline.py         ← Main orchestrator
# │  ├─ masking.py                     ← Masking logic
# │  ├─ factories.py                   ← Factory pour créer détecteurs
# │  └─ test_*.py                      ← Tests
# │
# ├─ policies/                         ← Déclaration rules (data-driven)
# │  ├─ compliance_policy_v1.yaml      ← Policy v1: [no_pii, no_secrets, scope_check]
# │  ├─ compliance_policy_v2.yaml      ← Policy v2: [no_pii, no_secrets, scope_check, no_tokens]
# │  └─ schema.json                    ← JSON schema pour valider policies
# │
# ├─ models/                           ← Data models (Pydantic)
# │  ├─ __init__.py
# │  ├─ detection.py                   ← DetectionResult, Finding, etc
# │  └─ policy.py                      ← PolicyConfig, etc
# │
# ├─ main.py ou server.py              ← Entry point (CLI ou FastAPI server)
# └─ requirements.txt                  ← Dependencies (pydantic, pyyaml, regex, etc)

echo "✅ Structure engine reviewed"
```

**Explications** :

| Folder | Role | Change trigger |
|--------|------|-----------------|
| `detectors/` | Implémentations concrètes de détections | Nouvelle loi (add SS# detector) |
| `pipelines/` | Orchestration (run all detectors, mask, audit) | Nouveau stage (add redaction) |
| `policies/` | Configuration déclarative (YAML) | Changement règles métier (disable no_pii?) |
| `models/` | Types Pydantic (contract) | Changement schema réponse |

---

## 🤖 LEÇON 2 : Strategy Pattern — Detectors Pluggables

### 📍 Le Concept (Théorie)

**Strategy Pattern** = Interface commune pour comportements interchangeables.

**En 3 étapes** :

```python
# 1️⃣ INTERFACE (contrat)
class Detector(ABC):
    @abstractmethod
    def detect(self, text: str) -> DetectionResult:
        """Detect violations. Return findings."""
        pass

# 2️⃣ IMPLÉMENTATIONS CONCRÈTES (stratégies)
class PiiDetector(Detector):
    def detect(self, text: str) -> DetectionResult:
        # PII detection logic
        pass

class SecretsDetector(Detector):
    def detect(self, text: str) -> DetectionResult:
        # Secrets detection logic
        pass

# 3️⃣ UTILISATION POLYMORPHE (pas de if/else hardcoded)
detectors: List[Detector] = [PiiDetector(), SecretsDetector()]
for detector in detectors:
    result = detector.detect(text)  # Polymorphism: runs correct implementation
```

**Avantage** : Ajouter nouveau détecteur = **zéro changement pipeline**.

---

### 🚀 Cas d'usage Réel — Implémentation Détecteur PII

**Fichier** : `ai/detectors/base.py`

```python
"""
Base detector interface (abstract).

All detectors inherit from this.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum

# ===== ENUMS =====

class Severity(Enum):
    """Risk severity levels."""
    LOW = "low"           # Non-critical (typos, formatting)
    MEDIUM = "medium"     # Moderate risk (scope violation)
    HIGH = "high"         # Serious (PII detected)
    CRITICAL = "critical" # Must block (RBAC bypass, secrets exposed)

# ===== DATA MODELS =====

@dataclass
class Finding:
    """Single detection result."""
    type: str                          # "email", "phone", "iban", etc
    severity: Severity                 # LOW/MEDIUM/HIGH/CRITICAL
    value: str                         # Detected text
    position: int                      # Position in original text
    context: Dict[str, Any] = None     # Extra metadata
    
    def to_dict(self):
        return {
            "type": self.type,
            "severity": self.severity.value,
            "value": self.value,
            "position": self.position,
            "context": self.context or {}
        }

@dataclass
class DetectionResult:
    """Result from one detector."""
    rule_name: str                     # "no_pii_in_prompts", "no_secrets", etc
    passed: bool                       # true = no violations, false = violations found
    findings: List[Finding]            # List of detected issues
    
    def to_dict(self):
        return {
            "rule_name": self.rule_name,
            "passed": self.passed,
            "findings": [f.to_dict() for f in self.findings],
            "count": len(self.findings)
        }

# ===== ABSTRACT BASE CLASS =====

class Detector(ABC):
    """
    Abstract base class for all detectors.
    
    Each detector checks for one specific type of violation.
    Subclasses implement concrete detection logic.
    """
    
    def __init__(self, rule_name: str):
        self.rule_name = rule_name
    
    @abstractmethod
    def detect(self, text: str) -> DetectionResult:
        """
        Detect violations in text.
        
        Args:
            text: Input text to analyze
        
        Returns:
            DetectionResult with findings list
        
        Raises:
            Should not raise exceptions, return findings instead
        """
        pass
    
    def __repr__(self):
        return f"{self.__class__.__name__}(rule={self.rule_name})"
```

**Fichier** : `ai/detectors/pii_detector.py`

```python
"""
PII (Personally Identifiable Information) Detector.

Detects:
- Emails (sophie@example.com)
- Phone numbers (+33 6 12 34 56 78)
- IBANs (FR76 3000 3000 10 xxxxxxxx)
- Social Security numbers (1 87 12 34 567 xxxxxx)
- Credit card numbers (4532xxxxxxxx1234)
"""

import re
from typing import List, Tuple
from detectors.base import Detector, DetectionResult, Finding, Severity

class PiiDetector(Detector):
    """
    Detect PII (Personally Identifiable Information).
    
    Uses regex patterns for common PII formats.
    Future: could use ML models for higher accuracy.
    """
    
    # Regex patterns for PII detection
    PATTERNS = {
        'email': {
            'pattern': r'[\w\.\-+]+@[\w\.\-]+\.\w+',
            'severity': Severity.HIGH,
            'description': 'Email address'
        },
        'phone': {
            'pattern': r'\+?[\d\s\-()]{10,}',  # Matches +33 6 12 34 56 78
            'severity': Severity.HIGH,
            'description': 'Phone number'
        },
        'iban': {
            'pattern': r'[A-Z]{2}[0-9]{2}\s?[A-Z0-9\s]{1,30}',  # IBAN format
            'severity': Severity.HIGH,
            'description': 'IBAN (bank account)'
        },
        'ssn_france': {
            'pattern': r'\b[1-8]\s\d{2}\s\d{2}\s\d{3}\s\d{3}\s\d{2,3}\b',  # French SS#
            'severity': Severity.CRITICAL,
            'description': 'French Social Security Number'
        },
        'credit_card': {
            'pattern': r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
            'severity': Severity.CRITICAL,
            'description': 'Credit card number'
        }
    }
    
    def __init__(self):
        super().__init__(rule_name="no_pii_in_prompts")
    
    def detect(self, text: str) -> DetectionResult:
        """
        Detect PII in text using regex patterns.
        
        Args:
            text: Input text to analyze
        
        Returns:
            DetectionResult with list of PII findings
        """
        findings: List[Finding] = []
        
        # Check each pattern
        for pii_type, config in self.PATTERNS.items():
            pattern = config['pattern']
            severity = config['severity']
            
            # Find all matches
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                finding = Finding(
                    type=pii_type,
                    severity=severity,
                    value=match.group(0),
                    position=match.start(),
                    context={
                        'description': config['description'],
                        'regex_pattern': pattern
                    }
                )
                findings.append(finding)
        
        # Sort by position
        findings.sort(key=lambda f: f.position)
        
        return DetectionResult(
            rule_name=self.rule_name,
            passed=len(findings) == 0,
            findings=findings
        )

# Example usage
if __name__ == "__main__":
    detector = PiiDetector()
    
    test_cases = [
        "Hello world",  # No PII
        "My email is sophie@example.com",  # Email PII
        "Call me at +33 6 12 34 56 78",  # Phone PII
        "IBAN: FR76 3000 3000 10 0123456789",  # IBAN PII
    ]
    
    for text in test_cases:
        result = detector.detect(text)
        print(f"Text: {text}")
        print(f"Result: {result.to_dict()}")
        print()
```

**Fichier** : `ai/detectors/secrets_detector.py`

```python
"""
Secrets Detector.

Detects:
- API keys (bearer tokens, etc)
- AWS keys
- GitHub tokens
- Database URLs (with passwords)
"""

import re
from typing import List
from detectors.base import Detector, DetectionResult, Finding, Severity

class SecretsDetector(Detector):
    """Detect exposed secrets (API keys, tokens, credentials)."""
    
    PATTERNS = {
        'api_key': {
            'pattern': r'(api[_-]?key|apikey|api_token)\s*[:=]\s*["\']?[A-Za-z0-9\-_]{32,}["\']?',
            'severity': Severity.CRITICAL,
            'description': 'API Key exposed'
        },
        'bearer_token': {
            'pattern': r'Bearer\s+[A-Za-z0-9\-_\.]+',
            'severity': Severity.CRITICAL,
            'description': 'Bearer token exposed'
        },
        'github_token': {
            'pattern': r'ghp_[A-Za-z0-9_]{36}',
            'severity': Severity.CRITICAL,
            'description': 'GitHub personal access token'
        },
        'aws_key': {
            'pattern': r'AKIA[0-9A-Z]{16}',
            'severity': Severity.CRITICAL,
            'description': 'AWS Access Key ID'
        },
        'db_url': {
            'pattern': r'(postgresql|mysql|mongodb)://[a-zA-Z0-9_:@./]+',
            'severity': Severity.CRITICAL,
            'description': 'Database connection URL (may contain credentials)'
        }
    }
    
    def __init__(self):
        super().__init__(rule_name="no_api_keys_exposed")
    
    def detect(self, text: str) -> DetectionResult:
        """Detect exposed secrets."""
        findings: List[Finding] = []
        
        for secret_type, config in self.PATTERNS.items():
            pattern = config['pattern']
            severity = config['severity']
            
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                finding = Finding(
                    type=secret_type,
                    severity=severity,
                    value=match.group(0),
                    position=match.start(),
                    context={
                        'description': config['description'],
                        'redacted_value': f"[REDACTED_{secret_type.upper()}]"
                    }
                )
                findings.append(finding)
        
        findings.sort(key=lambda f: f.position)
        
        return DetectionResult(
            rule_name=self.rule_name,
            passed=len(findings) == 0,
            findings=findings
        )
```

**Fichier** : `ai/detectors/scope_detector.py`

```python
"""
Scope Detector.

Checks RBAC (Role-Based Access Control).
Detects unauthorized access attempts.
"""

from typing import Optional
from detectors.base import Detector, DetectionResult, Finding, Severity

class ScopeDetector(Detector):
    """
    Detect scope violations (unauthorized resource access).
    
    User may have role:analyst with scope:contacts_only.
    If they try to access clients → violation!
    """
    
    # Define scope hierarchy
    SCOPES = {
        'admin': ['contacts', 'clients', 'audit', 'settings'],
        'manager': ['contacts', 'clients', 'audit'],
        'analyst': ['contacts', 'audit'],
        'viewer': ['contacts']
    }
    
    def __init__(self):
        super().__init__(rule_name="scope_check")
    
    def detect(self, text: str, user_scope: Optional[str] = None, resource: Optional[str] = None) -> DetectionResult:
        """
        Check if user can access resource.
        
        Args:
            text: Ignored (for API compatibility)
            user_scope: User's scope (e.g., "contacts_only")
            resource: Resource being accessed (e.g., "clients")
        
        Returns:
            DetectionResult with violation if scope mismatch
        """
        findings = []
        
        if user_scope and resource:
            # Check if resource in allowed scopes
            allowed_resources = self.SCOPES.get(user_scope, [])
            
            if resource not in allowed_resources:
                finding = Finding(
                    type='scope_violation',
                    severity=Severity.CRITICAL,
                    value=f"User scope {user_scope} cannot access {resource}",
                    position=0,
                    context={
                        'user_scope': user_scope,
                        'resource': resource,
                        'allowed_resources': allowed_resources
                    }
                )
                findings.append(finding)
        
        return DetectionResult(
            rule_name=self.rule_name,
            passed=len(findings) == 0,
            findings=findings
        )
```

**Fichier** : `ai/detectors/test_pii_detector.py`

```python
"""Tests for PII detector."""

import pytest
from detectors.pii_detector import PiiDetector
from detectors.base import Severity

class TestPiiDetector:
    """Test PII detection."""
    
    @pytest.fixture
    def detector(self):
        return PiiDetector()
    
    def test_no_pii_in_text(self, detector):
        """Test text without PII returns no findings."""
        result = detector.detect("Hello world, this is safe text")
        assert result.passed == True
        assert len(result.findings) == 0
    
    def test_detects_email(self, detector):
        """Test email detection."""
        result = detector.detect("Contact me at sophie@example.com")
        assert result.passed == False
        assert len(result.findings) == 1
        assert result.findings[0].type == "email"
        assert result.findings[0].severity == Severity.HIGH
    
    def test_detects_phone(self, detector):
        """Test phone detection."""
        result = detector.detect("Call me at +33 6 12 34 56 78")
        assert result.passed == False
        assert len(result.findings) >= 1
        assert any(f.type == "phone" for f in result.findings)
    
    def test_detects_iban(self, detector):
        """Test IBAN detection."""
        result = detector.detect("My IBAN is FR76 3000 3000 10 0123456789")
        assert result.passed == False
        assert any(f.type == "iban" for f in result.findings)
    
    def test_multiple_pii(self, detector):
        """Test multiple PII in one text."""
        result = detector.detect("Email: sophie@example.com, Phone: +33612345678, IBAN: FR76...")
        assert result.passed == False
        assert len(result.findings) >= 3
    
    def test_result_schema(self, detector):
        """Test result schema is correct."""
        result = detector.detect("Email: test@example.com")
        data = result.to_dict()
        
        assert "rule_name" in data
        assert "passed" in data
        assert "findings" in data
        assert "count" in data
        assert data["count"] == len(data["findings"])

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

---

## 🤖 LEÇON 3 : Factory Pattern — Instancier Rules selon Policy

### 📍 Le Concept (Théorie)

**Factory Pattern** = Créer objets sans hardcoder type.

```python
# ❌ SANS FACTORY (hardcoded)
if rule == "no_pii":
    detector = PiiDetector()
elif rule == "no_secrets":
    detector = SecretsDetector()
elif rule == "scope_check":
    detector = ScopeDetector()
else:
    raise ValueError(f"Unknown rule: {rule}")

# Problem: code brittleness, repeated everywhere

# ✅ AVEC FACTORY (centralisé, data-driven)
detector = DetectorFactory.create("no_pii")
# Factory knows how to create, rest of code doesn't care
```

---

### 🚀 Cas d'usage Réel — Factory pour Instancier selon Policy

**Fichier** : `ai/pipelines/factories.py`

```python
"""
Factory for creating detectors.

Data-driven: policy YAML defines which detectors to instantiate.
Factory creates without hardcoding.
"""

from typing import List, Dict, Type, Optional
from detectors.base import Detector
from detectors.pii_detector import PiiDetector
from detectors.secrets_detector import SecretsDetector
from detectors.scope_detector import ScopeDetector

class DetectorFactory:
    """
    Factory for creating detectors based on rule names.
    
    Registry pattern: each rule name maps to detector class.
    """
    
    # Registry: rule_name → Detector class
    REGISTRY: Dict[str, Type[Detector]] = {
        'no_pii_in_prompts': PiiDetector,
        'no_api_keys_exposed': SecretsDetector,
        'scope_check': ScopeDetector,
    }
    
    @staticmethod
    def create(rule_name: str) -> Optional[Detector]:
        """
        Create detector for given rule name.
        
        Args:
            rule_name: Name of rule (e.g., "no_pii_in_prompts")
        
        Returns:
            Detector instance, or None if rule not found
        
        Raises:
            ValueError if rule not found
        """
        detector_class = DetectorFactory.REGISTRY.get(rule_name)
        
        if not detector_class:
            raise ValueError(
                f"Unknown rule: {rule_name}. "
                f"Available: {', '.join(DetectorFactory.REGISTRY.keys())}"
            )
        
        return detector_class()
    
    @staticmethod
    def create_multiple(rule_names: List[str]) -> List[Detector]:
        """
        Create multiple detectors.
        
        Args:
            rule_names: List of rule names
        
        Returns:
            List of detector instances
        """
        return [DetectorFactory.create(rule_name) for rule_name in rule_names]
    
    @staticmethod
    def register(rule_name: str, detector_class: Type[Detector]):
        """
        Register new detector (for plugins/extensions).
        
        Usage:
            DetectorFactory.register("custom_rule", CustomDetector)
        """
        DetectorFactory.REGISTRY[rule_name] = detector_class
    
    @staticmethod
    def list_rules() -> List[str]:
        """List all available rules."""
        return list(DetectorFactory.REGISTRY.keys())

# Example usage
if __name__ == "__main__":
    # Create single detector
    detector = DetectorFactory.create("no_pii_in_prompts")
    print(f"Created: {detector}")
    
    # Create multiple
    detectors = DetectorFactory.create_multiple(["no_pii_in_prompts", "no_api_keys_exposed"])
    print(f"Created {len(detectors)} detectors")
    
    # List available
    print(f"Available rules: {DetectorFactory.list_rules()}")
```

---

## 🤖 LEÇON 4 : Pipeline — Orchestration

### 📍 Le Concept (Théorie)

**Pipeline** = Orchestration : charge policy YAML → crée détecteurs → run tous → masque → audit.

**Flux** :

```
1. Load policy YAML
   compliance_policy_v1.yaml = {
     rules: [no_pii, no_secrets, scope_check],
     masking: true,
     audit: true
   }

2. Factory crée détecteurs (selon rules)
   detectors = [PiiDetector(), SecretsDetector(), ScopeDetector()]

3. Run tous les détecteurs
   all_findings = []
   for detector in detectors:
     result = detector.detect(text)
     all_findings.extend(result.findings)

4. Masker données
   masked_text = mask_pii(text, all_findings)

5. Audit trail
   audit_log.append({
     timestamp: now,
     actor: user,
     action: analyze,
     pii_found: count(all_findings),
     audit_id: uuid
   })

6. Return masked + findings + audit_id
```

---

### 🚀 Cas d'usage Réel — Pipeline Orchestration

**Fichier** : `ai/pipelines/masking.py`

```python
"""
Masking logic.

Redact sensitive data in text.
"""

import re
from typing import List, Dict
from detectors.base import Finding

class Masker:
    """
    Mask/redact sensitive data in text.
    """
    
    @staticmethod
    def mask(text: str, findings: List[Finding]) -> str:
        """
        Mask sensitive values in text.
        
        Args:
            text: Original text
            findings: List of PII/secrets to mask
        
        Returns:
            Text with sensitive values redacted
        
        Example:
            text = "Email: sophie@example.com"
            findings = [Finding(type="email", value="sophie@example.com", position=7)]
            masked = "Email: sophi*@**mple.com"
        """
        if not findings:
            return text
        
        # Sort findings by position (descending) to avoid position shifting
        sorted_findings = sorted(findings, key=lambda f: f.position, reverse=True)
        
        result = text
        for finding in sorted_findings:
            original = finding.value
            masked = Masker._mask_value(original, finding.type)
            
            # Replace at position
            start = finding.position
            end = finding.position + len(original)
            result = result[:start] + masked + result[end:]
        
        return result
    
    @staticmethod
    def _mask_value(value: str, pii_type: str) -> str:
        """
        Create masked version of sensitive value.
        
        Args:
            value: Original value (e.g., "sophie@example.com")
            pii_type: Type of PII (e.g., "email")
        
        Returns:
            Masked value (e.g., "sophi*@**mple.com")
        """
        if pii_type == "email":
            # Keep first 5 chars + last 5 chars, mask middle
            parts = value.split("@")
            if len(parts) == 2:
                local, domain = parts
                masked_local = local[:min(2, len(local))] + "*" * max(1, len(local) - 2)
                masked_domain = domain[:min(2, len(domain))] + "*" * max(1, len(domain) - 2)
                return f"{masked_local}@{masked_domain}"
        
        elif pii_type == "phone":
            # Keep last 4 digits
            return value[:-4] + "****" if len(value) > 4 else "****"
        
        elif pii_type == "iban":
            # Keep first 4 and last 4
            if len(value) > 8:
                return value[:4] + "*" * (len(value) - 8) + value[-4:]
        
        elif pii_type == "credit_card":
            # Keep first 4 and last 4
            return value[:4] + "*" * (len(value) - 8) + value[-4:]
        
        # Default: full redaction
        return "[REDACTED_" + pii_type.upper() + "]"
```

**Fichier** : `ai/pipelines/compliance_pipeline.py`

```python
"""
Main compliance pipeline.

Orchestrates: load policy → run detectors → mask → audit.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
from dataclasses import dataclass

from detectors.base import Detector, DetectionResult, Finding
from pipelines.factories import DetectorFactory
from pipelines.masking import Masker

# ===== DATA MODELS =====

@dataclass
class AnalysisRequest:
    """Request to analyze text."""
    text: str
    policy_name: str = "default"
    actor: str = "system"
    context: Optional[Dict[str, Any]] = None

@dataclass
class AnalysisResult:
    """Result from analysis."""
    original_text: str
    masked_text: str
    findings: List[Finding]
    passed: bool
    audit_id: str
    timestamp: datetime
    
    def to_dict(self):
        return {
            "original_text": self.original_text,
            "masked_text": self.masked_text,
            "findings": [f.to_dict() for f in self.findings],
            "findings_count": len(self.findings),
            "passed": self.passed,
            "audit_id": self.audit_id,
            "timestamp": self.timestamp.isoformat()
        }

# ===== PIPELINE =====

class CompliancePipeline:
    """
    Main orchestrator for compliance analysis.
    
    Workflow:
    1. Load policy (which rules to apply)
    2. Create detectors (via factory)
    3. Run all detectors
    4. Collect findings
    5. Mask sensitive data
    6. Create audit record
    7. Return result
    """
    
    # In-memory audit trail (append-only)
    audit_trail: List[Dict[str, Any]] = []
    
    def __init__(self):
        """Initialize pipeline with default policy."""
        # TODO: Load policy from YAML file
        self.policy_name = "default"
        self.rules = ["no_pii_in_prompts", "no_api_keys_exposed"]  # Could load from YAML
    
    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Analyze text for compliance violations.
        
        Args:
            request: AnalysisRequest with text, policy, actor
        
        Returns:
            AnalysisResult with findings, masked text, audit_id
        """
        audit_id = str(uuid.uuid4())[:8]
        
        # Step 1: Create detectors from policy
        detectors = DetectorFactory.create_multiple(self.rules)
        
        # Step 2: Run all detectors
        all_findings: List[Finding] = []
        for detector in detectors:
            result = detector.detect(request.text)
            all_findings.extend(result.findings)
        
        # Step 3: Mask sensitive data
        masked_text = Masker.mask(request.text, all_findings)
        
        # Step 4: Determine if passed
        passed = len(all_findings) == 0
        
        # Step 5: Create audit record
        audit_record = {
            "audit_id": audit_id,
            "timestamp": datetime.utcnow().isoformat(),
            "actor": request.actor,
            "action": "analyze",
            "policy": self.policy_name,
            "findings_count": len(all_findings),
            "passed": passed,
            "context": request.context or {}
        }
        
        # Step 6: Append to audit trail (append-only = immuable)
        CompliancePipeline.audit_trail.append(audit_record)
        
        # Step 7: Create result
        result = AnalysisResult(
            original_text=request.text,
            masked_text=masked_text,
            findings=all_findings,
            passed=passed,
            audit_id=audit_id,
            timestamp=datetime.utcnow()
        )
        
        return result
    
    @staticmethod
    def get_audit_trail() -> List[Dict[str, Any]]:
        """Get append-only audit trail (read-only)."""
        return CompliancePipeline.audit_trail.copy()
    
    @staticmethod
    def audit_trail_size() -> int:
        """Get size of audit trail."""
        return len(CompliancePipeline.audit_trail)

# Example usage
if __name__ == "__main__":
    pipeline = CompliancePipeline()
    
    request = AnalysisRequest(
        text="Contact: sophie@example.com, IBAN: FR76123456",
        actor="user_sophie"
    )
    
    result = pipeline.analyze(request)
    
    print("=== ANALYSIS RESULT ===")
    print(f"Original: {result.original_text}")
    print(f"Masked: {result.masked_text}")
    print(f"Findings: {len(result.findings)}")
    print(f"Passed: {result.passed}")
    print(f"Audit ID: {result.audit_id}")
    
    print("\n=== AUDIT TRAIL ===")
    for record in CompliancePipeline.get_audit_trail():
        print(record)
```

---

## 🤖 LEÇON 5 : Audit Trail Immuable (Append-Only)

### 📍 Le Concept (Théorie)

**Audit Trail Immuable** = Log qui ne peut pas être modifié une fois écrit.

```
❌ MUTABLE LOG (dangereusité) :
  [10:15] Sophie viewed PII
  [10:20] Sophie deleted PII   ← Peut être modifié!
  Audit: "Sophie never saw PII" (false!)

✅ IMMUABLE LOG (sécurisé) :
  [10:15] Sophie viewed PII  ← Impossible d'effacer
  [10:20] Sophie deleted PII ← Impossible d'effacer
  Audit: "Sophie saw PII on 10:15" (proof!)
```

**Implémentation** :

```python
class AuditTrail:
    def __init__(self):
        self.records = []  # List, not dict (can't modify by key)
    
    def log(self, record: Dict):
        """Append only, never delete/update."""
        self.records.append(record)  # INSERT only
    
    def get_records(self) -> List[Dict]:
        """Read-only view (copy)."""
        return self.records.copy()  # Return copy, not reference

# ❌ Impossible:
# audit_trail.records[0] = new_record  # Can't modify
# audit_trail.records.pop(0)           # Can't delete

# ✅ Possible:
# audit_trail.log(new_record)          # Only append
```

**Pourquoi append-only?**

1. **Légale** : IA Act EU demande "full traceability". Immuable = legal defense.
2. **Forensics** : Si violation détectée, audit trail est preuve historique.
3. **Réparation** : Client demande "qui a vu mes données?", réponse immuable.

---

### 💼 Préparation Entretien (Q&A)

#### **Q1 : "Expliquez le Strategy pattern. Pourquoi utilisé pour les détecteurs?"**

**Réponse attendue** :

> "Strategy pattern = interface commune pour implémentations interchangeables.
>
> **Appliqué à Engine** :
> - Interface : Detector(ABC) avec method detect()
> - Stratégies : PiiDetector, SecretsDetector, ScopeDetector
> - Pipeline : agnostic aux implémentations, utilise polymorphism
>
> **Avantage** :
> - ✅ **Extensible** : Ajouter CustomDetector = extend Detector + register. Zéro changement pipeline.
> - ✅ **Testable** : Mock Detector en tests (no real detection needed).
> - ✅ **Reusable** : Detector peut servir autre système (pas couplé NovaCRM).
>
> **Sans Strategy** : `if rule == 'pii': ... elif rule == 'secrets': ...` scattered. Hard to extend.
> **Avec Strategy** : Pipeline agnostic. Rules defined in YAML. Pluggable."

**Score** : ✅ Montrez compréhension polymorphism + extensibility.

---

#### **Q2 : "Décrivez le Factory pattern pour créer détecteurs."**

**Réponse attendue** :

> "Factory pattern = créer objets sans hardcoding type. Data-driven.
>
> **Exemple** :
> ```python
> # Policy YAML
> rules: [no_pii, no_secrets, scope_check]
>
> # Factory crée détecteurs
> detectors = DetectorFactory.create_multiple(policy.rules)
> # = [PiiDetector(), SecretsDetector(), ScopeDetector()]
>
> # Pipeline runs all
> for detector in detectors:
>     result = detector.detect(text)
> ```
>
> **Avantage** :
> - ✅ **Data-driven** : Policy YAML définit quels détecteurs. Pas hardcoded.
> - ✅ **Centralisé** : Créations en un endroit (factory). Pas scattered if/else.
> - ✅ **Extensible** : Nouvelle détection? Ajouter à registry. Policy inclut la règle.
>
> **Use case NovaCRM** :
> - S1 : policy = [no_pii] (lancer minimal)
> - S3 : policy = [no_pii, no_secrets] (ajouter détection secrets)
> - S5 : policy = [no_pii, no_secrets, scope_check] (ajouter RBAC)
> - Zero code change, just update policy.yaml"

**Score** : ✅ Montrez compréhension creation logic centralisée + data-driven evolution.

---

#### **Q3 : "Comment l'audit trail est-il immuable?"**

**Réponse attendue** :

> "Audit trail immuable = append-only logging. INSERT only, jamais UPDATE/DELETE.
>
> **Implémentation** :
> ```python
> class AuditTrail:
>     def log(self, record):
>         self.records.append(record)  # INSERT only
>     
>     def get(self):
>         return self.records.copy()  # Read-only copy
> 
> # Impossible:
> # audit_trail.records[0] = new   # Can't modify
> # audit_trail.records.pop()      # Can't delete
> ```
>
> **Pourquoi immuable?**
> - ✅ **IA Act compliance** : EU demande traçabilité complète. Immuable = proof.
> - ✅ **Forensics** : Si violation, audit = incontestable historique.
> - ✅ **Legal defense** : Client sues: 'Who saw my PII?' Réponse immuable: 'Only sophie on Jan 28 10:15'
>
> **Storage** :
> - Dev : in-memory list (OK pour tests)
> - Prod : append-only DB (Event Sourcing, dedicated audit table, immutable snapshots)"

**Score** : ✅ Montrez compréhension immuabilité + justification légale.

---

#### **Q4 : "Donnez un exemple de flow complet : créer contact → masquer PII → audit."**

**Réponse attendue** :

> "Flow complet :
>
> ```python
> # 1. User creates contact
> POST /api/v1/contacts {
>   name: 'Sophie',
>   email: 'sophie@example.com',
>   iban: 'FR76123456'
> }
>
> # 2. Backend calls engine
> request = AnalysisRequest(
>     text='sophie@example.com FR76123456',
>     actor='user_sophie'
> )
> result = pipeline.analyze(request)
>
> # 3. Engine pipeline
> # - PiiDetector finds: [email, iban]
> # - Mask: 'sophi*@**mple.com FR76xxxxxx'
> # - Audit: '[2026-01-28 10:15] actor:sophie action:create pii_found:2 audit_id:001]'
>
> # 4. Backend stores
> contact.email = 'sophi*@**mple.com'
> contact.iban = 'FR76xxxxxx'
> db.save(contact)
>
> # 5. Return to frontend
> response = {
>     id: 123,
>     name: 'Sophie',
>     email: 'sophi*@**mple.com',  # Masked
>     iban: 'FR76xxxxxx',          # Masked
>     audit_id: '001'
> }
>
> # 6. Audit trail (append-only)
> audit_trail.append({
>     audit_id: '001',
>     timestamp: '2026-01-28T10:15:23',
>     actor: 'sophie',
>     action: 'create_contact',
>     pii_found: 2,
>     passed: true
> })
> ```
>
> **Key points** :
> - ✅ Original PII never stored in DB (masked before INSERT)
> - ✅ Audit trail records WHAT was detected + WHO detected it
> - ✅ Append-only = forever proof that masking was applied"

**Score** : ✅ Montrez compréhension flow complet + security measures.

---

### ✅ Validation de l'étape — SECTION D Complète

**Checklist** :

- [ ] Vous comprenez **Architecture Engine** (detectors, pipeline, policies, audit)
- [ ] Vous comprenez **Strategy pattern** (interface + implémentations)
- [ ] Vous comprenez **Factory pattern** (créer selon policy)
- [ ] Vous comprenez **Pipeline orchestration** (run detectors, mask, audit)
- [ ] Vous comprenez **Audit trail immuable** (append-only, legal defense)
- [ ] Vous pouvez **implémenter PiiDetector** (regex patterns, findings)
- [ ] Vous pouvez **créer Factory** (registry, create methods)
- [ ] Vous pouvez **écrire tests** (pytest, test cases)
- [ ] Vous répondez aux **4 questions entretien** avec confiance

---

**Fin de SECTION D — AI Compliance Engine**

✅ **Vous savez maintenant** :
- Architecture Engine (détecteurs, rules, policies)
- Patterns critiques (Strategy, Factory)
- Implémentation concrète (code samples)
- Audit trail immuable (compliance)
- Comment intégrer Engine au Backend

➡️ **Prochaine** : SECTION E — Audit/PII/IA Act (fondation légale)
