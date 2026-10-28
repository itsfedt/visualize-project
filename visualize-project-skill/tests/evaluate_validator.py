"""Compare structural rejection against any validator version, without a renderer."""
import argparse
import copy
import json
from pathlib import Path
import tempfile
import time

from test_workflow import VALIDATOR, fixture, run_validator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validator", type=Path, default=VALIDATOR)
    parser.add_argument("--baseline", action="store_true", help="Use a file-presence-only check as the baseline")
    args = parser.parse_args()
    if not args.baseline and not args.validator.is_file():
        parser.error(f"Validator file not found: {args.validator}")
    cases = ["valid", "non-object", "null-components", "bad-item", "missing-evidence",
             "dangling-edge", "invalid-svg", "wrong-mode", "bad-version", "bad-timestamp"]
    results = []
    start = time.perf_counter()
    for case in cases:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = copy.deepcopy(fixture(root))
            if case == "non-object": model = []
            elif case == "null-components": model["components"] = None
            elif case == "bad-item": model["actors"] = [42]
            elif case == "missing-evidence": model["relationships"][0]["evidence"] = []
            elif case == "dangling-edge": model["relationships"][0]["target"] = "absent"
            elif case == "invalid-svg": (root / "diagrams/project-overview.svg").write_text("broken")
            elif case == "wrong-mode": model["project"]["mode"] = "deep"
            elif case == "bad-version": model["schema_version"] = "99"
            elif case == "bad-timestamp": model["generated_at"] = "yesterday"
            (root / "architecture-model.json").write_text(json.dumps(model), encoding="utf-8")
            if args.baseline:
                from types import SimpleNamespace
                present = all((root / p).is_file() for p in (
                    "architecture-model.json", "OVERVIEW.md", "diagrams/project-overview.mmd", "diagrams/project-overview.svg"))
                result = SimpleNamespace(returncode=0 if present else 1, stderr="")
            else:
                result = run_validator(root, args.validator.resolve())
            expected = 0 if case == "valid" else 1
            results.append({"case": case, "pass": result.returncode == expected and "Traceback" not in result.stderr,
                            "exit": result.returncode, "crashed": "Traceback" in result.stderr})
    print(json.dumps({"cases": results, "passed": sum(r["pass"] for r in results),
                      "total": len(results), "seconds": round(time.perf_counter() - start, 3)}, indent=2))
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
