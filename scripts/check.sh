#!/usr/bin/env bash
set -euo pipefail
(cd backend && ruff check . && mypy app detection && pytest)
(cd frontend && npm run lint && npm run typecheck && npm test && npm run build)
docker compose config >/dev/null
