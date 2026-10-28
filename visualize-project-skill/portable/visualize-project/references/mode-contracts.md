# Mode Contracts

Default output root:

```text
docs/architecture/generated/
```

Do not overwrite hand-authored diagrams outside this generated directory.

# Overview — Standard Package

Required:

```text
docs/architecture/generated/
├── architecture-model.json
├── OVERVIEW.md
└── diagrams/
    ├── project-overview.mmd
    └── project-overview.svg
```

If one diagram cannot remain clean, add at most one supplemental overview view rather than shrinking labels.

## Overview content

Include where evidenced: actors, frontends, backend/API, major services/processes, primary data stores, queues/workers, auth, AI, external APIs, notifications, analytics/observability, cloud/deployment boundary, and high-level CI/CD when materially relevant.

Do not show every route, table, class, CI step, or environment variable.

Target normally 8–18 primary nodes, but legibility wins over a node target.

## OVERVIEW.md

Include:
1. architecture summary;
2. rendered image;
3. how to read it;
4. legend;
5. major components table;
6. concise main flows;
7. verified vs inferred summary;
8. important unknowns/contradictions;
9. verification status.

# Deep — Full Package

Required:

```text
docs/architecture/generated/
├── architecture-model.json
├── DEEP_DIVE.md
└── diagrams/
    ├── 01-system-context.mmd
    ├── 01-system-context.svg
    ├── 02-container-landscape.mmd
    ├── 02-container-landscape.svg
    └── ... evidence-backed views
```

## Required diagrams

### System context
Show users/actors, the system in scope, and directly connected external systems. Avoid implementation detail.

### Container/application landscape
Show apps, services/processes, DB/storage, queues, major managed services, technology labels, and communication protocols.

## Conditional diagrams

Create only when relevant and evidenced:

- runtime/data-flow;
- deployment/infrastructure;
- security/trust boundaries;
- CI/CD and observability;
- component views for complex containers.

Runtime flows should be separated when combining them would become confusing.

Deployment views should not mix staging and production unless clearly partitioned.

Security views must show trust boundaries without exposing secrets.

Component views are for meaningful internal responsibilities, not low-value class maps.

## DEEP_DIVE.md

Include:
1. architecture summary;
2. diagram index;
3. each diagram embedded with 2–5 sentence explanation;
4. component inventory;
5. external dependency inventory;
6. datastore inventory;
7. communication/protocol matrix;
8. trust/security notes;
9. deployment/environment notes;
10. verified vs inferred counts;
11. findings/contradictions;
12. unknowns;
13. verification status.

Typical deep package: 4–7 diagrams. Small projects may need 3; large distributed systems may need more. Clarity wins over quota.
