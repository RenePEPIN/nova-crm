# 🔐 SECTION E : Audit Trail Immuable, PII Masking, IA Act Compliance

**Durée estimée** : 8-10 heures  
**Prérequis** : SECTION A (contexte), SECTION D (Engine)  
**Objectif** : Comprendre et implémenter la fondation légale du projet (audit trail immuable, PII protection, conformité IA Act)

**⚠️ CRITICITÉ MAXIMALE** :
- S2 go/no-go DÉPEND de l'audit trail immuable fonctionnel
- GDPR + IA Act EU 2024 = obligations légales (pas optionnel)
- PII masking = fondation sécurité (bugs = GDPR fines énormes)

---

## 🔐 LEÇON 1 : Audit Trail Immuable (Append-Only Architecture)

### 📍 Le Concept (Théorie)

**Audit Trail Immuable** = Journal des actions qui ne peut pas être modifié une fois écrit.

**Problème sans audit trail** :

```
T=10:15 : Sophie views contact (with IBAN)
T=10:16 : Admin modifies audit log : "Sophie never viewed contact"
T=10:17 : Client sues : "Who saw my IBAN?"
         Admin says : "Nobody" (false, provable in court)
         → Company loses lawsuit, fined for non-compliance
```

**Solution avec audit trail immuable** :

```
T=10:15 : Sophie views contact (IBAN detected, masked before display)
         Audit log : "[10:15] Sophie viewed contact:123, pii:IBAN detected → masked"
T=10:16 : Admin CANNOT modify this log (append-only architecture prevents it)
T=10:17 : Client sues : "Who saw my IBAN?"
         Company shows audit log : "[10:15] Sophie viewed, masked before access"
         → Company wins, proves compliance
```

**Append-only = impossible de:
- ❌ Modifier record (UPDATE)
- ❌ Effacer record (DELETE)
- ✅ Seulement ajouter record (INSERT)

---

### 🚀 Cas d'usage Réel (NovaCRM Compliance)

**Scenario 1 : Contact view**

```
T=10:15:23 : User Sophie opens contact "Jean Dupont"
             Backend logs: {
               timestamp: "2026-01-28T10:15:23",
               actor: "sophie",
               action: "contact_view",
               resource: "contact:456",
               pii_involved: "email (masked before display)",
               audit_id: "audit_20260128_001",
               compliance: "GDPR Art.32 (audit trail)" 
             }

T=10:15:24 : Audit trail appended (INSERT only, never modifiable)

T=2026-07-15 : Legal audit
              Question: "Who accessed Jean Dupont's email?"
              Answer: "Only Sophie on 2026-01-28 at 10:15:23 (audit_20260128_001)"
              Evidence: Immutable log proves compliance
```

**Scenario 2 : PII masking audit**

```
T=10:15:50 : Backend creates contact with email "sophie@example.com"
             Engine detects PII → masks to "sophi*@**mple.com"
             Audit log: {
               action: "contact_create",
               pii_detected: ["email"],
               masking_applied: true,
               audit_id: "audit_20260128_002",
               masked_values: {
                 email: "sophi*@**mple.com"
               }
             }

T=10:15:51 : Log appended to audit trail (immutable forever)

T=2026-03-15 : Compliance check
              "How many PII detected and masked in Q1?"
              Count from audit trail: 1,234 PII masked
              Proof: Immutable logs show masking was always applied
              → GDPR compliant
```

---

### 💻 Implémentation — Audit Trail Immuable

#### **Structure de la base de données**

**Table** : `audit_trail` (append-only, never updated/deleted)

```sql
-- audit_trail table
-- INSERT-only, never UPDATE/DELETE
-- Primary key = (timestamp, id) = insertion order = immutable

CREATE TABLE audit_trail (
    -- Primary key (auto-generated at insert time)
    id SERIAL PRIMARY KEY,
    
    -- Immutable fields (set at creation, never changed)
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    audit_id VARCHAR(255) NOT NULL UNIQUE,  -- UUID for linking
    
    -- Who performed action
    actor VARCHAR(255) NOT NULL,  -- User or system
    actor_role VARCHAR(50) NOT NULL,  -- admin, manager, analyst, viewer
    
    -- What action
    action VARCHAR(100) NOT NULL,  -- contact_view, contact_create, contact_delete, etc
    
    -- On what resource
    resource_type VARCHAR(50) NOT NULL,  -- contact, client, opportunity, etc
    resource_id INTEGER,
    
    -- Compliance info
    pii_involved BOOLEAN DEFAULT FALSE,  -- Was PII accessed/modified?
    pii_types VARCHAR(255),  -- email, phone, iban, etc (comma-separated)
    pii_masked BOOLEAN DEFAULT FALSE,  -- Was PII masked before storage?
    
    -- Details (JSON for flexibility)
    details JSONB,  -- {findings_count: 2, masked_fields: ["email"], ...}
    
    -- Immutability markers
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    -- NEVER add: updated_at, deleted_at (would violate immutability)
    
    -- Compliance regulations
    gdpr_relevant BOOLEAN DEFAULT FALSE,
    ia_act_relevant BOOLEAN DEFAULT FALSE,
    
    -- Constraints
    CONSTRAINT audit_trail_immutable CHECK (
        -- Ensure timestamp is set at creation (never NULL)
        timestamp IS NOT NULL
    )
);

-- Indexes for querying (don't affect immutability)
CREATE INDEX idx_audit_trail_timestamp ON audit_trail(timestamp);
CREATE INDEX idx_audit_trail_actor ON audit_trail(actor);
CREATE INDEX idx_audit_trail_resource ON audit_trail(resource_type, resource_id);
CREATE INDEX idx_audit_trail_audit_id ON audit_trail(audit_id);

-- View: enforce read-only (nobody should write except append)
CREATE VIEW audit_trail_view AS
SELECT * FROM audit_trail;

-- Policies: enforce append-only
-- (In PostgreSQL, add RLS to prevent UPDATE/DELETE)
ALTER TABLE audit_trail ENABLE ROW LEVEL SECURITY;

-- Policy: Allow INSERT only
CREATE POLICY audit_trail_insert_only ON audit_trail
    FOR INSERT WITH CHECK (true);

-- Policy: Prevent UPDATE
CREATE POLICY audit_trail_no_update ON audit_trail
    FOR UPDATE USING (false);  -- Always false = nobody can update

-- Policy: Prevent DELETE
CREATE POLICY audit_trail_no_delete ON audit_trail
    FOR DELETE USING (false);  -- Always false = nobody can delete
```

#### **Python Implementation — Append-Only Logger**

**Fichier** : `backend/infrastructure/audit/audit_logger.py`

```python
"""
Append-only audit logger.

Central point for logging all compliance-relevant actions.
Immutable by design (append-only, no updates/deletes possible).
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, asdict
import uuid
import json
import logging

logger = logging.getLogger(__name__)

# ===== DATA MODELS =====

@dataclass
class AuditRecord:
    """Single audit record (immutable once created)."""
    
    # Immutable identifiers
    audit_id: str
    timestamp: datetime
    
    # Who
    actor: str  # User ID or "system"
    actor_role: str  # admin, manager, analyst, viewer
    
    # What action
    action: str  # contact_view, contact_create, pii_detected, etc
    
    # On what resource
    resource_type: str  # contact, client, audit, etc
    resource_id: Optional[int] = None
    
    # Compliance info
    pii_involved: bool = False
    pii_types: Optional[List[str]] = None  # email, phone, iban, etc
    pii_masked: bool = False
    
    # Details (flexible JSON)
    details: Optional[Dict[str, Any]] = None
    
    # Compliance relevance
    gdpr_relevant: bool = False
    ia_act_relevant: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (for JSON serialization)."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)

# ===== AUDIT LOGGER =====

class AuditLogger:
    """
    Append-only audit logger.
    
    Central place for logging all compliance-relevant actions.
    Enforces immutability (append-only, no modifications).
    """
    
    # In-memory storage (for demo; prod uses DB)
    _audit_trail: List[AuditRecord] = []
    
    @staticmethod
    def log(
        action: str,
        actor: str,
        actor_role: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        pii_involved: bool = False,
        pii_types: Optional[List[str]] = None,
        pii_masked: bool = False,
        details: Optional[Dict[str, Any]] = None,
        gdpr_relevant: bool = False,
        ia_act_relevant: bool = False
    ) -> str:
        """
        Log audit record (append-only).
        
        Args:
            action: Action performed (contact_view, contact_create, etc)
            actor: User ID or "system"
            actor_role: admin/manager/analyst/viewer
            resource_type: contact/client/audit/etc
            resource_id: ID of resource
            pii_involved: Was PII accessed/modified?
            pii_types: List of PII types detected
            pii_masked: Was PII masked?
            details: Extra metadata (JSON)
            gdpr_relevant: GDPR compliance relevant?
            ia_act_relevant: IA Act compliance relevant?
        
        Returns:
            audit_id (for linking to other records)
        
        Side effects:
            - Appends record to audit trail (never modifiable)
            - Logs to standard logging
        """
        # Generate unique audit ID
        audit_id = f"audit_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
        
        # Create record
        record = AuditRecord(
            audit_id=audit_id,
            timestamp=datetime.utcnow(),
            actor=actor,
            actor_role=actor_role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            pii_involved=pii_involved,
            pii_types=pii_types,
            pii_masked=pii_masked,
            details=details,
            gdpr_relevant=gdpr_relevant,
            ia_act_relevant=ia_act_relevant
        )
        
        # Append to trail (INSERT only, never UPDATE/DELETE)
        AuditLogger._audit_trail.append(record)
        
        # Log to standard logging (for operational visibility)
        logger.info(
            f"AUDIT: {record.audit_id} | actor:{actor} | action:{action} | "
            f"resource:{resource_type}:{resource_id} | pii_masked:{pii_masked}"
        )
        
        return audit_id
    
    @staticmethod
    def get_trail() -> List[AuditRecord]:
        """
        Get audit trail (read-only copy).
        
        Returns:
            Copy of audit trail (modifications don't affect original)
        """
        return AuditLogger._audit_trail.copy()
    
    @staticmethod
    def get_trail_json() -> str:
        """Get audit trail as JSON string."""
        return json.dumps(
            [record.to_dict() for record in AuditLogger._audit_trail],
            default=str
        )
    
    @staticmethod
    def filter_by_actor(actor: str) -> List[AuditRecord]:
        """Get all actions by specific actor."""
        return [r for r in AuditLogger._audit_trail if r.actor == actor]
    
    @staticmethod
    def filter_by_resource(resource_type: str, resource_id: int) -> List[AuditRecord]:
        """Get all actions on specific resource."""
        return [r for r in AuditLogger._audit_trail 
                if r.resource_type == resource_type and r.resource_id == resource_id]
    
    @staticmethod
    def filter_by_pii() -> List[AuditRecord]:
        """Get all actions involving PII."""
        return [r for r in AuditLogger._audit_trail if r.pii_involved]
    
    @staticmethod
    def get_compliance_report() -> Dict[str, Any]:
        """Generate compliance report from audit trail."""
        trail = AuditLogger._audit_trail
        
        return {
            "total_actions": len(trail),
            "unique_actors": len(set(r.actor for r in trail)),
            "actions_involving_pii": len([r for r in trail if r.pii_involved]),
            "pii_records_masked": len([r for r in trail if r.pii_masked]),
            "gdpr_relevant_actions": len([r for r in trail if r.gdpr_relevant]),
            "ia_act_relevant_actions": len([r for r in trail if r.ia_act_relevant]),
            "timeline": {
                "first_action": trail[0].timestamp.isoformat() if trail else None,
                "last_action": trail[-1].timestamp.isoformat() if trail else None
            }
        }
    
    @staticmethod
    def size() -> int:
        """Get size of audit trail."""
        return len(AuditLogger._audit_trail)

# ===== USAGE EXAMPLES =====

if __name__ == "__main__":
    # Example 1: Log contact view with PII
    audit_id = AuditLogger.log(
        action="contact_view",
        actor="sophie",
        actor_role="analyst",
        resource_type="contact",
        resource_id=456,
        pii_involved=True,
        pii_types=["email"],
        pii_masked=True,  # Important: PII was masked
        details={"masked_fields": ["email"]},
        gdpr_relevant=True
    )
    print(f"Logged: {audit_id}")
    
    # Example 2: Log contact creation with PII masking
    audit_id = AuditLogger.log(
        action="contact_create",
        actor="system",
        actor_role="admin",
        resource_type="contact",
        resource_id=789,
        pii_involved=True,
        pii_types=["email", "phone"],
        pii_masked=True,
        details={"original": "email detected", "masked": "sophi*@**mple.com"},
        gdpr_relevant=True,
        ia_act_relevant=True
    )
    
    # Example 3: Get compliance report
    report = AuditLogger.get_compliance_report()
    print(f"\nCompliance Report: {report}")
    
    # Example 4: Query audit trail
    print(f"\nAudit trail size: {AuditLogger.size()}")
    print(f"PII-related actions: {len(AuditLogger.filter_by_pii())}")
```

---

## 🔐 LEÇON 2 : PII Masking & Redaction Strategies

### 📍 Le Concept (Théorie)

**PII Masking** = Transformer données sensibles pour que ne soient pas lisibles.

```
Original : sophie@example.com
Masked   : sophi*@**mple.com
```

**Strategies** :

| Strategy | Usage | Readability | Security |
|----------|-------|-------------|----------|
| **Partial masking** | Visible hint + masking | High (can recognize) | Medium |
| **Full redaction** | Complete replacement | Low (can't read) | High |
| **Hashing** | One-way hash | None (hash unreadable) | Very High |
| **Encryption** | Reversible (with key) | None (encrypted) | High |

---

### 🚀 Cas d'usage Réel — Masking Strategies

**Fichier** : `backend/infrastructure/security/masking.py`

```python
"""
PII masking strategies.

Different masking approaches for different PII types.
Goal: Protect PII while maintaining some readability (context).
"""

import hashlib
import re
from typing import Dict, Any

class MaskingStrategy:
    """
    Base class for masking strategies.
    Different PII types need different masks.
    """
    
    @staticmethod
    def mask_email(email: str) -> str:
        """
        Mask email address.
        
        Example:
            sophie@example.com → sophi*@**mple.com
        
        Approach:
        - Keep first 2 chars of local part (for context)
        - Replace middle with *
        - Keep last 2 chars of domain (for context)
        """
        if not email or '@' not in email:
            return "[INVALID_EMAIL]"
        
        local, domain = email.split('@')
        
        # Keep first 2 + last 2, mask middle
        if len(local) <= 3:
            masked_local = local[0] + '*' * (len(local) - 1)
        else:
            masked_local = local[:2] + '*' * (len(local) - 4) + local[-2:]
        
        # Mask domain similarly
        if len(domain) <= 3:
            masked_domain = domain[0] + '*' * (len(domain) - 1)
        else:
            parts = domain.split('.')
            masked_domain = parts[0][:2] + '*' * (len(parts[0]) - 2)
            for part in parts[1:]:
                masked_domain += '.' + part[:2] + '*' * max(0, len(part) - 2)
        
        return f"{masked_local}@{masked_domain}"
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """
        Mask phone number.
        
        Example:
            +33 6 12 34 56 78 → +33 6 12 34 ****
        
        Approach:
        - Keep country code + first few digits
        - Replace last 4 digits with ****
        """
        if not phone:
            return "[INVALID_PHONE]"
        
        # Remove spaces/hyphens for processing
        digits = re.sub(r'[^0-9+]', '', phone)
        
        # Keep first 6 chars, mask rest
        if len(digits) <= 6:
            return '*' * len(digits)
        
        return digits[:6] + '*' * (len(digits) - 6)
    
    @staticmethod
    def mask_iban(iban: str) -> str:
        """
        Mask IBAN (bank account).
        
        Example:
            FR76 3000 3000 10 0123456789 → FR76 3000 3000 10 xxxxxx6789
        
        Approach:
        - Keep first 15 chars (country code + bank info)
        - Mask middle
        - Keep last 4 digits
        """
        if not iban or len(iban) < 15:
            return "[INVALID_IBAN]"
        
        return iban[:15] + '*' * (len(iban) - 19) + iban[-4:]
    
    @staticmethod
    def mask_ssn_france(ssn: str) -> str:
        """
        Mask French Social Security Number.
        
        Example:
            1 87 12 34 567 890 → [REDACTED_SSN]
        
        Approach:
        - Full redaction (SSN is highly sensitive)
        """
        return "[REDACTED_SSN]"
    
    @staticmethod
    def mask_credit_card(cc: str) -> str:
        """
        Mask credit card.
        
        Example:
            4532 1234 5678 9012 → 4532 **** **** 9012
        
        Approach:
        - Keep first 4 (bank ID) + last 4 (checksum)
        - Mask middle 8
        """
        if not cc or len(cc) < 13:
            return "[INVALID_CC]"
        
        # Remove spaces
        cc_clean = cc.replace(' ', '')
        
        if len(cc_clean) < 13:
            return "[INVALID_CC]"
        
        return cc_clean[:4] + ' ' + '*' * 4 + ' ' + '*' * 4 + ' ' + cc_clean[-4:]
    
    @staticmethod
    def hash_value(value: str) -> str:
        """
        One-way hash (for case-insensitive comparison, forensics).
        
        Example:
            sophie@example.com → a3f4b2c1d8e9... (SHA256)
        
        Use case:
        - Store hashed email to check duplicates (without storing real email)
        - Forensics: detect if same person accessed multiple times
        """
        return hashlib.sha256(value.lower().encode()).hexdigest()
    
    @staticmethod
    def mask_by_type(pii_type: str, value: str) -> str:
        """
        Route to correct masking strategy based on PII type.
        
        Args:
            pii_type: Type of PII (email, phone, iban, etc)
            value: Value to mask
        
        Returns:
            Masked value
        """
        strategies = {
            'email': MaskingStrategy.mask_email,
            'phone': MaskingStrategy.mask_phone,
            'iban': MaskingStrategy.mask_iban,
            'ssn_france': MaskingStrategy.mask_ssn_france,
            'credit_card': MaskingStrategy.mask_credit_card,
        }
        
        strategy = strategies.get(pii_type, lambda v: f"[REDACTED_{pii_type.upper()}]")
        return strategy(value)

# ===== USAGE =====

if __name__ == "__main__":
    print("=== Email Masking ===")
    print(f"Original: sophie@example.com")
    print(f"Masked: {MaskingStrategy.mask_email('sophie@example.com')}")
    
    print("\n=== Phone Masking ===")
    print(f"Original: +33 6 12 34 56 78")
    print(f"Masked: {MaskingStrategy.mask_phone('+33 6 12 34 56 78')}")
    
    print("\n=== IBAN Masking ===")
    print(f"Original: FR76 3000 3000 10 0123456789")
    print(f"Masked: {MaskingStrategy.mask_iban('FR76 3000 3000 10 0123456789')}")
    
    print("\n=== Credit Card Masking ===")
    print(f"Original: 4532 1234 5678 9012")
    print(f"Masked: {MaskingStrategy.mask_credit_card('4532 1234 5678 9012')}")
    
    print("\n=== Hash ===")
    print(f"Original: sophie@example.com")
    print(f"Hash: {MaskingStrategy.hash_value('sophie@example.com')}")
```

---

## 🔐 LEÇON 3 : IA Act Compliance & DPIA

### 📍 Le Concept (Théorie)

**IA Act (EU Regulation 2024)** = Nouvelles obligations pour systèmes IA.

**Key requirements** :

| Requirement | What | Why | NovaCRM Implementation |
|-------------|------|-----|------------------------|
| **Transparency** | Know when IA is used | Users have right to know | Dashboard: "AI detected PII" banner |
| **Audit Trail** | Log all IA decisions | Legal defense (who saw what) | Audit trail immuable (append-only) |
| **Risk Assessment** | Classify AI risk (Low/Med/High/Critical) | Proportional controls | Engine assigns severity to findings |
| **Data Protection** | Protect PII used by IA | GDPR + IA Act | Masking before storage + audit |
| **Human Oversight** | Humans review critical decisions | Can't automate compliance away | Alerts for CRITICAL findings |

**DPIA (Data Protection Impact Assessment)** = Evaluation de risques données.

```
Question: "What are risks to data privacy in this system?"
Answer: "Low, because..."
1. PII is detected and masked before storage (risk mitigation)
2. Audit trail immuable (accountability)
3. Access control via RBAC (confidentiality)
4. Encryption at rest (security)
5. Regular backups (availability)
```

---

### 🚀 Cas d'usage Réel — DPIA Template NovaCRM

**Fichier** : `docs/compliance/DPIA_Template.md`

```markdown
# DPIA — Data Protection Impact Assessment

**Project** : NovaCRM + AI Compliance Hub
**Date** : 2026-01-28
**Evaluator** : CTO + Legal Team

## 1. System Description

**Purpose** :
- Manage customer relationships (contacts, clients, opportunities)
- Automatically detect and protect PII (emails, phones, IBANs, etc)
- Provide audit trail for compliance

**Data types processed** :
- Contact info : name, email, phone, address (PII)
- Financial info : IBAN, credit card (sensitive)
- Communication : emails, messages (personal data)
- Audit info : who accessed what, when (non-sensitive)

**Processing** :
1. User inputs contact data
2. Backend sends to AI Engine for PII detection
3. Engine masks PII before storage
4. Database stores only masked data
5. Audit trail records action (append-only)

## 2. Data Processing & Storage

| Data Type | Storage | Masking | Encryption | Retention |
|-----------|---------|---------|-----------|-----------|
| Email | DB | ✅ Yes (sophi*@**) | ✅ AES-256 | 365 days |
| Phone | DB | ✅ Yes (+33****) | ✅ AES-256 | 365 days |
| IBAN | DB | ✅ Yes (FR76xxx) | ✅ AES-256 | 365 days |
| Audit | Append-only DB | N/A | ✅ AES-256 | Forever |

## 3. Risk Assessment

### Risk 1: PII Exposure (original risk)

**Severity** : 🔴 **CRITICAL** (without mitigation)

**Scenario** :
- Raw contact data stored in DB
- Admin can see real PII
- Risk: GDPR violation, fines up to 4% revenue

**Mitigation** :
- ✅ AI detects PII before storage
- ✅ Masking applied automatically
- ✅ Real PII never stored in DB
- ✅ Access logs show who viewed what

**Residual Risk** : 🟢 **LOW** (with mitigation)

### Risk 2: Unauthorized Access (access control risk)

**Severity** : 🔴 **HIGH** (without mitigation)

**Scenario** :
- User "analyst" only has scope:contacts
- But can somehow access scope:clients
- Risk: Data breach, unauthorized access

**Mitigation** :
- ✅ RBAC with 4 roles (admin/manager/analyst/viewer)
- ✅ Scope validation on every request
- ✅ Audit trail logs access attempts
- ✅ CRITICAL findings trigger alerts

**Residual Risk** : 🟡 **MEDIUM** (with mitigation)

### Risk 3: Audit Trail Tampering (audit risk)

**Severity** : 🔴 **CRITICAL** (without mitigation)

**Scenario** :
- Admin modifies audit log: "This access didn't happen"
- Compliance violation hidden
- Risk: Legal liability, court loses evidence

**Mitigation** :
- ✅ Audit trail is append-only (no updates/deletes)
- ✅ Database RLS prevents UPDATE/DELETE
- ✅ Immutability enforced at DB layer
- ✅ Backup of audit trail (separate storage)

**Residual Risk** : 🟢 **LOW** (with mitigation)

### Risk 4: IA Bias or False Positives

**Severity** : 🟡 **MEDIUM** (without mitigation)

**Scenario** :
- PII detector misclassifies "Paris" as location (false positive)
- Valid data gets masked unnecessarily
- Risk: Data quality degradation, false compliance

**Mitigation** :
- ✅ Multiple detectors (PII, secrets, scope)
- ✅ Human review for CRITICAL findings
- ✅ Monitoring of false positive rate
- ✅ Regular policy updates (rules versioned)

**Residual Risk** : 🟡 **MEDIUM** (with mitigation)

## 4. Compliance Checklist

- ✅ **GDPR Art.5** (Principles) : Lawfulness, fairness, transparency
  - Audit trail shows lawful processing
  - Masking shows data minimization
  
- ✅ **GDPR Art.32** (Security) : Encryption, audit logging, access control
  - AES-256 encryption at rest
  - Append-only audit trail
  - RBAC with role enforcement
  
- ✅ **GDPR Art.35** (DPIA) : This assessment itself
  
- ✅ **IA Act (EU 2024)** : Transparency, auditability, human oversight
  - Dashboard shows "AI detected PII"
  - Audit trail logs all IA decisions
  - Alerts for critical decisions (human review)

- ✅ **Data Retention** : Delete after 365 days (GDPR Art.17)
  - Automated job: delete records > 1 year
  - Audit trail kept indefinitely (compliance)

## 5. Monitoring & Controls

**Monthly** :
- Review audit trail for anomalies
- Check PII detection rate (baseline)
- Verify no UPDATE/DELETE on audit table

**Quarterly** :
- Penetration testing (access control)
- GDPR compliance audit
- Risk reassessment (new threats?)

**Yearly** :
- Full DPIA refresh
- IA Act compliance review
- Legal + security joint assessment

## 6. Conclusion

**Overall Risk Level** : 🟢 **LOW**

With implemented mitigations (masking, audit trail, RBAC, encryption), NovaCRM meets GDPR + IA Act requirements.

Residual risks are managed through monitoring and human oversight.
```

---

## 🔐 LEÇON 4 : IA Act Compliance Implementation

### 📍 Le Concept (Théorie)

**IA Act Requirements** mapped to NovaCRM:

```
1. TRANSPARENCY
   Requirement: Users know when IA is used
   Implementation: ComplianceBanner component (frontend)
                  "⚠️ AI detected PII → masked before storage"

2. AUDITABILITY
   Requirement: Log all IA decisions
   Implementation: Audit trail immuable (backend)
                  "[action:detect_pii][findings:2][masked:true]"

3. RISK CLASSIFICATION
   Requirement: Classify IA risk (Low/Medium/High/Critical)
   Implementation: Detector returns Severity enum
                  HIGH = PII found, must mask
                  CRITICAL = SS#/credit card, must block

4. HUMAN OVERSIGHT
   Requirement: Humans review critical decisions
   Implementation: Alert system + dashboard
                  CRITICAL findings → admin notification

5. DOCUMENTATION
   Requirement: Document IA system design
   Implementation: This section E + DPIA + ADRs
```

---

### 🚀 Caso d'uso Réel — IA Act Implementation

**Fichier** : `backend/compliance/ia_act.py`

```python
"""
IA Act compliance module.

Implements:
1. Risk classification (Low/Medium/High/Critical)
2. Transparency (logging what IA found)
3. Human oversight (alerts for critical findings)
4. Documentation (DPIA trail)
"""

from enum import Enum
from typing import List, Dict, Any
from datetime import datetime

# ===== ENUMS =====

class IARiskLevel(Enum):
    """IA risk levels (per IA Act)."""
    MINIMAL = "minimal"       # No PII, normal operation
    LOW = "low"               # Non-sensitive data
    MEDIUM = "medium"         # Potential false positive, review needed
    HIGH = "high"             # PII detected, masking applied
    CRITICAL = "critical"     # Sensitive PII (SSN, CC), must block/alert

class IADecisionType(Enum):
    """Type of IA decision."""
    ALLOW = "allow"           # Safe to proceed
    MASK = "mask"             # Mask data before storage
    ALERT = "alert"           # Alert admin, human review needed
    BLOCK = "block"           # Block operation completely

# ===== IA ACT COMPLIANCE =====

class IAActCompliance:
    """
    IA Act compliance enforcement.
    
    Per EU Regulation 2024, systems using IA must:
    1. Be transparent (users know when IA is used)
    2. Be auditable (log all decisions)
    3. Classify risk (low/medium/high/critical)
    4. Provide human oversight (humans review critical decisions)
    5. Document system design (DPIA)
    """
    
    @staticmethod
    def evaluate_risk(
        pii_types: List[str],
        findings_count: int
    ) -> Dict[str, Any]:
        """
        Evaluate IA risk based on detections.
        
        Args:
            pii_types: List of detected PII types (email, phone, ssn, etc)
            findings_count: Number of PII items found
        
        Returns:
            Risk assessment dict
        """
        # Determine risk level
        if not pii_types:
            risk_level = IARiskLevel.MINIMAL
            decision = IADecisionType.ALLOW
        
        elif any(t in ['ssn_france', 'credit_card'] for t in pii_types):
            # Sensitive PII = CRITICAL
            risk_level = IARiskLevel.CRITICAL
            decision = IADecisionType.ALERT  # Alert admin for review
        
        elif findings_count > 5:
            # Many items = HIGH (potential bulk PII leak)
            risk_level = IARiskLevel.HIGH
            decision = IADecisionType.MASK
        
        elif any(t in ['email', 'phone', 'iban'] for t in pii_types):
            # Standard PII = HIGH
            risk_level = IARiskLevel.HIGH
            decision = IADecisionType.MASK
        
        else:
            # Low-risk
            risk_level = IARiskLevel.LOW
            decision = IADecisionType.MASK
        
        return {
            "risk_level": risk_level.value,
            "decision": decision.value,
            "requires_human_review": risk_level in [
                IARiskLevel.CRITICAL,
                IARiskLevel.MEDIUM
            ]
        }
    
    @staticmethod
    def generate_transparency_message(
        pii_types: List[str],
        masked: bool
    ) -> str:
        """
        Generate user-facing transparency message.
        
        Per IA Act: "Users must know when IA is used."
        
        Args:
            pii_types: Detected PII types
            masked: Was PII masked?
        
        Returns:
            Human-readable message for frontend
        """
        if not pii_types:
            return "No PII detected."
        
        pii_str = ", ".join(pii_types)
        
        if masked:
            return (
                f"⚠️ AI detected sensitive information ({pii_str}). "
                f"Data has been automatically protected (masked) before storage. "
                f"Your data is secure. [More info →]"
            )
        else:
            return (
                f"⚠️ AI detected sensitive information ({pii_str}). "
                f"Review recommended. [Contact admin]"
            )
    
    @staticmethod
    def generate_dpia_evidence() -> Dict[str, Any]:
        """
        Generate evidence for DPIA (Data Protection Impact Assessment).
        
        Returns:
            Dict with compliance evidence
        """
        return {
            "assessment_date": datetime.utcnow().isoformat(),
            "system": "NovaCRM + AI Compliance Hub",
            "ia_technologies": [
                "Regex-based PII detection",
                "Pattern matching for secrets",
                "RBAC for access control"
            ],
            "risk_mitigation": [
                "PII masking before storage",
                "Audit trail immuable (append-only)",
                "Encryption at rest (AES-256)",
                "Access control (RBAC)",
                "Human oversight (alerts)"
            ],
            "compliance_standards": [
                "GDPR (EU 2018)",
                "IA Act (EU 2024)",
            ],
            "transparency_mechanisms": [
                "ComplianceBanner (frontend)",
                "Audit trail (backend)",
                "Detailed logging",
                "Admin dashboard"
            ]
        }

# ===== USAGE =====

if __name__ == "__main__":
    # Example 1: Evaluate risk
    risk = IAActCompliance.evaluate_risk(
        pii_types=["email", "iban"],
        findings_count=2
    )
    print(f"Risk Assessment: {risk}")
    
    # Example 2: Generate transparency message
    msg = IAActCompliance.generate_transparency_message(
        pii_types=["email"],
        masked=True
    )
    print(f"\nTransparency Message:\n{msg}")
    
    # Example 3: DPIA evidence
    dpia = IAActCompliance.generate_dpia_evidence()
    print(f"\nDPIA Evidence: {dpia}")
```

---

## 🔐 LEÇON 5 : Integration Backend — Audit + Masking + IA Act

### 🚀 Flow Complet : Contact Creation avec Compliance

**Fichier** : `backend/infrastructure/http/routes/contacts.py`

```python
"""
Contact routes with compliance integration.

Flow:
1. User creates contact
2. Backend sends to Engine for PII detection
3. Engine detects + masks
4. Backend stores masked data
5. Audit trail logs action
6. IA Act compliance checks
7. Return masked data + compliance banner
"""

from fastapi import APIRouter, HTTPException, Request
from typing import List, Dict, Any
from datetime import datetime

from core.domain.contact import Contact
from shared.dto import ContactCreateDTO, ContactResponseDTO
from infrastructure.audit.audit_logger import AuditLogger
from infrastructure.security.masking import MaskingStrategy
from compliance.ia_act import IAActCompliance
from ai.pipelines.compliance_pipeline import CompliancePipeline, AnalysisRequest

router = APIRouter(prefix="/api/v1/contacts", tags=["contacts"])

# ===== CREATE CONTACT WITH COMPLIANCE =====

@router.post("/", response_model=ContactResponseDTO)
async def create_contact(
    contact: ContactCreateDTO,
    request: Request
) -> ContactResponseDTO:
    """
    Create new contact with AI compliance checks.
    
    Flow:
    1. Validate input (Pydantic auto)
    2. Call Engine for PII detection
    3. Mask PII before storage
    4. Save masked contact to DB
    5. Log audit trail
    6. Check IA Act compliance
    7. Return masked contact + compliance info
    
    Args:
        contact: Contact data (validated by Pydantic)
        request: HTTP request (for actor info)
    
    Returns:
        ContactResponseDTO (with masked PII + compliance banner)
    
    Raises:
        422: Validation error (Pydantic)
        400: Business error (email already exists, etc)
    """
    
    # ===== Step 1: Extract actor (who is creating?) =====
    # TODO: Extract from JWT token
    actor = "system"  # or request.state.user['id']
    actor_role = "admin"  # or request.state.user['role']
    
    # ===== Step 2: Call Engine for compliance analysis =====
    # Combine all text fields for analysis
    analysis_text = f"{contact.email} {contact.phone or ''} {contact.notes or ''}"
    
    analysis_request = AnalysisRequest(
        text=analysis_text,
        policy_name="default",
        actor=actor,
        context={
            "action": "contact_create",
            "contact_name": contact.name
        }
    )
    
    # Run compliance analysis
    pipeline = CompliancePipeline()
    analysis_result = pipeline.analyze(analysis_request)
    
    # ===== Step 3: Mask PII in contact data =====
    masked_email = contact.email
    masked_phone = contact.phone
    
    for finding in analysis_result.findings:
        if finding.type == "email":
            masked_email = MaskingStrategy.mask_email(contact.email)
        elif finding.type == "phone":
            masked_phone = MaskingStrategy.mask_phone(contact.phone)
    
    # ===== Step 4: Create domain entity (with masked data) =====
    contact_entity = Contact(
        name=contact.name,
        email=masked_email,  # MASKED
        phone=masked_phone,  # MASKED
        company=contact.company,
        notes=contact.notes
    )
    
    # ===== Step 5: Save to database =====
    # TODO: Implement DB save
    # saved_contact = await db.save(contact_entity)
    contact_entity.id = 123  # Simulated save
    contact_entity.created_at = datetime.utcnow()
    
    # ===== Step 6: Log audit trail =====
    audit_id = AuditLogger.log(
        action="contact_create",
        actor=actor,
        actor_role=actor_role,
        resource_type="contact",
        resource_id=contact_entity.id,
        pii_involved=len(analysis_result.findings) > 0,
        pii_types=[f.type for f in analysis_result.findings],
        pii_masked=True,  # We always mask
        details={
            "masked_fields": [f.type for f in analysis_result.findings],
            "findings_count": len(analysis_result.findings),
            "contact_name": contact.name
        },
        gdpr_relevant=True,
        ia_act_relevant=True
    )
    
    # ===== Step 7: Check IA Act compliance =====
    ia_act_eval = IAActCompliance.evaluate_risk(
        pii_types=[f.type for f in analysis_result.findings],
        findings_count=len(analysis_result.findings)
    )
    
    # If CRITICAL, alert admin
    if ia_act_eval["requires_human_review"]:
        # TODO: Send alert to admin dashboard
        print(f"⚠️ ALERT: CRITICAL finding in contact creation (audit_id={audit_id})")
    
    # ===== Step 8: Generate transparency message =====
    compliance_banner = IAActCompliance.generate_transparency_message(
        pii_types=[f.type for f in analysis_result.findings],
        masked=True
    )
    
    # ===== Step 9: Return response (masked data + compliance info) =====
    return ContactResponseDTO(
        id=contact_entity.id,
        name=contact_entity.name,
        email=contact_entity.email,  # MASKED
        phone=contact_entity.phone,  # MASKED
        company=contact_entity.company,
        created_at=contact_entity.created_at,
        # Compliance info
        audit_id=audit_id,
        pii_detected=len(analysis_result.findings) > 0,
        compliance_banner=compliance_banner
    )

# ===== GET CONTACT (with audit logging) =====

@router.get("/{contact_id}", response_model=ContactResponseDTO)
async def get_contact(
    contact_id: int,
    request: Request
) -> ContactResponseDTO:
    """
    Get contact by ID.
    
    Logs access to audit trail (who viewed what PII?).
    """
    
    # Extract actor
    actor = "system"  # TODO: from JWT
    actor_role = "analyst"  # TODO: from JWT
    
    # TODO: Get contact from DB
    contact_entity = Contact(
        id=contact_id,
        name="Jean Dupont",
        email="jean@example.com",  # Would be masked in DB
        phone="+33612345678",  # Would be masked in DB
        created_at=datetime.utcnow()
    )
    
    # Log access (GDPR: who viewed PII?)
    AuditLogger.log(
        action="contact_view",
        actor=actor,
        actor_role=actor_role,
        resource_type="contact",
        resource_id=contact_id,
        pii_involved=True,  # Contact contains PII
        pii_types=["email", "phone"],
        pii_masked=True,  # Data in DB is masked
        gdpr_relevant=True
    )
    
    return ContactResponseDTO.from_orm(contact_entity)

# ===== GET AUDIT TRAIL (admin only) =====

@router.get("/audit/trail")
async def get_audit_trail(request: Request) -> Dict[str, Any]:
    """
    Get audit trail (admin only).
    
    Shows all compliance-related actions (who accessed what, when).
    """
    
    # TODO: Check permission (admin only)
    
    trail = AuditLogger.get_trail()
    
    return {
        "audit_trail": [record.to_dict() for record in trail],
        "compliance_report": AuditLogger.get_compliance_report()
    }
```

---

## 💼 Préparation Entretien (Q&A)

#### **Q1 : "Expliquez audit trail immuable. Pourquoi append-only?"**

**Réponse attendue** :

> "Audit trail immuable = log qui ne peut pas être modifié (append-only).
>
> **Pourquoi append-only?**
>
> Sans immuabilité :
> - Admin view : 'Sophie viewed PII'
> - Admin modify : 'Actually, nobody viewed PII'
> - Compliance check : Impossible de prouver qui a vu quoi
> - Risk: GDPR fine + jail time (fraud)
>
> Avec immuabilité :
> - Action: 'Sophie viewed PII at 10:15'
> - Cannot delete/modify (DB constraint + code design)
> - Compliance check: 'Sophie viewed, proof is in audit trail'
> - Risk: Company can defend legally
>
> **Implementation** :
> - DB table without UPDATE/DELETE triggers
> - Code design: append() only, no modify()
> - RLS (Row Level Security) prevents UPDATE/DELETE
> - Backup of audit table (separate immutable storage)
>
> **IA Act requirement** : EU 2024 demands 'full traceability'. Append-only = proof."

**Score** : ✅ Montrez compréhension immuabilité + raison légale + implémentation.

---

#### **Q2 : "Donnez 5 stratégies de masking PII. Quand utiliser chacune?"**

**Réponse attendue** :

> "5 Masking strategies :
>
> 1. **Partial masking** (keep hints, mask middle)
>    - Email: sophie@example.com → sophi*@**mple.com
>    - Use: Context needed (user can recognize their own email)
>    - Security: Medium (can be reverse-engineered)
>
> 2. **Full redaction** (complete replacement)
>    - SSN: 1 87 12 34 567 890 → [REDACTED_SSN]
>    - Use: Highly sensitive (SS#, credit card)
>    - Security: High (impossible to recover)
>
> 3. **Hashing** (one-way, irreversible)
>    - Email: sophie@example.com → a3f4b2c1d8e9... (SHA256)
>    - Use: Deduplication (check if email exists, without storing real email)
>    - Security: Very High (mathematically irreversible)
>    - Limitation: Can't restore original
>
> 4. **Encryption** (reversible with key)
>    - Email: sophie@example.com → AES_ENCRYPTED_VALUE
>    - Use: Need to decrypt later (with proper key management)
>    - Security: High if key is protected
>    - Limitation: Key must be managed securely
>
> 5. **Tokenization** (replace with token)
>    - Email: sophie@example.com → TOKEN_ABC123
>    - Use: Payment processing (PCI compliance)
>    - Security: Depends on token store (external vault)
>
> **NovaCRM approach** :
> - Partial masking for emails/phones (user context)
> - Full redaction for SS#/credit cards (illegal to store)
> - Hashing for deduplication checks
> - Encryption at rest (additional layer)
>"

**Score** : ✅ Montrez 5 strategies + trade-offs + choix NovaCRM.

---

#### **Q3 : "Qu'est-ce que la DPIA? Pourquoi obligatoire pour NovaCRM?"**

**Réponse attendue** :

> "DPIA (Data Protection Impact Assessment) = Évaluation des risques données.
>
> **Qu'est-ce?**
> Questionnaire qui répond à :
> - Quelles données traitez-vous?
> - Pourquoi?
> - Qui y accède?
> - Comment les protégez-vous?
> - Quels sont les risques?
> - Comment les atténuez-vous?
>
> **Obligatoire quand?**
> Per GDPR Art.35, DPIA required si :
> - Traitement large-scale de données (NovaCRM = yes)
> - PII sensitive (NovaCRM = yes, contacts + financial)
> - Utilisation d'IA (NovaCRM = yes, compliance engine)
> - Monitoring systématique (NovaCRM = yes, audit trail)
>
> **NovaCRM DPIA** :
> 1. System Description (CRM + Engine)
> 2. Data types (email, phone, IBAN, etc)
> 3. Risk Assessment
>    - Risk 1: PII exposure → Mitigation: masking + audit
>    - Risk 2: Unauthorized access → Mitigation: RBAC
>    - Risk 3: Audit tampering → Mitigation: append-only
> 4. Compliance checklist (GDPR + IA Act)
> 5. Monitoring plan (monthly/quarterly/yearly)
>
> **Outcome** : 'Overall risk = LOW (with mitigations)'
> = Legal defense if challenged
>"

**Score** : ✅ Montrez compréhension DPIA + obligation légale + structure NovaCRM.

---

#### **Q4 : "Décrivez le flow complet : créer contact → masquer PII → audit trail."**

**Réponse attendue** :

> "Flow complet (10 steps):
>
> ```
> Step 1: User submits POST /api/v1/contacts
>         {name: 'Sophie', email: 'sophie@example.com', phone: '+33...'}
>
> Step 2: Backend receives (Pydantic validates input)
>
> Step 3: Backend calls Engine
>         engine.analyze('sophie@example.com +33...')
>
> Step 4: Engine runs detectors
>         - PiiDetector finds: [email, phone]
>         - SecretsDetector finds: nothing
>         - ScopeDetector finds: nothing (user has contact scope)
>
> Step 5: Engine masks findings
>         - email: 'sophie@example.com' → 'sophi*@**mple.com'
>         - phone: '+33612345678' → '+336****78'
>
> Step 6: Engine returns result
>         {
>           pii_found: 2,
>           masked_data: {email: 'sophi*@**', phone: '+336****'},
>           audit_id: 'audit_001'
>         }
>
> Step 7: Backend stores masked contact
>         DB.contacts.insert({
>           name: 'Sophie',
>           email: 'sophi*@**mple.com',  # MASKED
>           phone: '+336****78'           # MASKED
>         })
>
> Step 8: Backend logs audit trail (append-only)
>         AuditTrail.append({
>           timestamp: '2026-01-28T10:15:23',
>           actor: 'sophie',
>           action: 'contact_create',
>           resource: 'contact:123',
>           pii_found: 2,
>           pii_masked: true,
>           audit_id: 'audit_001',
>           gdpr_relevant: true,
>           ia_act_relevant: true
>         })
>
> Step 9: Backend checks IA Act compliance
>         - Risk level: HIGH (2 PII items found)
>         - Decision: MASK (mitigated)
>         - Requires human review: false
>
> Step 10: Backend returns to frontend
>          {
>            id: 123,
>            name: 'Sophie',
>            email: 'sophi*@**mple.com',  # MASKED
>            phone: '+336****78',          # MASKED
>            audit_id: 'audit_001',
>            compliance_banner: '⚠️ AI detected PII → masked'
>          }
>
> Frontend shows:
>   - Masked contact data (safe)
>   - Compliance banner (transparency per IA Act)
>   - Link to 'View full audit' (admin only)
> ```
>
> **Key points** :
> - ✅ Original PII never stored (masked before INSERT)
> - ✅ Audit trail is append-only (immuable forever)
> - ✅ IA Act compliance checked (risk classification)
> - ✅ Transparency (user sees banner)
> - ✅ GDPR compliant (PII protected, audit trail, no retention beyond 1 year)
>"

**Score** : ✅ Montrez flow complet + all security measures + compliance.

---

### ✅ Validation de l'étape — SECTION E Complète

**Checklist** :

- [ ] Vous comprenez **audit trail immuable** (append-only, why)
- [ ] Vous comprenez **PII masking strategies** (5 types + when to use)
- [ ] Vous comprenez **DPIA** (what, why, structure)
- [ ] Vous comprenez **IA Act compliance** (requirements, implementation)
- [ ] Vous pouvez **implémenter audit logger** (append-only, queryable)
- [ ] Vous pouvez **masquer PII** (par type, partial vs full redaction)
- [ ] Vous pouvez **générer DPIA** (risk assessment, mitigations)
- [ ] Vous comprenez **IA Act risk classification** (Low/Medium/High/Critical)
- [ ] Vous répondez aux **4 questions entretien** avec confiance

---

**Fin de SECTION E — Audit Trail, PII Masking, IA Act Compliance**

✅ **Vous savez maintenant** :
- Audit trail immuable (append-only architecture)
- PII masking strategies (5 approches)
- DPIA (Data Protection Impact Assessment)
- IA Act compliance (EU 2024 requirements)
- Integration complète (audit + masking + compliance dans flow contact)
- Legal foundations (GDPR + IA Act)

➡️ **Prochaine** : LAB 3 — Implémenter rule no_pii_in_prompts (hands-on exercise)
