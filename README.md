# Visualize Project

Turn repository evidence into an architecture model, editable diagrams, and a verification record using your coding agent.

This is an **agent skill**, not a standalone diagram generator. Its distinguishing approach is to record components, relationships, source evidence, and uncertainty in one JSON model before drawing multiple views. Python utilities install the skill and check the structure of its output. Your agent performs discovery, diagram authoring, rendering, and visual review.

**Status:** development preview. Utility regression tests exist; cross-host agent behavior and diagram quality have not yet been independently evaluated. Do not treat validator success as proof of factual accuracy or visual quality.

## First use

Prerequisites: Python **3.12+** and a coding agent that can load local skills, read repository files, and run commands. The Python utilities use only the standard library; there is no pip install step, server, API key, or database configuration.

From this repository root:

```sh
python -m unittest discover -s visualize-project-skill/tests -v
python visualize-project-skill/install.py --target codex --scope project --project-root /absolute/path/to/your/repo
```

Choose `cursor`, `claude`, or `codex`. Use an existing scratch repository for your first attempt. See [installation](visualize-project-skill/INSTALL.md) for paths, replacement behavior, and host caveats. Reload the host's skill discovery after installation if needed.

In your coding agent, select the installed `visualize-project` skill and request `overview`. The target instructions describe intended command forms. Use `deep` for separate context, container, and other evidence-supported views.

Expected overview output in the analyzed repository:

```text
docs/architecture/generated/
  architecture-model.json
  OVERVIEW.md
  diagrams/project-overview.mmd
  diagrams/project-overview.svg
```

Validate it using the installed script (Codex project path shown):

```sh
python /absolute/path/to/your/repo/.codex/skills/visualize-project/scripts/validate_architecture.py /absolute/path/to/your/repo/docs/architecture/generated
```

Exit `0` means structural checks passed; review warnings. Exit `1` means invalid output. Exit `2` means the package could not be accessed. Read the generated verification record, compare source evidence, and inspect every rendered diagram before sharing it.

Rendering requires an independently installed Mermaid CLI (`mmdc`) or D2. The skill also describes optional transient `npx` execution, which downloads and executes third-party software and is not version-pinned. Review your host's execution policy. If rendering or visual inspection is unavailable, the skill must report incomplete verification.

## What is implemented

- Portable instructions and three host wrappers, with `overview` and `deep` output contracts.
- An installer that stages replacements and rolls back ordinary publish failures.
- Structural checks for model types, evidence presence, graph references, mode-required files, SVG XML, and local SVG links.
- Offline installation regression tests and a small [validator evaluation](visualize-project-skill/tests/evaluate_validator.py).

There is no bundled agent runner or renderer. The [example JSON](visualize-project-skill/portable/visualize-project/assets/architecture-model.example.json) is illustrative, not evidence of a real analyzed application. Tests deliberately use synthetic SVG; they do not demonstrate rendering or model-to-diagram fidelity.

## Boundaries and privacy

The Python utilities make no network requests and collect no telemetry. The agent host may send repository content to its provider under your account settings. Generated models persist repository paths and architecture details; inspect them before publishing and delete `docs/architecture/generated/` when no longer needed. Never include credentials or `.env` values. The validator checks structure, not secret absence, SVG safety, evidence truth, or authorization in the analyzed system. Do not open untrusted SVG as active content without review.

## Development and documentation

- [Architecture and implementation limits](visualize-project-skill/DESIGN_NOTES.md)
- [Output contracts](visualize-project-skill/portable/visualize-project/references/mode-contracts.md)
- [Verification rubric](visualize-project-skill/portable/visualize-project/references/verification-rubric.md)
- [Contributing](CONTRIBUTING.md)
- [Audit and verification results](AUDIT.md)
- [MIT license](LICENSE)

The Python code has no third-party runtime dependencies. Host and renderer versions remain external variables. CI is configured for Windows and Linux, Python 3.12 and 3.14; a workflow file alone is not evidence of a green hosted run.
