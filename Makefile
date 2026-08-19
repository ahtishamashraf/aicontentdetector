.PHONY: bootstrap check e2e model-smoke
bootstrap:
	./scripts/bootstrap.sh
check:
	./scripts/check.sh
e2e:
	cd frontend && npm run e2e
model-smoke:
	cd backend && python -m pytest -m model_smoke
