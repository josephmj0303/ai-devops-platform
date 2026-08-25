# AI DevOps Platform — Architecture

## 1. Overview

The AI DevOps Platform is a lightweight DevOps operations platform that combines AI-assisted analysis with practical DevOps automation.

The platform provides a web interface where users can:

- Interact with an AI assistant.
- Analyze Dockerfiles, Kubernetes configurations, Terraform configurations, and logs.
- Ask the AI to interpret DevOps actions.
- Execute supported DevOps actions against Docker and Kubernetes.
- Review previously executed actions.
- Monitor application and dependency health.

The project is intentionally designed as a practical demonstration platform rather than a production-scale enterprise platform.

---

## 2. High-Level Architecture

```text
                           User / Browser
                                |
                                v
                    +-----------------------+
                    | React + Vite          |
                    | Nginx Container       |
                    | Port 8080             |
                    +-----------+-----------+
                                |
                                | REST API
                                v
                    +-----------------------+
                    | FastAPI Backend       |
                    | Port 8000             |
                    +-----------+-----------+
                                |
              +-----------------+------------------+
              |                 |                  |
              v                 v                  v
       +-------------+   +-------------+   +---------------+
       | PostgreSQL  |   | Redis       |   | Ollama        |
       | Port 5433   |   | Port 6380   |   | Host :11434   |
       +-------------+   +-------------+   +---------------+
                                                 |
                                                 v
                                           llama3.2:3b
                                                 |
                                                 v
                                      AI analysis / reasoning
                                                 |
                              +------------------+------------------+
                              |                                     |
                              v                                     v
                       Docker Integration                  Kubernetes Integration
                              |                                     |
                              v                                     v
                     Docker Engine                         Vagrant Kubernetes
                                                           Cluster
3. Runtime Components
Frontend

The frontend is implemented using:

React
TypeScript
Vite
Tailwind CSS
React Router
Axios
React Query

The frontend is built using a multistage Dockerfile.

The first stage uses Node.js to install dependencies and build the application.

The second stage uses Nginx to serve the generated static files.

The frontend is exposed on:

http://localhost:8080

The frontend communicates with the backend API at:

http://192.168.56.20:8000/api/v1

The backend address is appropriate for the current Vagrant-based development environment.

4. Backend

The backend is implemented using:

Python
FastAPI
SQLAlchemy
Alembic
Pydantic Settings
PostgreSQL
Redis
Docker SDK
Kubernetes Python client

The backend exposes REST APIs under:

/api/v1

The API is served by Uvicorn on:

0.0.0.0:8000

The backend is containerized using its own Dockerfile and managed by Docker Compose.

5. PostgreSQL

PostgreSQL provides persistent application storage.

The Docker Compose service uses:

Image: postgres:17
Container: ai-devops-postgres
Host port: 5433
Container port: 5432
Database: ai_devops

A named Docker volume is used for PostgreSQL persistence:

postgres_data

The backend connects to PostgreSQL through the internal Docker Compose network.

6. Redis

Redis provides the application's Redis-based runtime dependency.

The Docker Compose service uses:

Image: redis:7-alpine
Container: ai-devops-redis
Host port: 6380
Container port: 6379

The backend connects to Redis through the internal Docker Compose network.

Redis is intentionally kept lightweight for the project's development and demonstration environment.

7. AI Provider

The project uses Ollama as the primary local AI provider.

Current model:

llama3.2:3b

Ollama runs directly on the host rather than inside Docker.

The backend container reaches the host Ollama service through:

http://host.docker.internal:11434

This approach avoids running another memory-intensive container.

The AI provider abstraction also contains support for OpenAI configuration, but the current project uses Ollama for local development and demonstration.

8. AI Capabilities

The AI layer supports several DevOps-oriented workflows:

AI Assistant

Users can interact with the AI assistant through the frontend.

Dockerfile Analysis

The platform can analyze Dockerfiles and return findings and recommendations.

Kubernetes Analysis

The platform can analyze Kubernetes-related input and provide operational recommendations.

Terraform Analysis

The platform can analyze Terraform configuration and provide findings and recommendations.

Terraform is used here as an AI analysis capability. The current project does not use Terraform to provision the platform infrastructure.

Log Analysis

The platform can analyze log input and identify potential issues and recommended actions.

AI Action Interpretation

The AI can interpret an operational request and determine whether it maps to a supported DevOps action.

9. DevOps Integration

The backend integrates directly with DevOps tooling.

Docker

The Docker SDK is used by the backend for supported Docker operations.

The backend container has access to the host Docker daemon through:

/var/run/docker.sock

This allows the platform to perform supported Docker operations without running a separate Docker daemon inside the backend container.

Kubernetes

The backend uses the Kubernetes Python client.

The development Kubernetes configuration is mounted into the backend container:

/home/vagrant/.kube/ai-devops-platform.config
        |
        v
/app/.kube/config

The current Kubernetes environment is a lightweight Vagrant-based cluster consisting of:

master
worker

The platform can inspect Kubernetes resources and execute supported actions such as restarting a deployment.

10. AI Action Execution Flow

A supported operational workflow follows this pattern:

User Request
     |
     v
AI Action Interpretation
     |
     v
Action Intent
     |
     v
User Executes Action
     |
     v
DevOps Service
     |
     +--------------------+
     |                    |
     v                    v
   Docker             Kubernetes
     |                    |
     +---------+----------+
               |
               v
        Action Result
               |
               v
        Action History

The system separates AI interpretation from actual execution.

The AI can identify an appropriate action, but the frontend provides an explicit execution step for the supported action.

11. Action History

Executed DevOps actions are persisted as action history.

The history provides visibility into:

Action type
Target
Execution status
Execution time
Result/message

For example, a Kubernetes deployment restart can be recorded as:

Action:
kubernetes_restart_deployment

Target:
ingress-nginx/ingress-nginx-controller

Result:
Kubernetes deployment restarted successfully

This provides an operational record of actions executed through the platform.

12. Health and Dependency Checks

The backend provides lightweight application observability through health endpoints.

Application health
GET /api/v1/health

Example response:

{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "local"
}
Dependency health
GET /api/v1/health/dependencies

The dependency endpoint checks:

PostgreSQL
Redis
Ollama

Example:

{
  "status": "ready",
  "checks": {
    "database": "healthy",
    "redis": "healthy",
    "ollama": "healthy"
  }
}

This lightweight approach is intentional. The project does not run a separate Prometheus/Grafana monitoring stack.

13. Docker Compose Architecture

Docker Compose manages four application services:

postgres
redis
backend
frontend

The current Compose topology is:

Docker Compose
|
+-- postgres
|     |
|     +-- postgres:17
|
+-- redis
|     |
|     +-- redis:7-alpine
|
+-- backend
|     |
|     +-- FastAPI
|     +-- Docker SDK
|     +-- Kubernetes Client
|     +-- Ollama integration
|
+-- frontend
      |
      +-- Nginx
      +-- React static files

The frontend is now part of the same Compose workflow as the backend, PostgreSQL, and Redis.

The entire application stack can therefore be started with:

docker compose up -d --build
14. Network and External Dependencies

The Docker Compose services communicate using the internal Compose network.

The backend additionally communicates with:

Host Ollama
Vagrant Kubernetes cluster
Host Docker daemon

The high-level dependency flow is:

Frontend
   |
   v
Backend
   |
   +----> PostgreSQL
   |
   +----> Redis
   |
   +----> Host Ollama
   |
   +----> Docker daemon
   |
   +----> Kubernetes API
15. Resource-Constrained Design

The project is intentionally designed to operate on a constrained development host.

The following choices reduce unnecessary resource consumption:

Ollama runs directly on the host.
A small local model is used (llama3.2:3b).
PostgreSQL uses a single lightweight container.
Redis uses the Alpine image.
The frontend uses Nginx for static file serving.
No additional monitoring stack is required.
No additional Kubernetes workloads are required for the application.
The project does not run Terraform, Helm, Prometheus, Grafana, or Alertmanager as persistent services.

The goal is to demonstrate AI Engineering integrated with DevOps operations without requiring production-scale infrastructure.

16. Technologies
Application
React
TypeScript
Vite
Tailwind CSS
FastAPI
Python
SQLAlchemy
Alembic
Data and Runtime
PostgreSQL
Redis
Docker
Docker Compose
Nginx
AI
Ollama
llama3.2:3b
DevOps Integration
Docker SDK
Kubernetes Python Client
Kubernetes
Vagrant
17. Scope

This project focuses on demonstrating the integration of AI with DevOps workflows.

It intentionally does not attempt to implement a complete enterprise platform.

The final implementation prioritizes:

Working AI workflows
Practical DevOps integration
Kubernetes operations
Docker operations
Persistent action history
Health checks
Simple local deployment
Clear documentation
A repeatable demonstration workflow

Technologies from the original project concept that are not part of the final implementation are intentionally excluded from the runtime architecture.
