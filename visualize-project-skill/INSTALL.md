# Install Visualize Project

## Quick install

Requires Git and Python 3.12+. From your terminal:

```sh
git clone https://github.com/itsfedt/visualize-project.git
cd visualize-project
python visualize-project-skill/install.py --target claude
```

Choose `--target cursor` or `--target codex` for those agents. Use `python3`
if that is your Python command. The default installs for your user account.
No Python packages or application configuration are needed.

After installation, open a repository in your agent and run
`/visualize-project overview`. In Codex, select the skill in the skill picker
and request `overview`. Start a new agent session if it does not appear.

## Instructions for an installing agent

When the user asks you to install this repository's skill:

1. Use the user's named host (`claude`, `cursor`, or `codex`). If none is named
   and you cannot identify your host, ask which one. Check for Python 3.12+;
   use `python3` if necessary. If unavailable, explain the prerequisite before
   changing the machine's Python installation.
2. Clone `https://github.com/itsfedt/visualize-project.git` into an unused scratch
   directory, or use an existing checkout of this repository. From its root,
   run `python visualize-project-skill/install.py --target <host>`. The default
   is user scope; honor project scope if the user requests it. An existing
   installation uses staged replacement and upgrades automatically.
3. Confirm exit code 0 and the reported destination contains `SKILL.md`,
   `references/`, `assets/`, and `scripts/validate_architecture.py`. Tell the
   user the destination and how to invoke overview. Report host discovery as
   unverified unless actually checked; do not generate diagrams as part of
   installation unless requested.

The installer needs the whole repository, not just a downloaded `install.py`.
It selects the appropriate host wrapper and copies the supporting files.
Host approval requirements still apply. Installation does not require running
the contributor test suite or downloading a diagram renderer.

## Project-only installation

From this repository root, append the scope and destination:

```sh
python visualize-project-skill/install.py --target claude --scope project --project-root "/path/to/your/repo"
```

If working from the inner `visualize-project-skill` distribution folder, use
`python install.py` instead. Quote paths containing spaces.

## Updates and recovery

To upgrade from an existing checkout, run these commands from its root:

```sh
git pull
python visualize-project-skill/install.py --target claude
```

Use the same target and scope as your original installation. The installer
installs the version in your checkout; it does not download updates itself.
Restart your agent session to load the updated skill.

An existing installation is upgraded automatically. Replacement
stages a complete copy first, then renames the old version to a sibling
`visualize-project.backup` while publishing. Ordinary publish failures restore
the old version. Do not run concurrent installs to the same destination. This is
not a crash-safe transaction: after interruption, inspect any `.backup` folder
before retrying. The installer refuses an existing backup and linked destination
directories (symlinks/junctions). Personal edits and extra files inside the installed skill directory are replaced;
back them up before upgrading. The old `--force` option is accepted for compatibility
but is no longer required.

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
