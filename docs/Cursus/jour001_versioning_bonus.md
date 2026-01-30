# 📋 BONUS : Comprendre le Versioning FastAPI et le Pinning de Versions

## Pourquoi "pincer" la version de FastAPI ?

FastAPI est en version `0.x.x` (< 1.0.0). Selon le Semantic Versioning :

| Partie | Nom | Signification | Exemple |
|--------|------|--------------|----------|
| **0** | MAJOR | Numéro majeur (rarement changé) | 0.x.x |
| **.104** | MINOR | Nouvelle version (peut avoir breaking changes) | 0.**104**.1 → 0.**105**.1 = risque ⚠️ |
| **.1** | PATCH | Corrections de bugs (jamais breaking changes) | 0.104.**1** → 0.104.**2** = sûr ✅ |

**Conséquence** : Si on spécifie `fastapi>=0.104.0`, et que 0.105.0 sort demain avec breaking changes, notre code peut casser.

## Solution : Pincer la version

```txt
# ❌ MAUVAIS (risqué)
fastapi>=0.128.0
# Accepte : 0.128.0, 0.128.1, 0.129.0, 0.135.0, 1.0.0 (breaking changes !)

# ✅ BON (sûr - RECOMMANDÉ)
fastapi[standard]==0.128.0
# Accepte UNIQUEMENT : 0.128.0 (27 décembre 2025 - stable)

# ✅ ACCEPTABLE (un peu moins strict)
fastapi[standard]>=0.128.0,<0.129.0
# Accepte : 0.128.0, 0.128.1, 0.128.2 (patches fixes, jamais breaking changes)
```

## Pourquoi `[standard]` ?

`fastapi[standard]` inclut les dépendances optionnelles pour la production :
- `uvloop` (accélère les boucles asynchrones de 2-4x)
- `httptools` (parser HTTP optimisé)
- `python-multipart` (upload de fichiers)

Nous utilisons déjà `uvicorn[standard]`, donc c'est cohérent.

## Upgrading de version : le processus sûr

1. Vous avez des tests (exercices Jour 001 ✅)
2. Testez la nouvelle version : `pip install 'fastapi[standard]==0.105.0' -q && pytest tests/`
3. Si tous les tests passent → Mettez à jour `requirements.txt` et committez

```bash
# Exemple réel
(.venv) PS C:\Perso\nova-crm> pip install 'fastapi[standard]==0.128.0'
(.venv) PS C:\Perso\nova-crm> pytest tests/backend/ -v
# ... tous les tests passent ✅
(.venv) PS C:\Perso\nova-crm> # Mettre à jour requirements.txt
(.venv) PS C:\Perso\nova-crm> git add backend/requirements.txt
(.venv) PS C:\Perso\nova-crm> git commit -m "Upgrade FastAPI de 0.128.0 à 0.129.0 (tous les tests PASSED)"
```

## À propos de Starlette (ne PAS pincer)

Starlette est la base de FastAPI. **Ne pas pincer sa version** car FastAPI gère automatiquement la version compatible de Starlette. Si vous la pincez, vous risquez une incompatibilité.

```txt
# ❌ À ÉVITER
starlette==0.27.0  # Non ! Laisser FastAPI décider

# ✅ CORRECT
# (Ne pas spécifier starlette du tout)
```

## À propos de Pydantic (peut être pincé)

Pydantic > 1.0.0 est compatible avec FastAPI. Vous pouvez utiliser :

```txt
# ✅ BON
pydantic>=2.0.0,<3.0.0

# ✅ AUSSI BON
pydantic==2.5.2
```

## Résumé : Stratégie de Versioning pour NovaCRM

| Package | Stratégie | Rationale |
|---------|-----------|-----------|
| **fastapi[standard]** | Pincer à `==0.128.0` | Version < 1.0.0, MINOR = breaking changes |
| **uvicorn[standard]** | Pincer à `==0.40.0` | Dépendance critique (serveur) |
| **sqlalchemy** | Pincer à `==2.0.46` | ORM critique, patches importants |
| **alembic** | Pincer à `==1.18.1` | Migrations BD, sync avec SQLAlchemy |
| **pydantic** | Pincer à `==2.12.5` | Validation, énormes corrections |
| **pydantic-settings** | Pincer à `==2.12.0` | Config, sync avec Pydantic |
| **pytest** | Pincer à `==9.0.2` | Tests (version 9.x moderne) |
| **pytest-asyncio** | Pincer à `==1.3.0` | Tests async FastAPI |
| **httpx** | `>=0.28.0,<0.29.0` | HTTP client (moins critique) |
| **python-dotenv** | `>=1.2.0,<2.0.0` | Gestion .env (stagnant) |
| **starlette** | ❌ NE PAS AJOUTER | Géré automatiquement par FastAPI |
| **aiofiles** | `>=23.0,<24.0` | I/O async (stable) |
| **black** | `>=23.0` | Formatter (non-critique dev) |
| **pylint** | `>=3.0` | Linter (non-critique dev) |
| **mypy** | `>=1.7` | Type checker (non-critique dev) |

