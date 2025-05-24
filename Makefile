.PHONY: install run format help

install: ## Set up Python virtualenv and install backend/frontend dependencies
	python3 -m venv venv
	. venv/bin/activate && pip install -r backend/requirements.txt
	cd frontend && npm install

run: ## Start FastAPI backend and Vue frontend in development mode
	. venv/bin/activate && uvicorn backend.main:app --reload &
	cd frontend && npm run dev

format: ## Format backend with black and frontend with prettier
	venv/bin/black backend
	prettier --write frontend

resetdb:  ## Drop and recreate the PostgreSQL database, then seed it
	docker exec -i coffee-db psql -U coffee -d coffee_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	PYTHONPATH=. python3 backend/init_db.py

help: ## Show available make commands
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""
