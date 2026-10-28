# Repository Discovery

Use this reference during the read-only discovery phase.

## Evidence hierarchy

When sources disagree, prefer evidence in roughly this order:

1. executable infrastructure/configuration and deployed-entrypoint configuration;
2. current source code and import/call boundaries;
3. database migrations/schema;
4. API definitions and generated contracts;
5. tests that exercise current behavior;
6. current CI/CD workflows;
7. repository architecture/technical documentation;
8. README/setup prose;
9. comments/TODOs;
10. naming conventions or assumptions.

Do not treat generated/vendor directories as architecture unless the application directly owns or configures them.

## Scan strategy

Start broad, then narrow.

### Repository shape
Identify monorepo vs single app, top-level services/apps, languages, generated/vendor directories, and docs roots.

Inspect common manifests such as `package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.sln`, `*.csproj`.

### Runtime entry points
Identify actual processes: web/mobile/desktop clients, APIs, workers, schedulers, CLIs, serverless functions, event consumers.

Use framework entry points, Docker `CMD/ENTRYPOINT`, process managers, task definitions, and route registration as evidence.

### Communication
Identify REST/GraphQL/gRPC/WebSocket, internal HTTP clients, queues/topics, event buses, webhooks, RPC, DB/cache connections. Capture protocols only when evidenced.

### Data
Inspect migrations, ORM models, schemas, object/blob storage, caches, search indexes, vector stores, and analytics stores. In overview mode represent logical stores, not every table.

### Authentication and authorization
Identify identity provider, session/JWT mechanism, backend authorization boundary, service identity, RLS/ACL/policies, and secret/token storage. Never read or expose secret values.

### External services
Detect payment, calendar/email/SMS/push, AI/model APIs, maps/location, analytics, error monitoring, social APIs, cloud managed services, external storage/search.

### Infrastructure/deployment
Inspect `Dockerfile*`, Compose, Terraform, CloudFormation, CDK, Kubernetes/Helm, serverless, Vercel/Netlify/Fly/Render configs. Distinguish local, CI/test, staging, and production.

### CI/CD
Inspect GitHub Actions, GitLab CI, Azure Pipelines, Jenkins, CircleCI. Identify triggers, checks, build, registry, deploy, migrations, and release gates.

### Observability
Identify logs, metrics, tracing, error monitoring, and analytics.

### Runtime flows
Find 2–6 flows that explain the system: login, primary entity creation, background processing, AI request, payment, notification, upload, deployment.

## Evidence ledger

For each material fact record:
- repository-relative source path;
- symbol/section when practical;
- what the evidence proves;
- confidence.

## Confidence

- `verified`: directly established by current code/config/schema, ideally corroborated.
- `strongly-inferred`: strongly implied by multiple signals but not demonstrated end-to-end.
- `tentative`: plausible but weakly evidenced. Keep out of the main diagram if misleading; otherwise mark clearly.

## Contradictions

If docs say one thing but current executable configuration/code says another:
- model current implementation;
- add a finding describing the mismatch;
- do not silently reconcile it.

## Adaptive questions

Ask only when necessary to avoid a materially wrong architecture. Do not ask questions already answered by the repository.
