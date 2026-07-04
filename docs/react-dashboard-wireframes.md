# Modern React Dashboard Wireframes

This document defines low-fidelity Mermaid wireframes for a modern React dashboard experience for the AI-Powered DevOps Platform. These wireframes are intentionally implementation-agnostic and do not include React code.

## Design System Direction

- **Visual style:** modern SaaS interface with dark-first theming, soft cards, subtle borders, rounded panels, and clear operational status indicators.
- **Layout model:** authenticated pages use a persistent left sidebar, top command bar, responsive content grid, and context-aware right panels where useful.
- **Navigation:** primary routes include Dashboard, Chat, Agent List, History, Metrics, Settings, and Admin.
- **Interaction priorities:** fast agent selection, visible platform health, searchable history, clear permissions, and explainable AI session outputs.
- **Responsive behavior:** desktop uses multi-column layouts; tablet collapses secondary panels; mobile collapses navigation into a drawer and stacks cards vertically.

## Route Map

```mermaid
flowchart LR
    Login[Login]
    Shell[Authenticated App Shell]
    Dashboard[Dashboard]
    Chat[Chat]
    Agents[Agent List]
    History[History]
    Metrics[Metrics]
    Settings[Settings]
    Admin[Admin]

    Login -->|Successful authentication| Shell
    Shell --> Dashboard
    Shell --> Chat
    Shell --> Agents
    Shell --> History
    Shell --> Metrics
    Shell --> Settings
    Shell --> Admin
```

## Shared Authenticated App Shell

```mermaid
flowchart TB
    subgraph Shell[Authenticated Dashboard Shell]
        Top[Top Bar: search, environment switcher, notifications, user menu]
        subgraph Body[Main Application Frame]
            Side[Sidebar Navigation: Dashboard, Chat, Agents, History, Metrics, Settings, Admin]
            Main[Page Content Area]
            Context[Optional Context Panel: details, filters, recommendations]
        end
        Footer[Compact Footer: version, status, documentation]
    end

    Top --> Body
    Body --> Footer
    Side --- Main
    Main --- Context
```

## Login Page

```mermaid
flowchart TB
    subgraph LoginPage[Login Page]
        Brand[Brand Panel: AI DevOps Platform, value proposition, trust signals]
        Card[Login Card]
        Email[Email Input]
        Password[Password Input]
        Options[Remember device, forgot password]
        Submit[Primary Button: Sign in]
        SSO[Secondary Actions: GitHub SSO, Google SSO]
        Security[Security Note: JWT sessions, RBAC, audit logging]
    end

    Brand --- Card
    Card --> Email
    Card --> Password
    Card --> Options
    Card --> Submit
    Card --> SSO
    Card --> Security
```

## Dashboard Page

```mermaid
flowchart TB
    subgraph DashboardPage[Dashboard Page]
        Header[Page Header: welcome message, quick action button]
        subgraph KPIs[KPI Cards]
            Active[Active Sessions]
            Success[Resolution Rate]
            Latency[Agent Latency]
            Alerts[Open Alerts]
        end
        subgraph MainGrid[Primary Content Grid]
            AgentLauncher[Agent Launcher: Kubernetes, Docker, Terraform, GitHub Actions, Linux]
            Recent[Recent Sessions: status, owner, agent, last activity]
            Health[Platform Health: API, workers, PostgreSQL, Redis, AI provider]
            Recommendations[Recommended Next Actions]
        end
    end

    Header --> KPIs
    KPIs --> MainGrid
    AgentLauncher --- Recent
    Health --- Recommendations
```

## Chat Page

```mermaid
flowchart TB
    subgraph ChatPage[Chat Page]
        ChatHeader[Chat Header: selected agent, session title, status]
        subgraph ChatLayout[Three Column Chat Layout]
            Sessions[Session Rail: recent chats, saved investigations]
            Conversation[Conversation Panel: user prompts, agent responses, streaming status]
            Inspector[Inspector Panel: artifacts, severity, evidence, suggested commands]
        end
        Composer[Composer: message input, artifact upload, agent selector, send button]
    end

    ChatHeader --> ChatLayout
    Sessions --- Conversation
    Conversation --- Inspector
    Conversation --> Composer
```

## Agent List Page

```mermaid
flowchart TB
    subgraph AgentListPage[Agent List Page]
        Header[Page Header: agent catalog, create policy action]
        Filters[Filters: category, status, access level, owner]
        subgraph Catalog[Agent Catalog]
            K8s[Kubernetes Troubleshooter Card]
            Docker[Docker Optimizer Card]
            Terraform[Terraform Reviewer Card]
            Actions[GitHub Actions Reviewer Card]
            Linux[Linux Troubleshooter Card]
        end
        Detail[Agent Detail Drawer: prompt policy, tools, confidence, recent usage]
    end

    Header --> Filters
    Filters --> Catalog
    Catalog --> Detail
```

## History Page

```mermaid
flowchart TB
    subgraph HistoryPage[History Page]
        Header[Page Header: investigation history]
        Search[Search and Filters: date, agent, severity, owner, tags]
        Table[Session Table: title, agent, result, confidence, created, updated]
        Timeline[Selected Session Timeline: prompt, artifact, findings, feedback]
        Export[Bulk Actions: export, archive, share, delete]
    end

    Header --> Search
    Search --> Table
    Table --> Timeline
    Table --> Export
```

## Settings Page

```mermaid
flowchart TB
    subgraph SettingsPage[Settings Page]
        Header[Page Header: workspace settings]
        Tabs[Tabs: profile, security, notifications, integrations, preferences]
        Profile[Profile Settings: name, role, avatar, timezone]
        Security[Security Settings: password, sessions, MFA, API tokens]
        Integrations[Integrations: GitHub, Kubernetes, Terraform Cloud, observability]
        Preferences[Preferences: theme, density, default agent, data retention]
    end

    Header --> Tabs
    Tabs --> Profile
    Tabs --> Security
    Tabs --> Integrations
    Tabs --> Preferences
```

## Metrics Page

```mermaid
flowchart TB
    subgraph MetricsPage[Metrics Page]
        Header[Page Header: operational metrics]
        Range[Time Range and Environment Controls]
        subgraph Charts[Metrics Grid]
            Requests[API Request Volume]
            Errors[Error Rate]
            AgentTime[Agent Execution Time]
            Queue[Queue Depth]
            DB[Database Health]
            Cache[Redis Cache Usage]
        end
        Logs[Linked Observability: traces, logs, dashboards]
    end

    Header --> Range
    Range --> Charts
    Charts --> Logs
```

## Admin Page

```mermaid
flowchart TB
    subgraph AdminPage[Admin Page]
        Header[Page Header: administration]
        Summary[Admin Summary: users, teams, active policies, audit events]
        subgraph AdminSections[Management Sections]
            Users[User Management: roles, status, teams]
            Policies[Agent Access Policies: allowed agents, data rules]
            Audit[Audit Log: auth, admin changes, agent execution]
            System[System Controls: feature flags, provider settings, retention]
        end
        Review[Pending Review Queue: high-risk findings, access requests]
    end

    Header --> Summary
    Summary --> AdminSections
    AdminSections --> Review
```

## Information Architecture Notes

- **Dashboard** is the operational landing page and should optimize for immediate awareness and quick agent launches.
- **Chat** is the primary work surface and should preserve context between messages, artifacts, findings, and recommended commands.
- **Agent List** acts as a governed catalog where users understand each agent's purpose, permissions, supported inputs, and recent performance.
- **History** supports auditability, repeatability, and knowledge reuse through searchable AI-assisted sessions.
- **Metrics** connects product usage with platform health so SRE and platform teams can evaluate latency, errors, queues, and dependencies.
- **Admin** centralizes RBAC, policy management, audit records, feature flags, and operational controls.
