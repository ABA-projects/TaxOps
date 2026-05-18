Actúa como DevOps Engineer especializado en TaxOps. El stack de producción es:
- **Frontend**: Next.js 15.3 en Vercel (`taxops-web` service)
- **API**: FastAPI Python en Vercel (`web` service, servida en `/_/web`)
- **DB**: PostgreSQL en Supabase (proyecto `dhiopkrtaubeogjehopb`, us-west-1)
- **CI**: GitHub Actions (`.github/workflows/ci.yml`)
- **Deploy**: Vercel auto-deploy en push a `main`

## Arquitectura Vercel (`vercel.json` raíz)

```json
{
  "experimentalServices": {
    "taxops-web": { "entrypoint": "taxops-web", "routePrefix": "/",      "framework": "nextjs" },
    "web":        { "entrypoint": "api",         "routePrefix": "/_/web" }
  }
}
```

El service `web` usa `api/index.py` como ASGI entry point → re-exporta `app` de `api/main.py`.

## Variables de entorno en Vercel

**Servicio `web` (FastAPI):**
| Variable | Descripción |
|----------|-------------|
| `DATABASE_URL` | `postgresql://postgres:[PASS]@db.dhiopkrtaubeogjehopb.supabase.co:5432/postgres` |
| `SECRET_KEY` | JWT secret — generar con `openssl rand -hex 32` |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `7` |
| `ALLOWED_ORIGINS` | URL del frontend en Vercel (e.g. `https://tax-ops.vercel.app`) |
| `API_BASE_URL` | `https://tax-ops.vercel.app/_/web` |
| `FRONTEND_URL` | `https://tax-ops.vercel.app` |
| `GROQ_API_KEY` | console.groq.com |
| `TAXOPS_ENV` | `production` |
| `TAXOPS_SUPERADMIN_EMAILS` | email del superadmin |
| `BOOTSTRAP_SECRET` | string secreto para el endpoint `/setup/bootstrap` |

**Servicio `taxops-web` (Next.js):**
| Variable | Valor |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://tax-ops.vercel.app/_/web` |

## Bootstrap inicial (una sola vez)

Tras el primer deploy exitoso, crear la organización y usuario owner:

```bash
curl -X POST "https://tax-ops.vercel.app/_/web/setup/bootstrap" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "secret=<BOOTSTRAP_SECRET>&org_slug=taxops&org_name=TaxOps&email=<EMAIL>&password=<PASS>"
```

## Desarrollo local

```bash
# API FastAPI (desde /api)
cd api && uvicorn main:app --reload --port 8000

# Frontend Next.js (desde /taxops-web)
cd taxops-web && npm run dev

# Docker completo (app + PostgreSQL local + Adminer)
cp .env.example .env   # rellenar DATABASE_URL y GROQ_API_KEY
docker-compose up --build
# App: http://localhost:3000 | Adminer: http://localhost:8080
```

## CI — GitHub Actions

`.github/workflows/ci.yml` corre en cada push/PR a main:
- `api-lint` → flake8 + mypy
- `api-test` → pytest
- `web-lint` → ESLint + tsc
- `web-build` → next build

Vercel despliega automáticamente cuando CI pasa.

## Supabase — operaciones DB

```
Dashboard: https://supabase.com/dashboard/project/dhiopkrtaubeogjehopb
SQL Editor: https://supabase.com/dashboard/project/dhiopkrtaubeogjehopb/sql
DB Host: db.dhiopkrtaubeogjehopb.supabase.co (port 5432)
```

Reset password: Settings → Database → Database password → Reset

Alembic migrations corren automáticamente en startup de FastAPI (`lifespan`).
Para correr manualmente:
```bash
cd api && alembic upgrade head
```

## Checklist deploy nuevo entorno

- [ ] Obtener DATABASE_URL de Supabase (Settings → Database → Connection string)
- [ ] Crear proyecto en Vercel → importar repo GitHub → `ABA-projects/TaxOps`
- [ ] Agregar todas las variables de entorno en Vercel dashboard
- [ ] Push a `main` → Vercel auto-deploys ambos servicios
- [ ] Llamar `/setup/bootstrap` para crear org + usuario inicial
- [ ] Verificar `https://tax-ops.vercel.app/_/web/health` retorna `{"status":"ok","db":"connected"}`

$ARGUMENTS
