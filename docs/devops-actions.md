# DevOps Actions

This document describes how the AI DevOps Platform executes supported DevOps operations.

The platform separates AI interpretation from deterministic DevOps execution.

The AI can identify an intended operation, but actual infrastructure changes are performed by dedicated backend services.

---

## 1. Execution Architecture

The DevOps action workflow is:

```
User Request
     |
     v
AI Interpretation
     |
     v
Structured Action Intent
     |
     v
User Confirmation
     |
     v
Action Validation
     |
     v
DevOps Action Service
     |
     +-------------------+
     |                   |
     v                   v
   Docker           Kubernetes
     |                   |
     v                   v
Docker Engine       Kubernetes API
     |                   |
     +---------+---------+
               |
               v
          Action Result
               |
               v
         Action History
```
This separation is one of the important design characteristics of the project.

The language model does not receive unrestricted access to execute arbitrary shell commands.

## 2. Action Catalog

Supported operations are defined through a DevOps action catalog.

The catalog provides a controlled mapping between an interpreted action and an implementation in the backend.

Examples include:
```
docker_restart
kubernetes_restart_deployment
```
The action catalog is used to determine whether an interpreted request maps to a supported operation.

Conceptually:
```
AI Intent
   |
   v
Action Name
   |
   v
Action Catalog
   |
   +---- Supported ----> Execute
   |
   +---- Unsupported --> Do not execute
```
## 3. User Confirmation

The platform does not immediately execute a DevOps operation merely because the AI interpreted a request.

The frontend displays the interpreted action first.

For an executable action, the user is presented with an:
```
Execute Action
```
control.

The execution flow is therefore:
```
Natural-language request
          |
          v
      AI interprets
          |
          v
     Action preview
          |
          v
     User confirms
          |
          v
       Execute
```
This provides an explicit boundary between AI reasoning and infrastructure modification.

## 4. Docker Integration

Docker operations are implemented using the Docker SDK for Python.

The backend container receives access to the host Docker daemon through:
```
/var/run/docker.sock
```
The architecture is:
```
FastAPI Backend
      |
      v
Docker Service
      |
      v
Docker SDK
      |
      v
/var/run/docker.sock
      |
      v
Host Docker Engine
```
No Docker daemon is started inside the backend container.

This keeps the implementation lightweight and allows the backend to operate on the same Docker environment that runs the application.

## 5. Kubernetes Integration

Kubernetes operations are implemented using the Kubernetes Python client.

The backend receives a read-only kubeconfig through Docker Compose:
```
Host:

/home/vagrant/.kube/ai-devops-platform.config

        |
        | read-only mount
        v

Container:

/app/.kube/config
```
The Kubernetes service uses this configuration to communicate with the development cluster.

The current cluster is the Vagrant-based Kubernetes environment:
```
master
worker
```
## 6. Kubernetes Action Flow

A Kubernetes action follows:
```
User Request
     |
     v
AI Interpretation
     |
     v
kubernetes_restart_deployment
     |
     v
Target Validation
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
Deployment Operation
     |
     v
Execution Result
```
The AI does not directly communicate with the Kubernetes API.

## 7. Kubernetes Deployment Restart

One of the demonstrated actions is:
```
kubernetes_restart_deployment
```
The action accepts a deployment target and, when required, its namespace.

Example target:
```
Namespace:
ingress-nginx

Deployment:
ingress-nginx-controller
```
The resulting Kubernetes operation causes the deployment to roll out a new pod.

## 8. Demonstrated Kubernetes Workflow

The project has been tested end-to-end using the ingress-nginx-controller deployment.

The workflow was:
```
User
 |
 | Restart ingress-nginx-controller
 |
 v
AI Assistant
 |
 v
Action Interpretation
 |
 v
kubernetes_restart_deployment
 |
 v
Target:
ingress-nginx/ingress-nginx-controller
 |
 v
Execute Action
 |
 v
KubernetesService
 |
 v
Kubernetes API
 |
 v
Deployment restarted
 |
 v
Action History
```
The operation was independently verified from the Kubernetes cluster.

The deployment status was:
```
READY:       1/1
UP-TO-DATE:  1
AVAILABLE:   1
```
The resulting pod was running successfully.

## 9. Independent Kubernetes Verification

Actions should be verifiable outside the application.

Check the deployment:
```
kubectl -n ingress-nginx get deployment \
  ingress-nginx-controller
```
Check the pod:
```
kubectl -n ingress-nginx get pods
```
Verify the rollout:
```
kubectl -n ingress-nginx rollout status \
  deployment/ingress-nginx-controller
```
A successful rollout returns:
```
deployment "ingress-nginx-controller" successfully rolled out
```
This provides an independent verification path for the action.

## 10. Action Result

After execution, the backend returns an action result to the frontend.

A successful Kubernetes restart produces a result similar to:
```
Kubernetes deployment restarted successfully
```
The frontend displays the result and updates the action state.

The action result is also persisted in the action history.

## 11. Action History

Executed actions are stored in PostgreSQL.

The history provides operational visibility into actions executed through the platform.

Recorded information includes:

- Action
- Target
- Namespace when applicable
- Execution status
- Execution timestamp
- Result/message

Example:
```
Action:
kubernetes_restart_deployment

Status:
completed

Target:
ingress-nginx/ingress-nginx-controller

Executed:
2026-08-25 14:32:25

Result:
Kubernetes deployment restarted successfully
```
The history can be viewed through the AI Assistant interface.

## 12. Action Persistence Flow
```
Action Execution
      |
      v
DevOps Action Service
      |
      +--------------------+
      |                    |
      v                    v
Infrastructure         PostgreSQL
Operation                  |
      |                    v
      |              Action History
      |
      v
Execution Result
      |
      v
Frontend
```
This allows the infrastructure result and the application record of the action to be connected.

## 13. Action Validation

The backend should only execute operations represented by the supported action catalog.

The general validation flow is:
```
AI Intent
   |
   v
Is this an action?
   |
   +---- No ----> Return normal AI response
   |
   +---- Yes
          |
          v
      Action supported?
          |
          +---- No ----> Do not execute
          |
          +---- Yes
                  |
                  v
             Validate target
                  |
                  v
               Execute
```
This keeps arbitrary model-generated instructions from becoming arbitrary infrastructure commands.

## 14. Failure Handling

If an action fails, the backend returns an error result instead of reporting a successful execution.

The frontend displays the execution failure to the user.

Operational failures should also be investigated using the underlying DevOps system.

For Kubernetes actions:
```
kubectl get pods -A
kubectl get deployments -A
kubectl describe deployment <deployment> -n <namespace>
```
For Docker actions:
```
docker ps
docker logs <container>
```
The platform therefore provides the action interface while the underlying DevOps tools remain available for independent diagnosis.

## 15. Health Before Action Execution

Before demonstrating DevOps actions, verify the application and its dependencies.

Application:
```
curl -s http://localhost:8000/api/v1/health \
  | python3 -m json.tool
```
Dependencies:
```
curl -s http://localhost:8000/api/v1/health/dependencies \
  | python3 -m json.tool
```
The dependency endpoint verifies:
```
database
redis
ollama
```
For Kubernetes actions, additionally verify:
```
kubectl get nodes
```
The cluster nodes should be Ready.

## 16. Docker Compose Relationship

The backend and frontend run through Docker Compose together with PostgreSQL and Redis:
```
Docker Compose
|
+-- frontend
|
+-- backend
|    |
|    +---- Docker socket
|    |
|    +---- Kubernetes kubeconfig
|    |
|    +---- Ollama on host
|
+-- postgres
|
+-- redis
```
The DevOps integrations are therefore external to the application container's own process space.

## 17. Security Boundary

The project is a portfolio and demonstration environment rather than a production enterprise control plane.

The Docker socket and Kubernetes kubeconfig provide the backend with significant operational access.

For that reason:

- The environment should be used only in a controlled development environment.
- The Docker socket should not be exposed to an untrusted application.
- The Kubernetes kubeconfig should remain protected.
- Local .env files must not be committed.
- The project should not be deployed as-is as a production privileged automation service.

The action confirmation workflow provides an application-level safety boundary, but it should not be treated as a complete production authorization system.

## 18. Why Actions Are Backend-Controlled

The platform intentionally avoids a design where the AI generates shell commands and the backend executes them directly.

Instead:
```
Unsafe pattern:

AI
 |
 v
Arbitrary shell command
 |
 v
Shell
```
The implemented approach is:
```
AI
 |
 v
Structured Action Intent
 |
 v
Supported Action
 |
 v
Dedicated Service
 |
 v
Docker / Kubernetes API
```
The second approach is easier to validate, test, explain, and demonstrate.

## 19. Current Action Scope

The current implementation focuses on a small set of meaningful operations rather than attempting to provide a complete DevOps automation engine.

The demonstrated capabilities include:

- Docker operations
- Kubernetes deployment restart
- Kubernetes inspection
- Action result reporting
- Action history

The project intentionally does not implement arbitrary infrastructure remediation.

## 20. Example End-to-End Demo

A complete Kubernetes action demonstration can be performed with:

#### Step 1 — Verify cluster
```
kubectl get nodes
```
#### Step 2 — Verify deployment
```
kubectl -n ingress-nginx get deployment \
  ingress-nginx-controller
```
#### Step 3 — Open the application
```
http://localhost:8080
```
#### Step 4 — Open AI Assistant
```
Navigate to the AI Assistant after authentication.
```
#### Step 5 — Request an action

Example:
```
Restart the ingress-nginx-controller deployment in the ingress-nginx namespace.
```
#### Step 6 — Interpret
```
Select the AI action interpretation workflow.
```
#### Step 7 — Review

Confirm that the action identifies:
```
Action:
kubernetes_restart_deployment

Target:
ingress-nginx-controller

Namespace:
ingress-nginx
```
#### Step 8 — Execute

Select:
```
Execute Action
```
#### Step 9 — Verify Kubernetes
```
kubectl -n ingress-nginx rollout status \
  deployment/ingress-nginx-controller
```
#### Step 10 — Review history
```
Return to the AI Assistant and review the recorded action.
```
## 21. DevOps Action Design Summary

The final execution model is:
```
                 +----------------+
                 |     User       |
                 +-------+--------+
                         |
                         v
                 +---------------+
                 | AI Interpreter|
                 +-------+-------+
                         |
                         v
                 +---------------+
                 | Action Intent |
                 +-------+-------+
                         |
                         v
                 +---------------+
                 | User Approval |
                 +-------+-------+
                         |
                         v
                 +---------------+
                 | Action Catalog|
                 +-------+-------+
                         |
              +----------+----------+
              |                     |
              v                     v
       +-------------+       +-------------+
       | Docker      |       | Kubernetes  |
       | Service     |       | Service     |
       +------+------+       +------+------+
              |                     |
              v                     v
        Docker Engine        Kubernetes API
              |                     |
              +----------+----------+
                         |
                         v
                 +---------------+
                 | Action Result |
                 +-------+-------+
                         |
                         v
                 +---------------+
                 | Action History|
                 +---------------+
```
This architecture demonstrates the central objective of the project:

**AI assists with DevOps intent and analysis, while deterministic services perform the actual infrastructure operations**.
