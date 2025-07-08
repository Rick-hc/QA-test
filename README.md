# QA Search System

This repository provides a full stack example of a QA search system. It includes a FastAPI backend with ETL script, React frontend and Docker Compose setup.

## Quickstart

```bash
make up          # start postgres, chroma, backend and frontend
make backend     # run backend in dev mode
make frontend    # run frontend in dev mode
```

Visit http://localhost:3000.

## Environment Variables

Backend reads the following variables:

- `DATABASE_URL` – Postgres URL
- `OPENAI_API_KEY` – API key for embeddings and GPT
- `CHROMA_HOST` – Chroma HTTP endpoint

Create `.env` from `.env.example` and adjust the values.

## ETL Example

Prepare `data/qa.xlsx` and run:

```bash
poetry run python backend/scripts/ingest.py data/qa.xlsx
```

## CI

GitHub Actions installs dependencies and runs backend tests on each push. Failed builds send a Slack notification via `SLACK_WEBHOOK` secret.
