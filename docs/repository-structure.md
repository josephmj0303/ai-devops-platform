# Enterprise Repository Structure

This repository uses a clean enterprise layout that separates application code, platform automation, deployment configuration, infrastructure provisioning, delivery workflows, and documentation. The folders below define the intended ownership boundaries and expected contents for the AI-powered DevOps platform.

> This document is a structure and governance guide only. It does not introduce application source code.

## Folder Overview

| Folder | Purpose | Technologies | Expected Files |
| --- | --- | --- | --- |
| `backend/` | Owns server-side application capabilities, including REST APIs, authentication, authorization, agent orchestration, background workers, persistence integration, and observability instrumentation. | FastAPI, NestJS, or Go REST framework; PostgreSQL; Redis; JWT; OpenAPI; OpenTelemetry; Prometheus client libraries; Docker. | Backend service README, API design notes, OpenAPI specification, domain/module directories, database migration definitions, worker design notes, backend Dockerfile, backend tests, configuration examples, and operational health endpoint documentation. |
| `frontend/` | Owns the user-facing web experience for authentication, dashboards, agent task submission, review history, admin workflows, and operational visibility. | React or Next.js; TypeScript; Tailwind CSS or enterprise component system; REST client tooling; frontend test framework; Docker. | Frontend README, UI architecture notes, route/page structure, component structure, API client contracts, static assets, frontend Dockerfile, accessibility notes, test strategy, and environment configuration examples. |
| `infrastructure/` | Holds cross-cutting platform infrastructure design and shared operational assets that do not belong to one deployment mechanism. This folder is for platform-wide decisions, shared scripts, environment conventions, networking notes, observability foundations, and security guardrails. | Cloud provider services, Docker, platform scripts, observability tooling, secret-management patterns, IAM/RBAC conventions, policy-as-code tools, and environment configuration standards. | Platform infrastructure README, environment matrix, shared configuration templates, network and security design notes, observability design notes, policy documents, bootstrap runbooks, and shared automation documentation. |
| `kubernetes/` | Contains raw Kubernetes manifests and GitOps-ready environment overlays for running the platform services and dependencies. It is the source of truth when deploying directly with Kubernetes YAML or Kustomize-style overlays. | Kubernetes Deployments, Services, Ingress, ConfigMaps, Secrets references, ServiceAccounts, RBAC, NetworkPolicies, HPA, PDB, Kustomize, ArgoCD. | Namespace manifests, application Deployments, Services, Ingress resources, ConfigMaps, Secret templates or external secret references, RBAC resources, NetworkPolicies, HPA/PDB definitions, environment overlays, and ArgoCD application references. |
| `helm/` | Provides reusable Helm packaging for deploying the platform as versioned charts across development, staging, and production environments. | Helm charts, values files, Kubernetes templates, chart testing, semantic chart versioning, optional Helmfile. | `Chart.yaml`, chart README, `values.yaml`, environment-specific values files, Kubernetes templates, helper templates, chart tests, dependency definitions, and release notes for chart versions. |
| `terraform/` | Owns infrastructure-as-code for provisioning cloud and platform resources required by the application and delivery system. | Terraform, remote state backend, provider plugins, cloud IAM, Kubernetes provider, Helm provider, PostgreSQL/Redis managed services, DNS, TLS, container registry resources. | Root Terraform README, backend/state configuration guidance, provider definitions, reusable modules, environment compositions, variable files, outputs, IAM policies, cluster provisioning definitions, registry definitions, database/cache resources, and Terraform plan documentation. |
| `.github/` | Owns GitHub-native automation and repository governance, including CI/CD workflows, pull request quality gates, security scanning, issue templates, and dependency automation. | GitHub Actions, Dependabot, CodeQL, secret scanning, container scanning, reusable workflows, branch protection documentation. | Workflow YAML files, reusable workflow definitions, pull request templates, issue templates, Dependabot configuration, CodeQL configuration, security policy references, release workflow notes, and repository automation documentation. |
| `docs/` | Centralizes product, architecture, onboarding, operations, security, and portfolio documentation. This is the primary place for human-readable guidance and design decisions. | Markdown, Mermaid diagrams, architecture decision records, runbooks, API documentation, threat models, operational playbooks. | Product requirements, architecture design, repository structure guide, ADRs, onboarding guides, API documentation, runbooks, deployment guides, troubleshooting guides, security model, observability guide, and demo scripts. |

## Recommended Root Layout

```text
.
├── backend/
├── frontend/
├── infrastructure/
├── kubernetes/
├── helm/
├── terraform/
├── .github/
├── docs/
├── README.md
└── LICENSE
```

## Ownership Principles

- Keep runtime application code in `backend/` and `frontend/` only.
- Keep cloud provisioning in `terraform/` and runtime deployment configuration in `kubernetes/` or `helm/`.
- Use `infrastructure/` for shared platform context, guardrails, diagrams, and automation that spans multiple delivery tools.
- Use `.github/` for repository automation only; avoid placing application or deployment logic there unless it is part of CI/CD orchestration.
- Use `docs/` for long-form explanations, runbooks, architecture decisions, and onboarding material.
- Avoid duplicating the same deployment configuration in both `kubernetes/` and `helm/`; if both are present, clearly document which one is canonical for each environment.
