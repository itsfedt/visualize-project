# Verification Rubric

Verification is mandatory in both modes.

## Evidence audit

For every diagram cross-check central components and relationships against repository evidence.

Blocking failures:
- invented provider/service;
- wrong relationship direction;
- incorrect ownership;
- obsolete deployment represented as current;
- secret value exposed.

## Structural validation

Run:

```text
python <skill-dir>/scripts/validate_architecture.py docs/architecture/generated
```

Errors block completion. Warnings require review and correction or explicit justification.

## Render validation

Every source diagram must render successfully.

Mermaid:
```text
mmdc -i diagram.mmd -o diagram.svg
```

or when allowed:
```text
npx --yes @mermaid-js/mermaid-cli -i diagram.mmd -o diagram.svg
```

D2:
```text
d2 diagram.d2 diagram.svg
```

A successful render proves syntax, not visual quality.

## Visual inspection

Open every SVG/PNG and check:
- no overlap/clipping;
- readable text;
- arrows point to intended targets;
- labels stay associated with their edges;
- main hierarchy is obvious quickly;
- external systems are separated;
- no color legend or color-key panel is included;
- no large unexplained dead zones;
- no cramped clusters;
- no gratuitous decoration.

If visual inspection cannot be performed, mark the package `rendered-not-visually-inspected` and do not claim full verification.

## C4-style review

Ask:
- Is type/scope obvious?
- Does every element have a name and understandable type?
- Is responsibility understandable?
- Is technology shown where relevant?
- Is every relationship labelled?
- Does label agree with direction?
- Is protocol shown for inter-process communication?
- Do labels and named boundaries communicate meaning without relying on color?

## Mode cleanliness

Overview: reader identifies user, client, core backend, data, async processing, external systems, and deployment/cloud shape without implementation-level detail.

Deep: each diagram answers one architectural question well. Never create one giant diagram containing runtime, deployment, CI/CD, all modules, and all tables.

## Quality score

Score 1–5:
- correctness;
- completeness for scope;
- legibility;
- consistency;
- standalone understandability.

Minimum 4 in every category. If any score is below 4: revise, rerender, inspect again.

## Final record

Include:

```text
Verification
- Structural model validation: PASS
- Diagram render validation: PASS
- Visual inspection: PASS
- Evidence cross-check: PASS
- Blocking uncertainties: 0
```

State the real status if any item is not passed.
