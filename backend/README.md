# Backend

Enterprise FastAPI backend for the AI DevOps Platform. The service currently provides the platform foundation only: authentication, health checks, configuration, logging, dependency injection, and Swagger/OpenAPI documentation. AI functionality is intentionally not implemented yet.

## Features

- FastAPI application with Swagger UI at `/docs` and OpenAPI JSON at `/openapi.json`
- JWT bearer authentication under `/api/v1/auth`
- Health endpoints at `/health/live`, `/health/ready`, and `/api/v1/health`
- Environment-based configuration with `pydantic-settings`
- Container-friendly logging
- FastAPI dependency injection seams for settings, authentication, and services

## Local development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
uvicorn app.main:app --reload --app-dir src
```

Default demo credentials for local-only authentication smoke tests:

- Email: `admin@example.com`
- Password: `ChangeMe123!`

Replace the in-memory user service and `JWT_SECRET_KEY` before using this service outside local development.

## Tests

```bash
cd backend
pytest
ruff check src tests
```
