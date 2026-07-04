# REST API Design

This document defines the REST API surface for the AI-Powered DevOps Platform. The APIs are versioned under `/api/v1`, use JSON request and response bodies unless otherwise stated, and return standard HTTP status codes.

## API Conventions

- **Base path:** `/api/v1`
- **Authentication:** JWT bearer tokens sent with `Authorization: Bearer <access_token>`.
- **Pagination:** List endpoints accept `page`, `page_size`, `sort`, and `filter` query parameters where applicable.
- **Timestamps:** All timestamps are ISO 8601 UTC strings.
- **Errors:** Error responses use a consistent envelope: `{ "error": { "code": "string", "message": "string", "details": {} } }`.
- **Roles:** Admin endpoints require an administrator role. User, agent, chat, and history endpoints require the authenticated user to have access to the requested resource.

## Authentication APIs

| Method | Endpoint | Request | Response | Authentication Required | Description |
| --- | --- | --- | --- | --- | --- |
| POST | `/api/v1/auth/register` | `{ "email": "user@example.com", "password": "string", "name": "User Name" }` | `201 Created` with `{ "user": { "id": "uuid", "email": "user@example.com", "name": "User Name", "role": "engineer" }, "access_token": "jwt", "refresh_token": "jwt" }` | No | Creates a new user account and returns initial tokens. |
| POST | `/api/v1/auth/login` | `{ "email": "user@example.com", "password": "string" }` | `200 OK` with `{ "access_token": "jwt", "refresh_token": "jwt", "expires_in": 900, "user": { "id": "uuid", "email": "user@example.com", "role": "engineer" } }` | No | Authenticates a user and issues access and refresh tokens. |
| POST | `/api/v1/auth/refresh` | `{ "refresh_token": "jwt" }` | `200 OK` with `{ "access_token": "jwt", "refresh_token": "jwt", "expires_in": 900 }` | No | Rotates a refresh token and issues a new access token. |
| POST | `/api/v1/auth/logout` | `{ "refresh_token": "jwt" }` | `204 No Content` | Yes | Revokes the current refresh token and ends the authenticated session. |
| POST | `/api/v1/auth/password/reset-request` | `{ "email": "user@example.com" }` | `202 Accepted` with `{ "message": "If the account exists, a reset email has been sent." }` | No | Starts the password reset flow without revealing whether the account exists. |
| POST | `/api/v1/auth/password/reset` | `{ "token": "reset-token", "new_password": "string" }` | `204 No Content` | No | Completes a password reset using a time-limited reset token. |
| GET | `/api/v1/auth/me` | None | `200 OK` with `{ "id": "uuid", "email": "user@example.com", "name": "User Name", "role": "engineer", "created_at": "timestamp" }` | Yes | Returns the current authenticated user. |

## User APIs

| Method | Endpoint | Request | Response | Authentication Required | Description |
| --- | --- | --- | --- | --- | --- |
| GET | `/api/v1/users/me` | None | `200 OK` with `{ "id": "uuid", "email": "user@example.com", "name": "User Name", "role": "engineer", "preferences": {}, "created_at": "timestamp" }` | Yes | Retrieves the authenticated user's profile. |
| PATCH | `/api/v1/users/me` | `{ "name": "Updated Name", "preferences": { "default_agent": "kubernetes-troubleshooter" } }` | `200 OK` with updated user profile | Yes | Updates profile fields and user preferences. |
| GET | `/api/v1/users/me/sessions` | Query parameters: `page`, `page_size`, `agent_id`, `status` | `200 OK` with `{ "items": [ { "id": "uuid", "agent_id": "string", "status": "completed", "created_at": "timestamp" } ], "page": 1, "page_size": 20, "total": 100 }` | Yes | Lists the authenticated user's chat and agent sessions. |
| GET | `/api/v1/users/me/api-keys` | None | `200 OK` with `{ "items": [ { "id": "uuid", "name": "ci-key", "last_used_at": "timestamp", "created_at": "timestamp" } ] }` | Yes | Lists personal API keys without exposing secret values. |
| POST | `/api/v1/users/me/api-keys` | `{ "name": "ci-key", "expires_at": "timestamp" }` | `201 Created` with `{ "id": "uuid", "name": "ci-key", "token": "secret-once", "expires_at": "timestamp" }` | Yes | Creates a personal API key and returns the secret once. |
| DELETE | `/api/v1/users/me/api-keys/{api_key_id}` | None | `204 No Content` | Yes | Revokes one personal API key. |

## Agent APIs

| Method | Endpoint | Request | Response | Authentication Required | Description |
| --- | --- | --- | --- | --- | --- |
| GET | `/api/v1/agents` | Query parameters: `category`, `enabled`, `page`, `page_size` | `200 OK` with `{ "items": [ { "id": "kubernetes-troubleshooter", "name": "Kubernetes Troubleshooter", "category": "kubernetes", "enabled": true, "description": "string" } ], "page": 1, "page_size": 20, "total": 6 }` | Yes | Lists agents available to the user. |
| GET | `/api/v1/agents/{agent_id}` | None | `200 OK` with `{ "id": "string", "name": "string", "category": "string", "capabilities": ["logs", "manifests"], "input_schema": {}, "output_schema": {}, "enabled": true }` | Yes | Returns details, capabilities, and schemas for an agent. |
| POST | `/api/v1/agents/{agent_id}/runs` | `{ "input": { "prompt": "string", "artifacts": [ { "type": "kubernetes_manifest", "content": "string" } ] }, "metadata": { "source": "web" } }` | `202 Accepted` with `{ "run_id": "uuid", "session_id": "uuid", "status": "queued", "status_url": "/api/v1/agents/runs/{run_id}" }` | Yes | Starts an asynchronous agent run. |
| GET | `/api/v1/agents/runs/{run_id}` | None | `200 OK` with `{ "id": "uuid", "agent_id": "string", "status": "running", "progress": 60, "result": null, "created_at": "timestamp", "updated_at": "timestamp" }` | Yes | Retrieves agent run status and result when available. |
| POST | `/api/v1/agents/runs/{run_id}/cancel` | None | `202 Accepted` with `{ "id": "uuid", "status": "cancel_requested" }` | Yes | Requests cancellation for a queued or running agent run. |
| POST | `/api/v1/agents/runs/{run_id}/feedback` | `{ "rating": 5, "helpful": true, "comment": "string" }` | `201 Created` with `{ "id": "uuid", "run_id": "uuid", "created_at": "timestamp" }` | Yes | Records user feedback for an agent response. |

## Chat APIs

| Method | Endpoint | Request | Response | Authentication Required | Description |
| --- | --- | --- | --- | --- | --- |
| POST | `/api/v1/chat/sessions` | `{ "agent_id": "kubernetes-troubleshooter", "title": "CrashLoopBackOff investigation", "context": { "environment": "prod" } }` | `201 Created` with `{ "id": "uuid", "agent_id": "string", "title": "string", "status": "active", "created_at": "timestamp" }` | Yes | Creates a chat session for an agent-assisted workflow. |
| GET | `/api/v1/chat/sessions` | Query parameters: `page`, `page_size`, `agent_id`, `status` | `200 OK` with `{ "items": [ { "id": "uuid", "title": "string", "agent_id": "string", "status": "active", "updated_at": "timestamp" } ], "page": 1, "page_size": 20, "total": 42 }` | Yes | Lists chat sessions visible to the authenticated user. |
| GET | `/api/v1/chat/sessions/{session_id}` | None | `200 OK` with `{ "id": "uuid", "agent_id": "string", "title": "string", "status": "active", "context": {}, "created_at": "timestamp", "updated_at": "timestamp" }` | Yes | Retrieves chat session metadata. |
| POST | `/api/v1/chat/sessions/{session_id}/messages` | `{ "role": "user", "content": "string", "attachments": [ { "artifact_id": "uuid" } ] }` | `202 Accepted` with `{ "message_id": "uuid", "run_id": "uuid", "status": "queued" }` | Yes | Adds a user message and queues the agent response. |
| GET | `/api/v1/chat/sessions/{session_id}/messages` | Query parameters: `page`, `page_size`, `before` | `200 OK` with `{ "items": [ { "id": "uuid", "role": "user", "content": "string", "created_at": "timestamp" } ], "page": 1, "page_size": 50, "total": 120 }` | Yes | Lists messages in a chat session. |
| PATCH | `/api/v1/chat/sessions/{session_id}` | `{ "title": "New title", "status": "archived" }` | `200 OK` with updated session metadata | Yes | Updates chat session metadata or archives the session. |
| DELETE | `/api/v1/chat/sessions/{session_id}` | None | `204 No Content` | Yes | Deletes or tombstones a chat session according to retention policy. |

## History APIs

| Method | Endpoint | Request | Response | Authentication Required | Description |
| --- | --- | --- | --- | --- | --- |
| GET | `/api/v1/history` | Query parameters: `page`, `page_size`, `type`, `agent_id`, `from`, `to` | `200 OK` with `{ "items": [ { "id": "uuid", "type": "agent_run", "summary": "string", "agent_id": "string", "created_at": "timestamp" } ], "page": 1, "page_size": 20, "total": 200 }` | Yes | Searches the user's historical chats, runs, reviews, and feedback records. |
| GET | `/api/v1/history/{history_id}` | None | `200 OK` with `{ "id": "uuid", "type": "chat_session", "summary": "string", "metadata": {}, "created_at": "timestamp" }` | Yes | Retrieves one historical record. |
| GET | `/api/v1/history/export` | Query parameters: `format`, `from`, `to`, `agent_id` | `202 Accepted` with `{ "export_id": "uuid", "status": "queued", "download_url": null }` | Yes | Starts an export of historical records in JSON or CSV format. |
| GET | `/api/v1/history/exports/{export_id}` | None | `200 OK` with `{ "id": "uuid", "status": "completed", "download_url": "https://example.com/download", "expires_at": "timestamp" }` | Yes | Checks export status and returns the download URL when ready. |
| DELETE | `/api/v1/history/{history_id}` | None | `204 No Content` | Yes | Deletes a user-owned historical record when retention rules allow. |

## Health APIs

| Method | Endpoint | Request | Response | Authentication Required | Description |
| --- | --- | --- | --- | --- | --- |
| GET | `/health/live` | None | `200 OK` with `{ "status": "ok" }` | No | Liveness probe that verifies the API process is running. |
| GET | `/health/ready` | None | `200 OK` with `{ "status": "ready", "checks": { "database": "ok", "redis": "ok", "queue": "ok" } }` | No | Readiness probe that verifies required dependencies are reachable. |
| GET | `/api/v1/health` | None | `200 OK` with `{ "status": "ok", "version": "string", "uptime_seconds": 12345 }` | No | Public health summary for load balancers and basic monitoring. |
| GET | `/api/v1/health/dependencies` | None | `200 OK` with `{ "database": { "status": "ok", "latency_ms": 12 }, "redis": { "status": "ok", "latency_ms": 4 }, "ai_provider": { "status": "degraded" } }` | Yes | Detailed dependency health for operators and support users. |

## Metrics APIs

| Method | Endpoint | Request | Response | Authentication Required | Description |
| --- | --- | --- | --- | --- | --- |
| GET | `/metrics` | None | `200 OK` with Prometheus text exposition format | No, when network-restricted to Prometheus; otherwise service token required | Exposes Prometheus metrics for scraping. |
| GET | `/api/v1/metrics/summary` | Query parameters: `from`, `to` | `200 OK` with `{ "request_count": 10000, "error_rate": 0.01, "p95_latency_ms": 180, "agent_runs": 250 }` | Yes | Returns a human-readable metrics summary for dashboards. |
| GET | `/api/v1/metrics/agents` | Query parameters: `from`, `to`, `agent_id` | `200 OK` with `{ "items": [ { "agent_id": "kubernetes-troubleshooter", "runs": 120, "success_rate": 0.98, "p95_duration_ms": 4500 } ] }` | Yes | Returns per-agent usage, success, latency, and feedback metrics. |
| GET | `/api/v1/metrics/users` | Query parameters: `from`, `to` | `200 OK` with `{ "active_users": 42, "new_users": 8, "sessions": 300 }` | Admin | Returns aggregate user activity metrics for administrators. |

## Admin APIs

| Method | Endpoint | Request | Response | Authentication Required | Description |
| --- | --- | --- | --- | --- | --- |
| GET | `/api/v1/admin/users` | Query parameters: `page`, `page_size`, `role`, `status`, `query` | `200 OK` with `{ "items": [ { "id": "uuid", "email": "user@example.com", "role": "engineer", "status": "active" } ], "page": 1, "page_size": 20, "total": 100 }` | Admin | Lists all users for administrative management. |
| POST | `/api/v1/admin/users` | `{ "email": "user@example.com", "name": "User Name", "role": "engineer", "status": "active" }` | `201 Created` with created user profile | Admin | Creates a user account, optionally triggering an invitation email. |
| PATCH | `/api/v1/admin/users/{user_id}` | `{ "role": "admin", "status": "suspended", "name": "Updated Name" }` | `200 OK` with updated user profile | Admin | Updates user role, status, and administrative profile fields. |
| DELETE | `/api/v1/admin/users/{user_id}` | None | `204 No Content` | Admin | Deactivates or deletes a user according to retention policy. |
| GET | `/api/v1/admin/agents` | Query parameters: `page`, `page_size`, `enabled`, `category` | `200 OK` with `{ "items": [ { "id": "string", "name": "string", "enabled": true, "category": "string" } ], "page": 1, "page_size": 20, "total": 6 }` | Admin | Lists all configured agents, including disabled agents. |
| PATCH | `/api/v1/admin/agents/{agent_id}` | `{ "enabled": false, "rate_limit_per_hour": 100, "allowed_roles": ["admin", "engineer"] }` | `200 OK` with updated agent configuration | Admin | Updates agent availability, rate limits, and role access policy. |
| GET | `/api/v1/admin/audit-events` | Query parameters: `page`, `page_size`, `actor_id`, `action`, `from`, `to` | `200 OK` with `{ "items": [ { "id": "uuid", "actor_id": "uuid", "action": "user.updated", "target_id": "uuid", "created_at": "timestamp" } ], "page": 1, "page_size": 20, "total": 500 }` | Admin | Searches administrative and security audit events. |
| GET | `/api/v1/admin/system/status` | None | `200 OK` with `{ "version": "string", "environment": "production", "workers": { "active": 4, "queue_depth": 12 }, "dependencies": {} }` | Admin | Returns system status, worker state, queue depth, and dependency summary. |
