# Design Notes

The skill uses a model-first workflow:

```text
Repository evidence
→ architecture-model.json
→ multiple diagram views
→ render
→ visual inspection
→ verification record
```

This gives the agent a shared basis for diagrams. It does not mechanically
prevent model-to-diagram contradictions; evidence and visual review remain necessary.

Modes are intentionally asymmetric:
- `overview` gives one recognizable architecture map plus explanation and legend.
- `deep` creates an architecture atlas with C4-style zoom levels and supporting runtime/deployment/security/CI views only when evidence warrants them.

Mermaid is the primary portable source format. D2 is optional for dense layouts.

The validator checks core model types, schema version, timestamp, evidence
presence, ID uniqueness, relationship endpoints, boundary membership, flow
endpoints, mode-required files, SVG XML roots, and local SVG links. Several
Mermaid styling checks are warnings. It does not parse Mermaid or D2 syntax,
render diagrams, compare diagrams to the model, verify source evidence, detect
all secrets, or sanitize active SVG content. Automated validation does not
replace rendering, evidence review, or visual inspection.

## Runtime and distribution

`install.py` copies `portable/visualize-project` and replaces its `SKILL.md` with
`targets/<host>/SKILL.md`. The three wrappers duplicate the portable workflow;
keep their bodies aligned when editing. Supporting references, assets, and the
validator are copied unchanged. No service, database, API, or deployment exists.

The host agent interprets the installed instructions and writes generated files
inside the analyzed repository. It may invoke an external Mermaid/D2 renderer.
The Python utilities use only the standard library and do not make network calls.
Host model costs, privacy, tool permissions, and renderer versions are external
dependencies; this distribution does not control them.

The installer rejects linked destination paths and stages before replacement.
It can recover from ordinary publication errors, but concurrent installations
and process/power loss during the rename window are not transactional.
