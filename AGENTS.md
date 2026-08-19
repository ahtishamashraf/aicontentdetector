# OriginLens engineering guide

## Architecture
The monorepo contains `frontend/` (Next.js UI), `backend/app/` (FastAPI),
`backend/detection/` (local model and deterministic features), `backend/alembic/`
(PostgreSQL migrations), `scripts/`, and `docs/`.

## Commands
- Install: `make bootstrap`
- Develop: `docker compose up --build`
- Migrate: `docker compose run --rm api alembic upgrade head`
- Test/lint/type-check/build: `make check`
- Backend tests: `cd backend && uv run pytest`
- Backend lint/type: `cd backend && uv run ruff check . && uv run mypy app detection`
- Frontend tests: `cd frontend && npm test`
- Frontend lint/type/build: `cd frontend && npm run lint && npm run typecheck && npm run build`
- E2E: `make e2e`; real model: `make model-smoke`

Fix a failing validation before progressing. Never log submitted/extracted text or
secrets. Never make conclusive authorship claims. Core analysis must not call a
third-party LLM API. Keep UI mobile-first, WCAG 2.2 AA, keyboard accessible, and
respect reduced motion. Python is fully typed; tests accompany behavior. Every
schema change requires an Alembic migration. Never commit secrets in code,
fixtures, logs, or commits.

## Definition of done
Behavior is implemented (no fake UI), migrations and tests pass, production builds,
privacy/security controls are maintained, documentation matches reality, and
`docs/STATUS.md` records validation honestly.
