# backend/Dockerfile
FROM python:3.11-slim

# Install Poetry
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Configure Poetry not to use virtualenvs
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry-cache

WORKDIR /app

# Install dependencies
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-root --no-dev

# Copy application code
COPY . .

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]

