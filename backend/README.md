# AI DevOps Platform — Backend

The backend is the FastAPI service that powers the AI DevOps Platform.

It provides:

- Authentication and JWT-based access control
- Project management
- DevOps analysis
- AI action interpretation
- Docker DevOps actions
- Kubernetes inspection and actions
- Persistent AI analysis history
- Persistent DevOps action history
- Application and dependency health checks
- PostgreSQL persistence
- Redis integration
- Ollama-based local AI inference

## Technology Stack

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Pydantic Settings
- Docker SDK for Python
- Kubernetes Python Client
- Ollama
- JWT authentication
- Argon2 password hashing

## Backend Structure

The main application is under `src/app`:

```
src/app/
    ├── api/              # API dependencies and versioned routers
    ├── core/             # Application configuration and runtime concerns
    ├── db/               # Database setup and sessions
    ├── exceptions/       # Application exceptions and handlers
    ├── middleware/       # HTTP middleware
    ├── mixins/           # Shared model mixins
    ├── models/           # SQLAlchemy models
    ├── prompts/          # AI prompts
    ├── providers/        # AI provider implementations
    ├── repositories/     # Database repository layer
    ├── schemas/          # Pydantic request/response schemas
    ├── security/         # Authentication and authorization
    ├── services/         # Application and DevOps services
    └── main.py           # FastAPI application entry point
```

## API

The API is versioned under:
```
/api/v1
```
Interactive API documentation is available through FastAPI:
```
http://localhost:8000/docs
```
OpenAPI JSON:
```
http://localhost:8000/openapi.json
```
The backend includes API areas for:

- Authentication
- Projects
- AI operations
- AI analysis history
- DevOps actions
- Kubernetes operations
- Health checks

## Health Endpoints

Application health:
```
GET /api/v1/health
```
Dependency health:
```
GET /api/v1/health/dependencies
```
The dependency health check verifies:

- PostgreSQL
- Redis
- Ollama

Example:
```
{
  "status": "ready",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "ollama": "healthy"
  }
}
```

## AI Provider

The backend uses a provider abstraction so AI functionality is separated from the rest of the application.

Current local provider:
```
Ollama
```
Current model:
```
llama3.2:3b
```
The provider implementation is located under:
```
src/app/providers/
```
Current providers include:
```
base.py
factory.py
ollama.py
openai.py
```
Ollama is the active provider for the project.

## AI Workflows

The backend supports the following AI workflows:

### Dockerfile Analysis

Analyzes Dockerfile content and returns findings and recommendations.

### Kubernetes Analysis

Analyzes Kubernetes-related configuration or input and returns operational findings.

### Terraform Analysis

Analyzes Terraform configuration.

The project does not use Terraform to provision its own infrastructure.

### Log Analysis

Analyzes log input and identifies potential issues and recommendations.

### AI Action Interpretation

Interprets a user's DevOps request and maps it to a supported operational action when appropriate.

### DevOps Integration

The backend integrates with external DevOps interfaces through dedicated services.

### Docker

Docker operations use the Docker SDK for Python.

The containerized backend receives access to the host Docker daemon through:
```
/var/run/docker.sock
```
This allows supported Docker actions to be executed without running a separate Docker daemon inside the backend container.

### Kubernetes

Kubernetes operations use the official Kubernetes Python client.

The backend receives the development kubeconfig through a read-only Docker volume:
```
/home/vagrant/.kube/ai-devops-platform.config
        ↓
/app/.kube/config
```
The current development cluster is the Vagrant-based Kubernetes cluster used by the project.

Supported Kubernetes functionality includes:

- Cluster/resource inspection
- Deployment inspection
- Deployment restart actions

## DevOps Action Flow

Supported actions follow this general flow:
```
User Request
     |
     v
AI Action Interpretation
     |
     v
Action Intent
     |
     v
User Execution
     |
     v
DevOps Service
     |
     +-------------------+
     |                   |
     v                   v
   Docker           Kubernetes
     |                   |
     +---------+---------+
               |
               v
          Action Result
               |
               v
         Action History
```

AI interpretation and action execution are separate steps. The user explicitly triggers execution of the interpreted action.

## Persistence

PostgreSQL stores application data including:

- Users
- Roles
- Projects
- AI analysis records
- DevOps action records
- Related application metadata

SQLAlchemy is used for database access.

Alembic manages database migrations.

Migration files are located under:
```
alembic/
migrations/
```

## Redis

Redis is available as a backend runtime dependency.

The Docker Compose configuration connects the backend to the Redis service through the internal Compose network.

## Configuration

Runtime configuration is managed using Pydantic Settings.

Configuration includes:

- Application settings
- API settings
- Database settings
- Redis settings
- AI provider settings
- Kubernetes settings
- Security settings
- CORS settings
- Logging and observability settings

For local development, use:
```
backend/.env
```
The environment file is intentionally excluded from Git.

A safe configuration template is provided as:
```
backend/.env.example
```
Never commit local .env files or real credentials.

## Running the Backend with Docker Compose

The recommended project-level workflow is to run the backend through Docker Compose from the repository root:
```
docker compose up -d --build
```
Check the backend:
```
docker compose ps
```
Test the API:
```
curl -s http://localhost:8000/api/v1/health | python3 -m json.tool
```
Test dependencies:
```
curl -s http://localhost:8000/api/v1/health/dependencies \
  | python3 -m json.tool
```
### Standalone Local Development

A Python virtual environment can be created when standalone backend development is required:
```
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```
Start FastAPI directly:
```
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --app-dir src
```
The virtual environment is local-only and is ignored by Git.

## Database Migrations

Alembic is used for database migrations.

From the backend directory:
```
alembic upgrade head
```
Migration configuration is provided by:
```
alembic.ini
```

## Tests

The backend contains tests for authentication and health functionality.

Run:
```
cd backend
pytest
```

The project keeps testing lightweight because the platform is intended as a local demonstration environment.

## Utility Scripts

The backend contains small utility scripts under:
```
scripts/
```
Current scripts include:
```
create_admin.py
test_ai.py
```
create_admin.py is used to create the local administrative user required for the demonstration environment.

## Resource-Constrained Design

The backend is designed to operate in a lightweight local environment.

The project intentionally avoids additional persistent infrastructure such as:

- Prometheus
- Grafana
- Alertmanager
- Additional AI model servers
- Additional database servers
- Additional Kubernetes workloads

Ollama runs on the host and uses the lightweight llama3.2:3b model.

## Development Notes

The backend is the central integration point between:
```
React Frontend
      |
      v
   FastAPI
   /  |  \
  /   |   \
 DB  Redis Ollama
       |
       +---- Docker
       |
       +---- Kubernetes
```

The backend is therefore responsible for connecting AI-assisted workflows with real DevOps operations while keeping the implementation simple enough to run on a constrained development machine.
