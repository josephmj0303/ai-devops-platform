# Setup and Runbook

This document describes how to run the AI DevOps Platform in the local development environment used by this project.

The platform is intentionally lightweight and is designed to demonstrate AI-assisted DevOps workflows without requiring production-scale infrastructure.

## 1. Architecture Overview

The local environment consists of:

```
Host
├── Ollama
│   └── llama3.2:3b
│
├── Docker Compose
│   ├── PostgreSQL
│   ├── Redis
│   ├── FastAPI Backend
│   └── React + Nginx Frontend
│
└── Vagrant Kubernetes Cluster
    ├── master
    └── worker
```
The backend communicates with:

- PostgreSQL
- Redis
- Ollama
- Docker through the host Docker socket
- Kubernetes through the mounted kubeconfig

## 2. Prerequisites

The development environment requires:

- Linux host
- Docker
- Docker Compose
- Git
- Python 3.11+
- Node.js 22+ for standalone frontend development
- Ollama
- Vagrant
- VirtualBox
- Kubernetes cluster for Kubernetes workflows

The main application can be run through Docker Compose without creating Python or Node.js virtual environments on the host.

## 3. Clone the Repository
```
git clone https://github.com/josephmj0303/ai-devops-platform
cd ai-devops-platform
```
## 4. Environment Configuration

Local environment files are intentionally excluded from Git.

The repository provides:
```
.env.example
backend/.env.example
```
Create the backend environment file if standalone backend development is required:
```
cp backend/.env.example backend/.env
```
The Docker Compose configuration provides the environment required by the containerized backend directly.

Do not commit local .env files.

## 5. Ollama

The project uses Ollama as the local AI provider.

Verify Ollama:
```
ollama --version
```
Verify that the required model exists:
```
ollama list
```
The project uses:
```
llama3.2:3b
```
If the model is not available:
```
ollama pull llama3.2:3b
```
Verify the Ollama API:
```
curl http://localhost:11434/api/tags
```
The backend container reaches Ollama through:
```
http://host.docker.internal:11434
```

## 6. Kubernetes Development Cluster

Kubernetes workflows use the project's Vagrant-based cluster.

Expected nodes:
```
master
worker
```
Verify the cluster:
```
kubectl get nodes
```
Both nodes should be Ready.

Check workloads:
```
kubectl get pods -A
kubectl get deployments -A
```
The backend uses the kubeconfig:
```
/home/vagrant/.kube/ai-devops-platform.config
```
Docker Compose mounts this file into the backend container as:
```
/app/.kube/config
```

## 7. Start the Platform

From the repository root:
```
docker compose up -d --build
```
Check all services:
```
docker compose ps
```
Expected services:
```
ai-devops-postgres
ai-devops-redis
ai-devops-backend
ai-devops-frontend
```
Expected ports:

| Service | Host Port |
| ------- | --------- |
| PostgreSQL | 5433 |
| Redis | 6380 |
| Backend | 8000 |
| Frontend | 8080 |

## 8. Verify Backend Health

Application health:
```
curl -s http://localhost:8000/api/v1/health \
  | python3 -m json.tool
```
Expected result:
```
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "local"
}
```
Check dependencies:
```
curl -s http://localhost:8000/api/v1/health/dependencies \
  | python3 -m json.tool
```
Expected result:
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

## 9. Verify API Documentation

FastAPI provides interactive documentation at:
```
http://localhost:8000/docs
```
OpenAPI JSON is available at:
```
http://localhost:8000/openapi.json
```

## 10. Verify Frontend

Open:
```
http://localhost:8080
```
The login page should be displayed.

After authentication, the main application provides:

- Dashboard
- Projects
- AI DevOps Assistant

## 11. Create the Demo Administrator

The backend includes:
```
backend/scripts/create_admin.py
```
The script can be used to create the local administrator required for the demonstration environment.

Run it from the backend environment according to the project's current database configuration.

Do not use demo credentials outside the local demonstration environment.

## 12. Frontend Standalone Development

For frontend-only development:
```
cd frontend
npm ci
npm run dev
```
Build the production frontend:
```
npm run build
```
Run linting:
```
npm run lint
```

## 13. Backend Standalone Development

For backend-only development:
```
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```
Start FastAPI:
```
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --app-dir src
```
Run tests:
```
pytest
```
Run linting:
```
ruff check src tests
```

## 14. Useful Docker Commands

View services:
```
docker compose ps
```
View backend logs:
```
docker compose logs -f backend
```
View frontend logs:
```
docker compose logs -f frontend
```
View PostgreSQL logs:
```
docker compose logs -f postgres
```
View Redis logs:
```
docker compose logs -f redis
```
Restart the platform:
```
docker compose restart
```
Rebuild after source or Dockerfile changes:
```
docker compose up -d --build
```
Stop the platform:
```
docker compose down
```
The PostgreSQL named volume is retained by docker compose down.

## 15. Kubernetes Verification

Before demonstrating Kubernetes-related functionality:
```
kubectl get nodes
kubectl get pods -A
kubectl get deployments -A
```
The Kubernetes cluster should be healthy enough for the required demonstration workflow.

For example:
```
kubectl -n ingress-nginx get deployment ingress-nginx-controller
```
After a deployment restart:
```
kubectl -n ingress-nginx rollout status \
  deployment/ingress-nginx-controller
```

## 16. Resource-Conscious Operation

The development host has limited memory, so the project intentionally keeps the runtime environment small.

Do not start unnecessary infrastructure.

The current demonstration environment does not require:

- Prometheus
- Grafana
- Alertmanager
- Helm deployment
- Terraform runtime infrastructure
- Additional AI models
- Additional databases
- Additional Kubernetes clusters

When running the complete demonstration environment, avoid starting unrelated VMs or resource-heavy workloads.

The existing lightweight Ollama model is sufficient for the project's AI demonstrations.

## 17. Troubleshooting
#### Backend is not starting

Check:
```
docker compose ps
docker compose logs backend
```
Then verify:
```
curl http://localhost:8000/api/v1/health
```
#### PostgreSQL is unavailable

Check:
```
docker compose ps postgres
docker compose logs postgres
```
The backend connects to PostgreSQL through the Docker Compose service name:
```
postgres:5432
```
The host-side PostgreSQL port is:
```
5433
```
#### Redis is unavailable

Check:
```
docker compose ps redis
docker compose logs redis
```
The backend connects through:
```
redis:6379
```
The host-side Redis port is:
```
6380
```

#### Ollama is unavailable

Verify:
```
curl http://localhost:11434/api/tags
```
Then check:
```
ollama list
```
The backend dependency health endpoint should report:
```
ollama: healthy
```
#### Kubernetes actions fail

Verify the cluster:
```
kubectl get nodes
```
Verify the kubeconfig exists:
```
ls -l ~/.kube/ai-devops-platform.config
```
Verify the backend container has the mounted configuration:
```
docker exec ai-devops-backend ls -l /app/.kube/config
```

#### Frontend cannot reach the backend

Verify the backend:
```
curl http://localhost:8000/api/v1/health
```
Verify the frontend container:
```
docker compose ps frontend
```
Then inspect:
```
docker compose logs frontend
```
The frontend currently uses the development backend address configured in **frontend/src/api/axios.ts**.

## 18. Shutdown

Stop the application:
```
docker compose down
```
If the Vagrant Kubernetes cluster was started specifically for the demonstration, it can be stopped separately:
```
vagrant halt
```
Start it again when Kubernetes functionality is required.

## 19. Clean Rebuild

When a clean application rebuild is required:
```
docker compose down
docker compose build --no-cache
docker compose up -d
```
Use --no-cache only when necessary because it consumes additional CPU, disk I/O, and build time.

## 20. Normal Development Workflow

A typical development session is:
```
1. Start Ollama
        |
2. Start Kubernetes only if required
        |
3. docker compose up -d
        |
4. Check /health
        |
5. Check /health/dependencies
        |
6. Open frontend
        |
7. Run AI / DevOps demonstration
        |
8. Review action or analysis history
        |
9. Stop unnecessary services
```
The project is intended to remain simple enough to reproduce locally without requiring a large platform stack.
