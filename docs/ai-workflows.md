# AI Workflows

This document describes how AI is integrated into the AI DevOps Platform.

The project uses AI as a DevOps assistance and decision-support layer. The AI can analyze DevOps-related input, interpret operational requests, and identify supported actions.

Actual DevOps operations are performed by dedicated backend services, not directly by the language model.

---

## 1. AI Architecture

The AI workflow is organized around a provider abstraction.

```
                        Frontend
                           |
                           v
                     FastAPI API
                           |
                           v
                      AI Service
                           |
                           v
                    Provider Factory
                           |
                +----------+----------+
                |                     |
                v                     v
             Ollama                OpenAI
                |
                v
          llama3.2:3b
```
The current runtime provider is Ollama.

The project also contains an OpenAI provider implementation so that the AI layer is not tightly coupled to a single provider.

## 2. Current AI Provider

The active provider is:
```
Provider: Ollama
Model:    llama3.2:3b
```
Ollama runs on the development host.

The backend reaches the host Ollama API through:
```
http://host.docker.internal:11434
```
Running Ollama outside the application containers avoids introducing another memory-intensive container.

## 3. Provider Abstraction

AI provider implementations are located under:
```
backend/src/app/providers/
```
The main components are:
```
base.py
factory.py
ollama.py
openai.py
```
The provider abstraction allows the application service to work with an AI provider without depending directly on a specific implementation.

Conceptually:
```
AI Service
    |
    v
Provider Interface
    |
    +---- Ollama Provider
    |
    +---- OpenAI Provider
```
The current environment selects Ollama.

## 4. AI Service

The main AI application logic is implemented under:
```
backend/src/app/services/
```
The AI service is responsible for:

- Receiving AI requests.
- Selecting the appropriate prompt/workflow.
- Calling the configured AI provider.
- Returning the generated result.
- Supporting structured action interpretation.

The frontend communicates with the backend rather than communicating directly with Ollama.

This keeps provider-specific behavior inside the backend.

## 5. AI Chat

The AI Assistant provides a general DevOps-oriented chat workflow.
```
User
 |
 | Natural-language question
 v
React AI Assistant
 |
 | API request
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
AI response
 |
 v
React UI
```
This workflow is intended for general DevOps assistance and explanation.

The model does not directly execute commands as part of ordinary chat.

## 6. Dockerfile Analysis

The platform can analyze Dockerfile content.

The workflow is:
```
Dockerfile
    |
    v
Frontend AI Analysis
    |
    v
FastAPI
    |
    v
Dockerfile Prompt
    |
    v
Ollama
    |
    v
Analysis Result
```
The AI analyzes the supplied Dockerfile and returns findings and recommendations.

Typical areas of analysis can include:

- Dockerfile structure
- Image selection
- Build practices
- Layering
- Container configuration
- Potential improvements

The AI provides recommendations; it does not automatically modify the Dockerfile.

## 7. Kubernetes Analysis

The platform provides an AI workflow for Kubernetes-related input.

The workflow is:
```
Kubernetes Configuration
          |
          v
      AI Assistant
          |
          v
       FastAPI
          |
          v
 Kubernetes Prompt
          |
          v
        Ollama
          |
          v
 Analysis / Findings
```
The Kubernetes analysis workflow is separate from the Kubernetes action execution workflow.

This distinction is important:
```
Kubernetes Analysis
        |
        +--> AI provides findings/recommendations

Kubernetes Action
        |
        +--> Backend Kubernetes service performs an operation
```
The AI therefore acts as an analysis and interpretation layer rather than replacing the Kubernetes client.

## 8. Terraform Analysis

Terraform configuration can also be submitted for AI analysis.

The workflow follows the same pattern:
```
Terraform Configuration
          |
          v
       FastAPI
          |
          v
 Terraform Prompt
          |
          v
        Ollama
          |
          v
 Findings / Recommendations
```
The current project uses Terraform as an AI analysis capability.

It does not use Terraform to provision the AI DevOps Platform itself.

No Terraform execution is triggered by the AI analysis workflow.

## 9. Log Analysis

The platform can analyze log content to assist with troubleshooting.
```
Application / DevOps Logs
          |
          v
       AI Assistant
          |
          v
       FastAPI
          |
          v
      Logs Prompt
          |
          v
        Ollama
          |
          v
 Findings / Recommendations
```
The AI can help identify:

- Potential failures
- Error patterns
- Operational symptoms
- Possible causes
- Recommended investigation steps

The workflow is intended as an operational troubleshooting assistant.

## 10. AI Action Interpretation

One of the key capabilities of the platform is interpreting a natural-language DevOps request.

For example:
```
Restart the ingress-nginx-controller deployment
in the ingress-nginx namespace.
```
The request is first sent to the backend for interpretation.
```
Natural-language request
          |
          v
       FastAPI
          |
          v
      AI Service
          |
          v
      Action Prompt
          |
          v
        Ollama
          |
          v
    Structured Intent
```
The resulting intent identifies whether the request represents a supported DevOps action.

A successful interpretation can identify information such as:
```
is_action
action
target
namespace
reason
```
## 11. AI Interpretation Does Not Equal Execution

The platform deliberately separates AI interpretation from action execution.

The complete workflow is:
```
             User Request
                  |
                  v
          Interpret with AI
                  |
                  v
           Action Intent
                  |
             +----+----+
             |         |
             v         v
        Not an Action  Supported Action
             |               |
             v               v
       Show Response     Show Preview
                             |
                             v
                      User selects
                      Execute Action
                             |
                             v
                      Backend Service
                             |
                             v
                    Docker / Kubernetes
```
This is an important architectural boundary.

The language model determines the intended action, but the backend controls the actual operation.

## 12. Supported DevOps Actions

The platform maintains a catalog of supported DevOps actions.

Current integrations include actions for:
```
Docker
Kubernetes
```
Examples include:
```
docker_restart
kubernetes_restart_deployment
```
The action catalog prevents arbitrary natural-language instructions from being treated as executable operations.

The backend receives the interpreted action and validates it against the supported action implementation before execution.

## 13. Kubernetes Action Example

A concrete demonstrated workflow is restarting a Kubernetes deployment.

Example request:
```
Restart the ingress-nginx-controller deployment in the ingress-nginx namespace.
```
The workflow is:
```
User
 |
 v
AI Assistant
 |
 v
Interpret Action
 |
 v
kubernetes_restart_deployment
 |
 v
Target:
ingress-nginx/ingress-nginx-controller
 |
 v
User clicks Execute Action
 |
 v
KubernetesService
 |
 v
Kubernetes API
 |
 v
Deployment restarted
```
The Kubernetes deployment can then be verified independently:
```
kubectl -n ingress-nginx rollout status \
  deployment/ingress-nginx-controller
```
This separation makes the demonstration easy to verify from both the application and Kubernetes sides.

## 14. Action Result

After an action executes, the backend returns an execution result to the frontend.

For a successful Kubernetes deployment restart, the result can indicate:
```
Kubernetes deployment restarted successfully
```
The frontend then updates the action state and displays the result to the user.

## 15. Action History

Executed actions are persisted by the backend.

The action history provides a record containing information such as:

- Action
- Target
- Namespace when applicable
- Execution status
- Execution time
- Result/message

Example:
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
This provides traceability for actions executed through the platform.

## 16. AI Analysis History

AI analysis results are also persisted.

This allows users to review previous analysis requests rather than losing results when the page is refreshed.

The frontend exposes analysis history through the AI Assistant interface.

The backend stores the analysis records in PostgreSQL.

Conceptually:
```
AI Request
    |
    v
AI Provider
    |
    v
AI Result
    |
    +------> Frontend
    |
    +------> PostgreSQL
                 |
                 v
          Analysis History
```
## 17. Prompt Organization

The project keeps AI prompts separate from application services.

Prompts are located under:
```
backend/src/app/prompts/
```
Current prompt categories include:
```
actions.py
chat.py
dockerfile.py
kubernetes.py
logs.py
terraform.py
```
This keeps the prompt definitions easier to inspect and modify without embedding large prompt strings throughout the service implementation.

## 18. Structured AI Responses

The AI service supports structured response handling for workflows that require more than plain text.

This is particularly important for action interpretation.

Instead of treating an AI response as an executable command, the application expects structured action information that can be validated and passed to the appropriate backend service.

Conceptually:
```
AI Output
   |
   v
Structured Intent
   |
   v
Validation
   |
   v
Supported Action
   |
   v
Execution
```
This is safer and easier to reason about than directly executing free-form model output.

## 19. AI and DevOps Service Boundaries

The project intentionally keeps AI and DevOps execution as separate
concerns.
```
+----------------------+
| AI Layer             |
|                      |
| Prompt + Provider    |
| Interpretation       |
| Analysis             |
+----------+-----------+
           |
           | intent / findings
           v
+----------------------+
| Application Layer    |
|                      |
| Validation           |
| Action Catalog       |
| Action History       |
+----------+-----------+
           |
           v
+----------------------+
| DevOps Services      |
|                      |
| Docker               |
| Kubernetes           |
+----------------------+
```
This makes the AI useful without making the AI model responsible for direct infrastructure access.

## 20. Local AI Design

The project uses a local AI model rather than requiring a remote AI API for the main demonstration.

Advantages for this project include:

- No external AI service is required for the default workflow.
- The AI model can run locally.
- The project can be demonstrated without sending DevOps input to an external provider.
- The architecture still supports an alternative provider through the provider abstraction.

The trade-off is that a small local model has more limited reasoning capability than larger hosted models.

The project deliberately accepts that trade-off to keep the development environment lightweight.

## 21. AI Scope

The AI layer is intentionally focused on practical DevOps assistance.

It demonstrates:

- Natural-language DevOps interaction
- Infrastructure/configuration analysis
- Log analysis
- Action interpretation
- AI-assisted operational workflows

It does not attempt to provide:

- Autonomous infrastructure management
- Fully autonomous remediation
- Production-scale agent orchestration
- Large-model hosting infrastructure
- Long-running AI agents
- Enterprise AI governance

The objective is to demonstrate meaningful AI Engineering integrated with real DevOps tooling.

## 22. Complete AI DevOps Workflow

The overall platform workflow can be summarized as:
```
                         User
                          |
                          v
                  React AI Assistant
                          |
              +-----------+-----------+
              |                       |
              v                       v
        AI Analysis             Action Request
              |                       |
              v                       v
         FastAPI AI Service     Action Interpretation
              |                       |
              v                       v
           Ollama               Structured Intent
              |                       |
              v                       v
         AI Findings          User Confirmation
                                      |
                                      v
                               DevOps Service
                                  /       \
                                 /         \
                                v           v
                             Docker    Kubernetes
                                \         /
                                 \       /
                                  v     v
                                  Result
                                    |
                    +---------------+---------------+
                    |                               |
                    v                               v
             Frontend Result                 PostgreSQL
                                                   |
                                                   v
                                           History / Audit
```
This is the central AI Engineering story of the project:

AI assists with understanding DevOps problems and operational intent, while deterministic backend services remain responsible for executing actual DevOps operations.
