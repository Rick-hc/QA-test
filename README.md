# QA Search System

This mono-repo contains a question answering search system built with FastAPI and React.

## Prerequisites
- Docker & Docker Compose
- Poetry 1.8+
- Node.js 18+

## Quickstart
```bash
# spin up services
make up
# run backend and frontend
make backend
make frontend
```

See `.env.example` in `backend/` for environment variables. A sample Excel file should be placed at `data/qa.xlsx`.

### Environment variables
- `DATABASE_URL` – connection string for Postgres
- `OPENAI_API_KEY` – OpenAI API key
