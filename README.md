# 🚀 AI DevOps Platform

An AI-assisted DevOps platform that combines **AI Engineering, application development, Docker, and Kubernetes** into a practical end-to-end workflow.

The platform allows users to:

- Interact with a local AI assistant for DevOps questions.
- Analyze Dockerfiles, Kubernetes configurations, Terraform configurations, and logs.
- Translate natural-language DevOps requests into structured action intents.
- Execute supported Docker and Kubernetes operations through deterministic backend services.
- Review AI analysis and DevOps action history.
- Monitor basic application and dependency health.

The project is designed as a **portfolio and learning project** that demonstrates how AI capabilities can be integrated into practical DevOps workflows.

---

## 📌 Why This Project?

Modern DevOps platforms increasingly combine automation, observability, cloud infrastructure, and AI-assisted workflows.

This project explores a practical implementation of that idea without building an unnecessarily large platform.

The central design principle is:

> **AI assists with understanding and decision-making, while deterministic
> backend services remain responsible for executing DevOps operations.**

For example:

```
User
 |
 | "Restart the ingress-nginx-controller deployment"
 v
AI Assistant
 |
 v
AI Action Interpretation
 |
 v
Structured Action Intent
 |
 v
User Confirmation
 |
 v
Backend Action Service
 |
 v
Kubernetes API
 |
 v
Deployment Restart
```
The Kubernetes operation can then be independently verified using
```kubectl```.

---

## 🎯 Key Capabilities
### AI Assistant

The platform provides an AI-powered DevOps assistant using a local Ollama model.

Current default model:
```
llama3.2:3b
```
The assistant supports:

* General DevOps chat
* Dockerfile analysis
* Kubernetes analysis
* Terraform analysis
* Log analysis
* DevOps action interpretation

### AI-Assisted DevOps Actions

The platform can interpret natural-language operational requests and map them to supported DevOps actions.

Example:
```
Restart the ingress-nginx-controller deployment in the ingress-nginx namespace.
```
The AI can identify:
```
Action:
kubernetes_restart_deployment

Target:
ingress-nginx-controller

Namespace:
ingress-nginx
```
The user then explicitly confirms the operation.

The backend validates and executes the supported action.

This creates a clear separation:
```
AI
 |
 | interpretation
 v
Structured Intent
 |
 | validation
 v
Action Catalog
 |
 | execution
 v
DevOps Service
 |
 +---- Docker
 |
 +---- Kubernetes
```
### Kubernetes Integration

The backend integrates with the Vagrant-based Kubernetes cluster through the Kubernetes Python client.

The demonstrated workflow includes:
```
kubernetes_restart_deployment
```
The project has been tested by restarting:
```
Namespace:
ingress-nginx

Deployment:
ingress-nginx-controller
```
The operation was independently verified using:
```
kubectl -n ingress-nginx rollout status \
  deployment/ingress-nginx-controller
```
with a successful rollout.

### Docker Integration

The backend integrates with the Docker Engine using the Docker SDK for Python.

The backend container receives access to the host Docker daemon through:
```
/var/run/docker.sock
```
This allows supported Docker operations to be performed without running a second Docker daemon inside the application container.

### Analysis and Action History

AI analysis results and executed DevOps actions are persisted in PostgreSQL.

This allows the platform to retain:

* AI analysis results
* Action information
* Targets
* Execution status
* Execution timestamps
* Results/messages

The history is exposed through the application interface.

---

## 🏗 Architecture
                              User
                               |
                               v
                     +-------------------+
                     | React + TypeScript|
                     |      Frontend     |
                     +---------+---------+
                               |
                               | HTTP / REST
                               v
                     +-------------------+
                     |   FastAPI Backend |
                     +---------+---------+
                               |
             +-----------------+------------------+
             |                 |                  |
             v                 v                  v
       +-----------+     +-----------+      +-----------+
       | PostgreSQL|     |   Redis   |      |  Ollama  |
       +-----------+     +-----------+      +-----+-----+
                                                  |
                                                  v
                                            llama3.2:3b

                               |
                               v
                     +-------------------+
                     | DevOps Services   |
                     +---------+---------+
                               |
                     +---------+---------+
                     |                   |
                     v                   v
                 Docker              Kubernetes
                 Engine                 API

The application services run through Docker Compose.

Ollama runs locally on the development host.

The Kubernetes integration connects to the Vagrant Kubernetes cluster.

----

## 🧰 Technology Stack
|Area|Technology|
|----|----------|
|Frontend|React|
|Language|TypeScript|
|Frontend Build|Vite|
|Styling|Tailwind CSS|
|Backend|FastAPI|
|Language|Python|
|ORM|SQLAlchemy|
|Database|PostgreSQL|
|Database Migrations|Alembic|
|Cache/Runtime Dependency|Redis|
|Authentication|JWT|
|AI Runtime|Ollama|
|AI Model|llama3.2:3b|
|AI Provider Abstraction|Ollama/OpenAI providers|
|Containers|Docker|
|Local Orchestration|Docker Compose|
|Container Web Server|Nginx|
|Docker Integration|Docker SDK for Python|
|Kubernetes Integration|Kubernetes Python Client|
|Kubernetes Environment|Vagrant|
|API Documentation|FastAPI/OpenAPI|

---

## 🏗 AI Architecture

The AI layer uses a provider abstraction rather than coupling the application directly to one AI implementation.
```
AI Service
    |
    v
Provider Factory
    |
    +---- Ollama Provider
    |
    +---- OpenAI Provider
```
The default local configuration uses:
```
Provider: Ollama
Model:    llama3.2:3b
```
The frontend communicates with FastAPI, and FastAPI communicates with the selected AI provider.

The frontend does not communicate directly with Ollama.

Detailed documentation:

* AI Workflows - [`docs/ai-workflows.md`](docs/ai-workflows.md)

---

## 🔄 DevOps Execution Model

A key architectural decision is to keep AI interpretation separate from infrastructure execution.
```
Natural Language
      |
      v
AI Interpretation
      |
      v
Structured Action
      |
      v
User Confirmation
      |
      v
Action Validation
      |
      v
Deterministic Backend Service
      |
      +--------+---------+
      |                  |
      v                  v
   Docker           Kubernetes
```
This avoids treating arbitrary model-generated text as a shell command.

The backend controls which operations are actually executable.

Detailed documentation:

* DevOps Actions - [`docs/devops-actions.md`](docs/devops-actions.md)

---

## ⚙️ Application Services

The current Docker Compose environment contains four application services:
```
ai-devops-frontend
ai-devops-backend
ai-devops-postgres
ai-devops-redis
```
Ollama runs separately on the host.

Check the application:
```
docker compose ps
```
Expected host ports:

|Component	|Port|
|----------|----|
|Frontend	|8080|
|Backend	|8000|
|PostgreSQL	|5433|
|Redis	|6380|

---

## 📂 Repository Structure

The repository intentionally contains only the components used by the current implementation.
```
ai-devops-platform/
├── .gitignore
├── .env.example
├── LICENSE
├── README.md
├── docker-compose.yml
│
├── backend/
│   ├── Dockerfile
│   ├── README.md
│   ├── pyproject.toml
│   ├── alembic/
│   ├── migrations/
│   ├── scripts/
│   ├── src/
│   └── tests/
│
├── frontend/
│   ├── Dockerfile
│   ├── README.md
│   ├── package.json
│   ├── public/
│   └── src/
│
└── docs/
    ├── architecture.md
    ├── setup.md
    ├── ai-workflows.md
    ├── devops-actions.md
    └── demo.md
```
The repository was deliberately cleaned up during the final project phase to remove unused initial scaffolding and empty infrastructure placeholders.

---

## 🔥 Quick Start
1. Clone
```
git clone <repository-url>
cd ai-devops-platform
```
2. Start Ollama

Verify Ollama:
```
ollama --version
```
Verify the model:
```
ollama list
```
The project uses:
```
llama3.2:3b
```
3. Start the Application
```
docker compose up -d --build
```
Check:
```
docker compose ps
```
4. Verify Backend
```
curl -s http://localhost:8000/api/v1/health \
  | python3 -m json.tool
```
Then:
```
curl -s http://localhost:8000/api/v1/health/dependencies \
  | python3 -m json.tool
```
Expected dependency status:
```
database: healthy
redis: healthy
ollama: healthy
```
5. Open the Frontend

Open:
```
http://localhost:8080
```
After authentication, navigate to the AI Assistant.

---

## ☸️ Kubernetes Demo

The Kubernetes portion requires the Vagrant cluster.

Verify:
```
kubectl get nodes
```
Expected:
```
master    Ready
worker    Ready
```
Then verify:
```
kubectl -n ingress-nginx get deployment \
  ingress-nginx-controller
```
The AI Assistant can then be used to request:
```
Restart the ingress-nginx-controller deployment in the ingress-nginx namespace.
```
Review the interpreted action and select:
```
Execute Action
```
Verify the resulting rollout:
```
kubectl -n ingress-nginx rollout status \
  deployment/ingress-nginx-controller
```
Detailed demonstration instructions:

* Demo Guide - [`docs/demo.md`](docs/demo.md)

---

## 🔵 Backend Development

Backend-specific documentation is available in:

* Backend README - [`backend/README.md`](backend/README.md)

The backend uses:
```
FastAPI
SQLAlchemy
Alembic
asyncpg
Redis
JWT
Docker SDK
Kubernetes Python Client
```
Run backend tests:
```
cd backend
pytest
```
---

## ⚙️ Frontend Development

Frontend-specific documentation is available in:

* Frontend README - [`frontend/README.md`](frontend/README.md)

The frontend uses:
```
React
TypeScript
Vite
Tailwind CSS
React Router
Axios
```
Build the frontend:
```
cd frontend
npm ci
npm run build
```
Run linting:
```
npm run lint
```
---

## 🌐 Docker Compose

The current application environment is intentionally small:
```
Docker Compose
├── PostgreSQL
├── Redis
├── FastAPI Backend
└── React + Nginx Frontend
```
The frontend uses a multistage Docker build:
```
Node.js
   |
   | npm ci
   | npm run build
   v
Static React application
   |
   v
Nginx
```
The backend runs FastAPI with Uvicorn.

---

## 📊 Health Checks

The platform provides lightweight application health endpoints.

Application health:
```
GET /api/v1/health
```
Dependency health:
```
GET /api/v1/health/dependencies
```
The dependency endpoint currently checks:
```
PostgreSQL
Redis
Ollama
```
This provides basic operational visibility without introducing a separate monitoring stack.

---

## 📦 Resource-Conscious Design

The project is intentionally designed to run on a constrained local development environment.

The final implementation does not require additional heavyweight infrastructure such as:

* Prometheus
* Grafana
* Alertmanager
* Helm runtime
* Terraform runtime infrastructure
* Additional AI models
* Additional databases
* Additional Kubernetes clusters

These technologies were considered during the initial project design, but they are not required by the implemented application.

Keeping them out of the runtime environment reduces memory usage and keeps the project focused on its primary demonstration:
```
AI Engineering
        +
Application Development
        +
DevOps Automation
```

---

## 🔐 Security Scope

This is a controlled portfolio and demonstration environment.

The project is not intended to be deployed directly as a production enterprise control plane.

The backend has access to:

- Docker through ```/var/run/docker.sock```
- Kubernetes through a mounted kubeconfig
- Application secrets through local environment configuration

Therefore:

- Keep the environment on a trusted development machine.
- Do not expose the Docker socket to untrusted applications.
- Protect the Kubernetes kubeconfig.
- Do not commit ```.env``` files.
- Replace development secrets before any non-local deployment.
- Treat the current authorization model as demonstration-level rather than enterprise-grade infrastructure authorization.

---

## 📝 Documentation

Detailed project documentation:

|Document	|Purpose|
|---------|-------|
|Architecture	|System architecture and component relationships|
|Setup Guide	|Installation, startup, verification and troubleshooting|
|AI Workflows	|AI provider, prompts, analysis and action interpretation|
|DevOps Actions	|Docker/Kubernetes execution model and action history|
|Demo Guide	|10–15 minute portfolio/interview demonstration|
|Backend README	|Backend-specific development information|
|Frontend README	|Frontend-specific development information|

---

## 🎯 Project Highlights

This project demonstrates several practical engineering concepts in one workflow:

### AI Engineering
- Local LLM integration
- Provider abstraction
- Prompt engineering
- Structured AI responses
- AI-assisted DevOps analysis
- Natural-language action interpretation

### Backend Engineering
- FastAPI
- Async database access
- SQLAlchemy
- Alembic migrations
- Redis
- JWT authentication
- Service and repository layers
- Health and dependency checks

### Frontend Engineering
- React
- TypeScript
- Vite
- Tailwind CSS
- API integration
- AI assistant UI
- Action confirmation
- History views

### DevOps Engineering
- Docker
- Docker Compose
- Docker SDK
- Kubernetes Python Client
- Vagrant Kubernetes cluster
- Containerized frontend
- Containerized backend
- Operational health verification

---

## 💡 Project Scope

The project deliberately focuses on demonstrating a working AI-enabled DevOps workflow.

It is not intended to demonstrate every possible DevOps technology in a single repository.

The current scope prioritizes:
```
Working AI workflows
        |
        v
Real application integration
        |
        v
Controlled DevOps actions
        |
        v
Kubernetes verification
        |
        v
Clear documentation
```
This keeps the project understandable, reproducible and suitable for portfolio and interview demonstrations.

---

## 🧠 Current Status

The implementation and engineering work are complete.

The project has progressed through:
```
Authentication
      |
Backend Foundation
      |
AI Provider Integration
      |
React Frontend
      |
Dockerization
      |
AI Analysis Workflows
      |
DevOps Actions
      |
Kubernetes Integration
      |
Action History
      |
Health / Reliability
      |
Repository Cleanup
      |
Documentation
      |
Final Portfolio Packaging
```
The final project demonstrates an end-to-end workflow from:
```
Natural-language request
        |
        v
AI interpretation
        |
        v
User confirmation
        |
        v
Backend execution
        |
        v
Real DevOps operation
        |
        v
Independent verification
        |
        v
Persisted history
```

---

## 📈 Future Extensions

Possible future improvements include:

- Additional controlled DevOps actions.
- More sophisticated AI response validation.
- Expanded observability.
- Additional AI providers.
- Cloud deployment.
- More comprehensive authorization.
- Production-grade secrets management.
- Automated CI/CD deployment environments.

These are intentionally outside the current project's required scope.

---

## 📄 License

This project is licensed under the terms defined in LICENSE.

---

## 🏁 Portfolio Summary

AI DevOps Platform is a practical AI Engineering and DevOps projectthat demonstrates how a local LLM can be integrated into a real application and connected to controlled infrastructure operations.

The strongest part of the project is the boundary between AI and execution:
```
AI understands the request.
        |
        v
Backend validates the intent.
        |
        v
Deterministic DevOps services execute it.
        |
        v
The infrastructure result is independently verified.
```
This demonstrates AI not as an isolated chatbot, but as an integrated component of a practical DevOps workflow.
