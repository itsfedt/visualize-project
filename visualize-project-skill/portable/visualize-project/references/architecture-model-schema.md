# Architecture Model Schema

Create `docs/architecture/generated/architecture-model.json`.

Use JSON so the model can be mechanically validated with standard tooling.

## Required shape

```json
{
  "schema_version": "1.0",
  "generated_at": "ISO-8601 timestamp",
  "project": {"name": "...", "scope": "repository", "mode": "overview|deep"},
  "actors": [],
  "components": [],
  "relationships": [],
  "boundaries": [],
  "runtime_flows": [],
  "findings": [],
  "unknowns": []
}
```

## Actor

```json
{
  "id": "actor-user",
  "name": "End User",
  "description": "Uses the application.",
  "evidence": ["README.md"],
  "confidence": "verified"
}
```

## Component

```json
{
  "id": "mobile-app",
  "name": "Mobile App",
  "type": "frontend",
  "technology": ["React Native", "Expo"],
  "responsibility": "User-facing mobile client.",
  "ownership": "project",
  "runtime": "mobile-device",
  "deployment_environment": ["production"],
  "evidence": ["apps/mobile/package.json"],
  "confidence": "verified",
  "tags": ["mobile", "client"]
}
```

Common `type` values: `frontend`, `backend`, `service`, `module`, `database`, `cache`, `queue`, `worker`, `scheduler`, `storage`, `auth`, `ai`, `external-api`, `notification`, `analytics`, `observability`, `ci`, `registry`, `infrastructure`, `gateway`, `cdn`, `other`.

Ownership: `project`, `external`, or `managed`.

## Relationship

```json
{
  "id": "mobile-to-api",
  "source": "mobile-app",
  "target": "api",
  "direction": "source-to-target",
  "kind": "sync-request",
  "label": "Calls application API",
  "protocol": "HTTPS/JSON",
  "data": ["authenticated requests"],
  "evidence": ["apps/mobile/src/api/client.ts"],
  "confidence": "verified"
}
```

Common `kind`: `sync-request`, `async-message`, `data-read`, `data-write`, `auth`, `notification`, `build`, `deploy`, `observability`, `control`, `other`.

Every endpoint must reference an existing actor/component ID.

## Boundary

```json
{
  "id": "project-system",
  "name": "Project-owned system",
  "type": "ownership",
  "members": ["mobile-app", "api"],
  "description": "Components maintained by this project.",
  "evidence": ["repository structure"],
  "confidence": "verified"
}
```

Useful boundary types: `ownership`, `trust`, `network`, `environment`, `deployment`, `subsystem`.

## Runtime flow

```json
{
  "id": "flow-save-item",
  "name": "Save item",
  "description": "Main save workflow.",
  "steps": [{"order": 1, "source": "actor-user", "target": "mobile-app", "label": "Submits item"}],
  "evidence": ["..."],
  "confidence": "verified"
}
```

## Finding / unknown

Use findings for meaningful observations/contradictions and unknowns for unresolved architectural questions.

## Rules

- IDs are lowercase kebab-case and stable across reruns.
- Evidence paths are repository-relative.
- Never include secret values or `.env` values.
- Technology is included only when evidenced.
- Relationship direction must match its label.
- Planned components must have a status such as `planned` and must not look current in diagrams.

## Executable validation boundary

The validator accepts schema version `1.0` and requires a timezone-bearing
ISO-8601 `generated_at`. All top-level collections above are arrays. Actors,
components, relationships, boundaries, and flows are objects with stable IDs,
confidence, and non-empty evidence string arrays. Relationships use `label`
instead of `name`; direction is `source-to-target`. Flow step orders start at
1 and are sequential. Findings and unknowns remain free-form array entries.

Evidence presence is checked, not whether the cited file exists or proves the
claim. This prose contract is not a complete machine-readable JSON Schema;
optional metadata and semantic correctness still need review. SVG XML checks
establish file structure only, not successful rendering or safe active content.
