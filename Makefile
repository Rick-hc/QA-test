up:
	docker-compose -f infra/docker-compose.yml up -d

down:
	docker-compose -f infra/docker-compose.yml down

backend:
	cd backend && poetry run uvicorn app.main:app --reload

frontend:
	cd frontend && npm run dev
