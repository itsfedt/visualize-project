#!/usr/bin/env python3
from __future__ import annotations
import argparse
import shutil
import tempfile
from pathlib import Path

HOME_PATHS = {
    "cursor": Path.home()/".cursor"/"skills"/"visualize-project",
    "claude": Path.home()/".claude"/"skills"/"visualize-project",
    "codex": Path.home()/".codex"/"skills"/"visualize-project",
}
PROJECT_PATHS = {
    "cursor": Path(".cursor")/"skills"/"visualize-project",
    "claude": Path(".claude")/"skills"/"visualize-project",
    "codex": Path(".codex")/"skills"/"visualize-project",
}

def install(portable: Path, wrapper: Path, dest: Path, force: bool = False) -> None:
    """Stage a complete install before replacing a previous version.

    Callers must serialize installs to the same destination. Rollback handles
    ordinary I/O failures, not power loss or concurrent external modification.
    """
    for path in (dest, *dest.parents):
        if path.is_symlink() or path.is_junction():
            raise ValueError(f"Refusing linked destination path: {path}")
    if dest.exists() and not dest.is_dir():
        raise ValueError(f"Destination is not a directory: {dest}")
    if dest.exists() and not force:
        raise ValueError(f"Destination already exists: {dest}. Use --force to replace it.")
    if not portable.is_dir() or not wrapper.is_file():
        raise ValueError("Incomplete distribution: portable skill or target wrapper missing")
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".visualize-stage-", dir=dest.parent) as scratch:
        staged = Path(scratch) / "skill"
        shutil.copytree(portable, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copy2(wrapper, staged / "SKILL.md")
        backup = dest.with_name(dest.name + ".backup")
        if backup.exists() or backup.is_symlink():
            raise ValueError(f"Recovery backup already exists; inspect it before retrying: {backup}")
        replaced = dest.exists()
        if replaced:
            dest.rename(backup)
        try:
            staged.rename(dest)
        except OSError:
            if replaced:
                backup.rename(dest)
            raise
        if replaced:
            shutil.rmtree(backup)


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--target", choices=HOME_PATHS, required=True)
    ap.add_argument("--scope", choices=["user","project"], default="user")
    ap.add_argument("--project-root", default=".")
    ap.add_argument("--force", action="store_true")
    args=ap.parse_args()

    here=Path(__file__).resolve().parent
    portable=here/"portable"/"visualize-project"
    wrapper=here/"targets"/args.target/"SKILL.md"
    dest=HOME_PATHS[args.target] if args.scope=="user" else Path(args.project_root).resolve()/PROJECT_PATHS[args.target]

    try:
        install(portable, wrapper, dest, args.force)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1
    print(f"Installed visualize-project for {args.target}: {dest}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
