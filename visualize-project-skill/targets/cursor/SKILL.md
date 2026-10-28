---
name: visualize-project
description: Reverse-engineer a software repository into verified, clean architecture diagrams. Use for /visualize-project overview or deep.
disable-model-invocation: true
icon: image
color: indigo
---

# Visualize Project

Use this skill to reverse-engineer a software repository into a verified, visually clear architecture package.

## Invocation

The first argument is the mode:

- `overview` — compact architecture map. Standard package.
- `deep` — multi-diagram architecture atlas. Full package.

Intended invocations:

```text
/visualize-project overview
/visualize-project deep
```

On Codex, invoke the skill through `/skills` or use:

```text
$visualize-project overview
$visualize-project deep
```

Optional trailing scope may identify a subdirectory or subsystem, for example:

```text
/visualize-project deep backend/
```

If the mode is missing, ask the user to choose `overview` or `deep` before generating artifacts.

## Primary goal

Produce an easy-to-understand, visually appealing, evidence-backed map of how the project works as a whole.

The output must help a technically curious person answer:

- Who uses the system?
- What are the major applications/services/modules?
- Where does data live?
- How do components communicate?
- What happens during important runtime flows?
- Which external services are involved?
- How do authentication and authorization fit in?
- Where are queues/background jobs?
- How is the system deployed?
- How does CI/CD move code to environments?
- Where do notifications, analytics, observability, AI/ML, storage, and infrastructure fit?
- What are the trust/security boundaries?
- Which statements are verified and which are inferred?

Do not force every answer into one diagram. Split diagrams whenever density reduces comprehension.

## Non-goals

Do not:

- modify application behavior;
- refactor source code;
- add application dependencies solely for documentation;
- invent infrastructure, services, protocols, or data flows;
- represent planned features as deployed/current unless clearly marked;
- expose secrets or secret values in diagrams;
- create a code/class diagram unless it materially helps the requested view;
- overwrite hand-authored architecture documentation without explicit approval.

## Operating model

Use four phases:

1. **Discover**
2. **Model**
3. **Visualize**
4. **Verify**

Do not skip verification.

---

# Phase 1 — Discover

Perform a read-only architecture scan before drawing.

Read `references/repo-discovery.md` and follow its evidence hierarchy.

At minimum inspect, where present:

- README and architecture/product docs;
- AGENTS.md / CLAUDE.md / repository instructions;
- package/dependency manifests;
- source-tree entry points;
- environment example files;
- API specifications/routes;
- database schemas and migrations;
- Docker/Compose files;
- Terraform/CloudFormation/CDK/Kubernetes files;
- CI/CD workflows;
- worker/queue code;
- authentication/authorization configuration;
- notification integrations;
- analytics/observability integrations;
- cloud/provider configuration;
- tests that reveal runtime boundaries.

Use source code and executable configuration as stronger evidence than prose when they disagree. Report meaningful contradictions.

Do not read or print secret values from `.env`, credential files, key stores, or secret managers. Environment *names* may be used when discoverable from safe examples/configuration.

## Adaptive questions

Ask questions only when a missing answer would materially change the architecture map or would force an unsafe guess.

Do not ask for facts already available in the repository.

Ask questions in one concise batch, normally no more than five.

Good reasons to ask:

- two architectures are present and it is unclear which is current;
- production deployment cannot be distinguished from obsolete/local infrastructure;
- multiple applications exist but the diagram scope is unclear;
- a critical external dependency is referenced only by a placeholder;
- a major relationship cannot be safely inferred.

Otherwise continue and mark uncertainty in the model.

---

# Phase 2 — Model

Before diagramming, create/update:

```text
docs/architecture/generated/architecture-model.json
```

Use `references/architecture-model-schema.md`.

The model is the source of truth for generated diagrams.

Every component and relationship must include:

- stable ID;
- human-readable name;
- type;
- short responsibility/relationship description;
- evidence;
- confidence: `verified`, `strongly-inferred`, or `tentative`.

For components, also include technology when known.

For relationships, include protocol/mechanism when known.

Never upgrade an inference to verified merely because it seems conventional.

If architecture docs and live code disagree, represent the live implementation and record the discrepancy under `findings`.

---

# Phase 3 — Visualize

Read:

- `references/mode-contracts.md`
- `references/visual-language.md`

Use the architecture model as the basis for every generated diagram.

Default output root:

```text
docs/architecture/generated/
```

Prefer Mermaid as the portable diagram source format.

Use D2 only when:
- it is available in the environment,
- it materially improves a dense architecture/deployment diagram,
- and a Mermaid or Markdown-accessible equivalent remains available or the user explicitly prefers D2.

Always keep editable source alongside rendered output.

## Overview mode

Generate the Standard Package defined in `references/mode-contracts.md`.

Goal: a single clean map where every major part of the project is recognizable without showing internal implementation detail.

If the single overview becomes congested, create one supplemental diagram rather than shrinking labels to illegibility.

## Deep mode

Generate the Full Package defined in `references/mode-contracts.md`.

Use multiple diagrams by default.

Start with C4-style zoom levels:
- system context;
- container/application landscape.

Then add only diagrams supported by the repository and useful to understanding:
- runtime/data-flow;
- deployment/infrastructure;
- security/trust boundaries;
- CI/CD and observability;
- component-level views for complex containers.

A component view is warranted when a container has several meaningful internal responsibilities whose interaction is important. Do not create component diagrams just to satisfy a template.

## Visual style

Use a hybrid of:
- colorful teaching diagram;
- disciplined enterprise architecture diagram.

Every diagram must:
- have a descriptive title and scope;
- omit color legends and color-key panels; use clear node labels and named boundaries;
- use icons where they aid recognition;
- use a consistent semantic color palette;
- label every meaningful arrow;
- include protocol/technology on inter-process relationships when known;
- distinguish external systems from project-owned systems;
- distinguish synchronous, asynchronous, deployment/control, and data relationships;
- use boundaries/subgraphs for application, network, trust, environment, or ownership boundaries where relevant;
- remain readable without requiring a long narrative.

Prefer portable emoji/icon labels when renderer-specific icon packs are unavailable.

---

# Phase 4 — Verify

This phase is mandatory.

Read `references/verification-rubric.md`.

Verification has four layers:

## A. Evidence verification

Cross-check the generated model and diagrams against repository evidence.

Confirm:
- every major project subsystem is represented;
- no unsupported service is drawn as fact;
- component ownership is correct;
- relationship direction matches code/config;
- protocols are not invented;
- planned/optional components are clearly marked.

## B. Structural validation

Run:

```text
python <skill-dir>/scripts/validate_architecture.py docs/architecture/generated
```

Fix all errors.

Warnings require review and either correction or explicit justification.

## C. Render validation

Render every Mermaid/D2 diagram.

Preferred Mermaid commands, without adding a permanent project dependency:

```text
mmdc -i input.mmd -o output.svg
```

If `mmdc` is unavailable and network/tool policy allows transient execution:

```text
npx --yes @mermaid-js/mermaid-cli -i input.mmd -o output.svg
```

For D2:

```text
d2 input.d2 output.svg
```

Do not modify project package manifests merely to render documentation unless the user explicitly requests it.

If no renderer can be executed, report that rendering could not be independently verified and do not claim visual verification passed.

## D. Visual cleanliness review

Open/inspect every rendered SVG/PNG using available visual tools.

Reject and revise diagrams that have:
- overlapping nodes;
- clipped text;
- unreadably small labels;
- excessive edge crossings;
- ambiguous arrows;
- unbalanced whitespace that obscures hierarchy;
- meaning conveyed only by color without clear labels;
- visually indistinguishable boundaries;
- too many elements for the selected mode.

Split the diagram when necessary instead of compressing it.

Repeat render + inspection until the diagram is clean.

A successful parse is not sufficient.

---

# Quality gate

Before finalizing, score each diagram from 1–5 for:

1. factual correctness;
2. completeness for its stated scope;
3. visual legibility;
4. visual consistency;
5. standalone understandability.

No dimension may be below 4.

Also require:
- zero unresolved validator errors;
- rendered artifact exists for every source diagram;
- all blocking ambiguities are resolved or explicitly marked;
- generated Markdown links point to existing files.

If these conditions are not met, revise before reporting completion.

---

# Final response

Keep the response concise.

For `overview`, report:
- output directory;
- main overview document;
- rendered main diagram;
- number of verified vs inferred architecture elements;
- any important uncertainty.

For `deep`, additionally list the generated diagram set and any intentionally omitted view.

Do not paste the entire architecture model into chat unless asked.

Do not call the work verified if rendering or visual inspection was not actually performed.
