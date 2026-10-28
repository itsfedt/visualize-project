# Install Visualize Project

This distribution contains one portable skill with native installation targets for Cursor, Claude Code, and Codex.

Requires Python 3.12 or newer. The installer and validator have no third-party
Python dependencies. A supported coding-agent host is required to execute the
skill; copying files alone does not generate architecture diagrams. Host
discovery and invocation syntax must be confirmed in your installed host version.

## Automatic installation

From the extracted distribution directory:

```bash
python install.py --target cursor --scope user
python install.py --target claude --scope user
python install.py --target codex --scope user
```

Use `--scope project --project-root /path/to/repo` to install only for one repository.

From the outer repository root, use `python visualize-project-skill/install.py`
instead of `python install.py`. Paths containing spaces must be quoted.

An existing installation is preserved unless `--force` is supplied. Replacement
stages a complete copy first, then renames the old version to a sibling
`visualize-project.backup` while publishing. Ordinary publish failures restore
the old version. Do not run concurrent installs to the same destination. This is
not a crash-safe transaction: after interruption, inspect any `.backup` folder
before retrying. The installer refuses an existing backup and linked destination
directories (symlinks/junctions). Back up personal changes before using `--force`.

To uninstall, remove only the installed `visualize-project` directory from the
selected location below. Generated repository documentation is separate and is
not removed by installation or uninstallation.

## Native locations

### Cursor
User/global: `~/.cursor/skills/visualize-project/`
Project: `<repo>/.cursor/skills/visualize-project/`

Invoke:
```text
/visualize-project overview
/visualize-project deep
```

The Cursor target is manual-only so unrelated architecture questions do not invoke it accidentally.

### Claude Code
User/global: `~/.claude/skills/visualize-project/`
Project: `<repo>/.claude/skills/visualize-project/`

Invoke:
```text
/visualize-project overview
/visualize-project deep
```

### Codex
User/global: `~/.codex/skills/visualize-project/`
Project: `<repo>/.codex/skills/visualize-project/`

The wrapper's intended invocation is:
```text
$visualize-project overview
$visualize-project deep
```
or select the installed skill in your host's skill picker. This checkout does
not include a recorded integration test against specific host versions.

## Manual installation

Copy `portable/visualize-project/` to the native directory above, then replace `SKILL.md` with the corresponding file from `targets/<tool>/SKILL.md`.

## Rendering

For full verification, make Mermaid CLI (`mmdc`) available, or permit transient use of:

```bash
npx --yes @mermaid-js/mermaid-cli
```

D2 is optional.

The skill is designed not to claim full verification if it cannot render and visually inspect the output.
