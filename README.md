# OriginLens
OriginLens is a privacy-first writing analysis platform that estimates statistical
patterns associated with machine-generated writing. It is **not proof of authorship**
and must not drive consequential decisions automatically.

## Architecture and features
Next.js provides a responsive analyzer and responsible result report. FastAPI owns
the versioned contract; PostgreSQL persists metadata, Redis/Celery isolate expensive
local ModernBERT inference, and Mailpit captures development email. The explicit fake
backend is for tests only and is rejected in production.

## Setup
Requires Docker 24+ and Compose v2 (or Python 3.12 and Node 22 manually).
```bash
cp .env.example .env
# generate secrets: openssl rand -hex 32
./scripts/bootstrap.sh
docker compose up --build
```
Open http://localhost:3000, API docs at http://localhost:8000/docs, and Mailpit at
http://localhost:8025. Run `make check`, `make e2e`, or `make model-smoke`.
Production must provide unique `SECRET_KEY`, Fernet-compatible `ENCRYPTION_KEY`,
`DATABASE_URL`, `REDIS_URL`, SMTP configuration, allowed hosts/origins, and optionally
pinned `MODEL_REVISION`. Cache model files before rollout. Use TLS, private database
networks, backups, one model worker per available memory budget, and migrate before
traffic. Roll back application and schema only with a tested backup.

The baseline model is GeorgeDrayson/modernbert-ai-detection. Identity calibration is
not a probability; English-only, short, transformed, translated, formulaic, and
out-of-domain inputs can be wrong.
