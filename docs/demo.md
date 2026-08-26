# Portfolio and Interview Demo

This document provides a repeatable demonstration flow for the AI DevOps Platform.

The goal is to demonstrate how AI Engineering is integrated with practical DevOps workflows rather than simply demonstrating a chatbot.

The recommended demonstration takes approximately 10–15 minutes.

---

## 1. Demo Objective

The central story of the project is:

> An AI-assisted DevOps platform that analyzes DevOps information,
> understands natural-language operational requests, and connects those
> requests to controlled Docker and Kubernetes actions.

The demonstration should make three things clear:

1. AI is integrated into a real application.
2. AI can assist with DevOps analysis and operational intent.
3. Actual infrastructure operations are performed by deterministic    backend services.

---

## 2. Architecture to Explain

The simplified architecture is:

```
                    User
                     |
                     v
             React + Vite UI
                     |
                     v
               FastAPI API
                     |
        +------------+------------+
        |            |            |
        v            v            v
   PostgreSQL      Redis         Ollama
                                   |
                                   v
                             llama3.2:3b

                     |
                     v
              DevOps Services
                /         \
               v           v
            Docker     Kubernetes
```
The application runs through Docker Compose.

Ollama runs locally on the host.

The Kubernetes workflows connect to the Vagrant Kubernetes cluster.

## 3. Before the Demo

Start Ollama and verify the model:
```
ollama list
```
Confirm that:
```
llama3.2:3b
```
is available.

If required:
```
ollama pull llama3.2:3b
```
## 4. Start Kubernetes

Kubernetes is only required for the Kubernetes portion of the demo.

Verify the cluster:
```
kubectl get nodes
```
Expected:
```
master    Ready
worker    Ready
```
Then verify the relevant deployment:
```
kubectl -n ingress-nginx get deployment \
  ingress-nginx-controller
```
Expected:
```
READY        1/1
UP-TO-DATE   1
AVAILABLE    1
```
## 5. Start the Application

From the project root:
```
cd ~/ai-devops-platform

docker compose up -d
```
Verify:
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
```
Frontend   http://localhost:8080
Backend    http://localhost:8000
```
## 6. Verify Application Health

Before opening the UI, verify the backend.
```
curl -s http://localhost:8000/api/v1/health \
  | python3 -m json.tool
```
Expected:
```
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "local"
}
```
Then verify dependencies:
```
curl -s http://localhost:8000/api/v1/health/dependencies \
  | python3 -m json.tool
```
Expected:
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
This is a useful point to explain that the platform has lightweight dependency health checking rather than requiring a separate monitoring stack.

## 7. Open the Application

Open:
```
http://localhost:8080
```
Log in using the local demonstration administrator.

After authentication, show:

- Dashboard
- Projects
- AI Assistant

The AI Assistant is the primary area for the technical demonstration.

## 8. Demo Part 1 — Application Overview

Start with a short overview.

Suggested explanation:

**"This is an AI-powered DevOps platform built with React, FastAPI, PostgreSQL, Redis and a local Ollama model. The objective isn't to build another chatbot. The AI layer is connected to actual DevOps workflows, including Docker and Kubernetes operations."**

Then briefly show the application structure.

## 9. Demo Part 2 — AI Assistant

Navigate to:
```
AI Assistant
```
Explain:

**"The AI Assistant is the main interface between the user and the AI capabilities of the platform."**

Demonstrate a normal DevOps question.

For example:
```
Explain what happens when a Kubernetes deployment is restarted.
```
The important point is not the specific answer.

Explain the workflow:
```
React
  |
  v
FastAPI
  |
  v
AI Service
  |
  v
Ollama
  |
  v
llama3.2:3b
  |
  v
Response
```
Emphasize that the frontend does not communicate directly with Ollama.

## 10. Demo Part 3 — DevOps Analysis

Demonstrate one of the analysis workflows.

Possible examples:
```
Dockerfile analysis
```
or:
```
Kubernetes analysis
```
or:
```
Log analysis
```
or:
```
Terraform analysis
```
Explain that these workflows use specialized prompts.

The relevant prompt implementations are located under:
```
backend/src/app/prompts/
```
The AI provides findings and recommendations.

It does not automatically modify the supplied configuration.

## 11. Demo Part 4 — AI Action Interpretation

This is the most important part of the demonstration.

Ask the AI Assistant:
```
Restart the ingress-nginx-controller deployment in the ingress-nginx namespace.
```
The platform should interpret the request as a supported action.

The expected intent is conceptually:
```
Action:
kubernetes_restart_deployment

Target:
ingress-nginx-controller

Namespace:
ingress-nginx
```
Explain:

**"The model isn't executing a shell command. It is translating the natural-language request into a structured action intent."**

This distinction is central to the architecture.

## 12. Demo Part 5 — User Confirmation

Show the action preview.

The user is given an explicit:
```
Execute Action
```
control.

Explain:

**"I intentionally keep a confirmation step between AI interpretation and infrastructure execution."**

This demonstrates that AI interpretation and infrastructure execution are separate stages.

## 13. Demo Part 6 — Execute Kubernetes Action

Select:
```
Execute Action
```
The backend then invokes the Kubernetes service.

The execution path is:
```
AI Intent
    |
    v
Action Catalog
    |
    v
KubernetesService
    |
    v
Kubernetes Python Client
    |
    v
Kubernetes API
    |
    v
Deployment Restart
```
The expected application result is:
```
Kubernetes deployment restarted successfully
```
## 14. Demo Part 7 — Verify the Infrastructure Change

Switch to the Kubernetes terminal.

Check the deployment:
```
kubectl -n ingress-nginx get deployment \
  ingress-nginx-controller
```
Then:
```
kubectl -n ingress-nginx get pods
```
Finally:
```
kubectl -n ingress-nginx rollout status \
  deployment/ingress-nginx-controller
```
Expected:
```
deployment "ingress-nginx-controller" successfully rolled out
```
Explain:

**"The important part of the demonstration is that the AI-generated intent resulted in a real Kubernetes operation, and I can independently verify that operation using kubectl."**

## 15. Demo Part 8 — Action History

Return to the application.

Show the action history.

The recorded operation should contain information such as:
```
Action:
kubernetes_restart_deployment

Target:
ingress-nginx/ingress-nginx-controller

Status:
completed

Result:
Kubernetes deployment restarted successfully
```
Explain:

**"The platform also persists executed actions, so the operational activity isn't lost when the UI session ends."**

## 16. Demo Part 9 — Health and Dependencies

Return to the terminal.

Show:
```
curl -s http://localhost:8000/api/v1/health/dependencies \
  | python3 -m json.tool
```
Explain the three current runtime dependencies:
```
PostgreSQL
Redis
Ollama
```
This demonstrates that the application includes basic operational health visibility without adding a heavyweight monitoring stack.

## 17. Optional API Demonstration

If time permits, open:
```
http://localhost:8000/docs
```
Show the FastAPI Swagger UI.

Explain that the backend exposes versioned APIs under:
```
/api/v1
```
This is useful when the audience is technically oriented.

For a non-technical audience, this section can be skipped.

## 18. Recommended Demo Sequence

The shortest complete demonstration is:
```
1. Show architecture
       |
2. Show running Docker Compose services
       |
3. Verify backend health
       |
4. Open React application
       |
5. Show AI Assistant
       |
6. Ask a DevOps question
       |
7. Demonstrate analysis
       |
8. Request Kubernetes restart
       |
9. Show structured action intent
       |
10. Confirm Execute Action
       |
11. Verify Kubernetes rollout with kubectl
       |
12. Show Action History
```
This sequence demonstrates both the AI Engineering and DevOps sides of the project.

## 19. What to Highlight in an Interview

The following technical points are worth highlighting.

### AI Engineering
- Local LLM integration using Ollama.
- Provider abstraction.
- Prompt separation.
- Structured AI action interpretation.
- AI analysis workflows.
- Separation between AI reasoning and execution.

### Backend
- FastAPI.
- Async PostgreSQL access.
- SQLAlchemy.
- Alembic migrations.
- Redis integration.
- JWT authentication.
- Service/repository separation.
- Health and dependency endpoints.

### Frontend
- React.
- TypeScript.
- Vite.
- React Router.
- API integration with Axios.
- AI Assistant interface.
- Action confirmation workflow.
- Analysis and action history.

### DevOps
- Docker.
- Docker Compose.
- Docker SDK integration.
- Kubernetes Python client.
- Kubernetes deployment operations.
- Vagrant Kubernetes cluster.
- Health verification.
- Containerized frontend and backend.

## 20. Key Architectural Decision to Explain

If asked:

"Why didn't you let the AI execute arbitrary commands?"

Answer:

"Because I wanted a clear separation between AI interpretation and infrastructure execution. The model produces a structured intent. The backend validates that intent against a supported action catalog, and a deterministic service performs the operation. This makes the workflow easier to control, test and demonstrate."

## 21. Key AI Design Decision

If asked:

"Why Ollama instead of a hosted model?"

Answer:

"The project was designed to be reproducible on a local development environment. Ollama allows the core AI workflow to run locally without requiring an external AI API for the main demonstration. I also kept the provider layer abstract so another provider can be selected later."

## 22. Key Infrastructure Decision

If asked:

"Why didn't you add Prometheus, Grafana, Helm and Terraform?"

Answer:

"Those technologies were considered during the initial architecture, but the project scope was intentionally reduced to focus on the demonstrated AI and DevOps workflow. The development environment also has constrained memory, so adding multiple additional infrastructure components would increase resource consumption without materially improving the core demonstration."

The current project therefore focuses on:
```
AI
+
Application
+
Docker
+
Kubernetes
```
rather than trying to demonstrate every DevOps technology in one repository.

## 23. What Not to Claim

The project should not be presented as:

- A production-ready enterprise platform.
- An autonomous remediation engine.
- A complete Kubernetes management platform.
- A full observability platform.
- A Terraform infrastructure provisioning platform.
- A Helm-based deployment platform.
- A production-grade security control plane.
- A large-scale AI agent platform.

Instead, describe it as:
    
"A practical AI-assisted DevOps platform demonstrating AI Engineering integrated with application services, Docker and Kubernetes."

This accurately represents the implemented project.

## 24. Demo Troubleshooting

If the backend is unavailable:
```
docker compose ps
docker compose logs backend
```
If the AI provider is unavailable:
```
curl http://localhost:11434/api/tags
```
If Kubernetes is unavailable:
```
kubectl get nodes
```
If the frontend is unavailable:
```
docker compose ps frontend
docker compose logs frontend
```
If the dependency health check fails:
```
curl -s http://localhost:8000/api/v1/health/dependencies \
  | python3 -m json.tool
```
Fix the failed dependency before continuing with the demonstration.

## 25. Final Demo Story

The complete story can be summarized in one flow:
```
                    Natural Language
                         Request
                            |
                            v
                    +---------------+
                    |  AI Assistant |
                    +-------+-------+
                            |
                            v
                    +---------------+
                    | AI Interpreter|
                    +-------+-------+
                            |
                            v
                    Structured Intent
                            |
                            v
                    User Confirmation
                            |
                            v
                    +---------------+
                    | Action Catalog|
                    +-------+-------+
                            |
                            v
                    +---------------+
                    | DevOps Service|
                    +-------+-------+
                            |
                 +----------+----------+
                 |                     |
                 v                     v
              Docker              Kubernetes
                 |                     |
                 +----------+----------+
                            |
                            v
                     Real Operation
                            |
                            v
                    Verified Result
                            |
                            v
                    Action History
```
The strongest portfolio message is therefore:

**The project connects AI Engineering to real DevOps operations while maintaining a clear boundary between AI-generated intent and deterministic infrastructure execution.**
