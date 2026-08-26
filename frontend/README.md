# Frontend

React + TypeScript frontend for the AI DevOps Platform.

The frontend provides the web interface for authentication, project management, AI-powered DevOps analysis, DevOps action execution, and analysis history.

## Technology Stack

- React
- TypeScript
- Vite
- React Router
- Axios
- Tailwind CSS
- React Hook Form
- Zod
- Nginx
- Docker

## Application Structure

```
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── ai.ts
│   │   ├── auth.ts
│   │   ├── axios.ts
│   │   └── projects.ts
│   ├── assets/
│   ├── components/
│   │   └── ProtectedRoute.tsx
│   ├── context/
│   │   └── AuthContext.tsx
│   ├── layouts/
│   │   └── DashboardLayout.tsx
│   ├── pages/
│   │   ├── AIAssistant.tsx
│   │   ├── Dashboard.tsx
│   │   ├── Login.tsx
│   │   └── Projects.tsx
│   ├── types/
│   │   ├── ai.ts
│   │   ├── auth.ts
│   │   └── project.ts
│   ├── App.tsx
│   ├── App.css
│   ├── index.css
│   └── main.tsx
├── Dockerfile
├── package.json
├── package-lock.json
├── vite.config.ts
└── tsconfig*.json
```

## Application Routes

| Route | Access | Purpose |
|-------|--------|---------|
| / | Public | Login |
| /dashboard | Protected | Platform dashboard |
| /projects | Protected | Project management |
| /ai |	Protected | AI DevOps Assistant |

Protected routes are wrapped by **ProtectedRoute** and use the shared **DashboardLayout**.

## Authentication

Authentication is handled through the backend API.

The frontend stores the authentication token in browser local storage and the Axios client automatically adds the token as a Bearer token to API requests.

The main authentication components are:

- AuthContext.tsx - authentication state
- ProtectedRoute.tsx - protected route handling
- api/auth.ts - authentication API calls
- api/axios.ts - shared API client

## Backend API Integration

The frontend uses Axios for communication with the FastAPI backend.

The current local API endpoint is:
```
http://192.168.56.20:8000/api/v1
```
The shared Axios client:

1. Configures the backend API base URL.
2. Sets the JSON content type.
3. Reads the authentication token from local storage.
4. Adds the token as a Bearer authorization header.

API functionality is organized into:
```
src/api/
├── ai.ts
├── auth.ts
├── axios.ts
└── projects.ts
```
## Dashboard

The dashboard provides the main authenticated entry point into the platform and links users to the platform's DevOps functionality.

### Projects

The Projects page provides the frontend interface for working with projects through the backend project APIs.

### AI DevOps Assistant

The AI Assistant is the main AI interface of the platform.

It supports four analysis types:

- Application Logs
- Dockerfile
- Kubernetes Manifest
- Terraform

Users provide the relevant content and select the analysis type. The frontend sends the request to the backend AI API and displays the returned analysis.

#### AI Analysis Flow
```
User selects analysis type
        │
        ▼
User provides DevOps input
        │
        ▼
"Analyze with AI"
        │
        ▼
Frontend API client
        │
        ▼
FastAPI backend
        │
        ▼
AI provider
        │
        ▼
Analysis response
        │
        ▼
Frontend result card
```
### AI DevOps Actions

The AI Assistant also supports natural-language DevOps actions.

A user can describe an action such as:
```
Restart the ingress-nginx-controller deployment in the ingress-nginx namespace
```
The frontend sends the request for AI interpretation first.

The interpreted action is then displayed as a preview containing the identified action, target, namespace when applicable, and reasoning.

Only after the action has been interpreted can the user select **Execute Action**.

#### Action Flow
```
Natural-language request
        │
        ▼
Interpret with AI
        │
        ▼
AI action preview
        │
        ├── No executable action
        │       └── Display result
        │
        └── Executable action
                │
                ▼
          Execute Action
                │
                ▼
        Backend DevOps service
                │
                ▼
          Action result
```
This provides a clear separation between AI interpretation and actual DevOps action execution.

## Analysis History

The AI Assistant loads previously stored AI analysis results from the backend.

The history interface allows users to:

- View the number of previous analyses.
- Select an analysis from the history.
- Review previously generated analysis results.

Analysis history is persisted by the backend rather than only being maintained in frontend state.

## Docker

The frontend uses a multistage Docker build.

**Build stage**

The first stage uses Node.js to:

1. Install dependencies.
2. Copy the frontend source.
3. Run the production build.

**Runtime stage**

The generated Vite dist directory is served using Nginx.

The resulting container exposes:
```
80/tcp
```
The Dockerfile therefore keeps the runtime image smaller than a Node.js-based development container.

## Local Development

Install dependencies:
```
cd frontend
npm ci
```
Start the Vite development server:
```
npm run dev
```
Build the frontend:
```
npm run build
```
Run linting:
```
npm run lint
```
Preview the production build:
```
npm run preview
```

## Docker Compose

The frontend can be started as part of the main project Compose environment.

From the project root:
```
docker compose up -d --build
```
Check the services:
```
docker compose ps
```
The frontend is exposed on:
```
http://localhost:8080
```
The backend is exposed on:
```
http://localhost:8000
```
The frontend container serves the compiled application through Nginx.

## Development Notes

The current frontend is intentionally designed for the project's demonstration environment.

It focuses on demonstrating:

- React-based DevOps UI
- Backend API integration
- JWT authentication
- AI-assisted DevOps analysis
- AI-assisted DevOps action interpretation
- Controlled DevOps action execution
- Persistent analysis and action history

It does not attempt to implement a production-scale enterprise frontend architecture.

For the overall platform architecture and service relationships, see:
```
docs/architecture.md
```
