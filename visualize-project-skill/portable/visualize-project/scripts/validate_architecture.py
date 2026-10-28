#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

CONFIDENCE = {"verified", "strongly-inferred", "tentative"}
COMPONENT_TYPES = {
    "frontend","backend","service","module","database","cache","queue","worker",
    "scheduler","storage","auth","ai","external-api","notification","analytics",
    "observability","ci","registry","infrastructure","gateway","cdn","other"
}


def check_shape(model: object) -> list[str]:
    """Validate types before graph checks; untrusted JSON must not crash the CLI."""
    errors = []
    if not isinstance(model, dict):
        return ["Model must be a JSON object"]
    if model.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    try:
        stamp = datetime.fromisoformat(model.get("generated_at", "").replace("Z", "+00:00"))
        if stamp.tzinfo is None:
            raise ValueError
    except (ValueError, TypeError, AttributeError):
        errors.append("generated_at must be an ISO-8601 timestamp with timezone")
    project = model.get("project")
    if not isinstance(project, dict):
        errors.append("project must be an object")
    else:
        for key in ("name", "scope", "mode"):
            if not isinstance(project.get(key), str) or not project[key].strip():
                errors.append(f"project.{key} must be a non-empty string")
        if project.get("mode") not in ("overview", "deep"):
            errors.append("project.mode must be overview or deep")
    for collection in ("actors", "components", "relationships", "boundaries", "runtime_flows", "findings", "unknowns"):
        items = model.get(collection)
        if not isinstance(items, list):
            errors.append(f"{collection} must be an array")
            continue
        if collection in ("findings", "unknowns"):
            continue  # These intentionally accept free-form observations.
        seen = set()
        for index, item in enumerate(items):
            label = f"{collection}[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{label} must be an object")
                continue
            keys = ["id", "confidence"]
            keys += ["source", "target", "label", "kind", "direction"] if collection == "relationships" else ["name"]
            if collection == "components":
                keys += ["type", "responsibility", "ownership", "runtime"]
            for key in keys:
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"{label}.{key} must be a non-empty string")
            iid = item.get("id")
            if isinstance(iid, str):
                if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", iid):
                    errors.append(f"{label}.id must be lowercase kebab-case")
                if iid in seen:
                    errors.append(f"{label}: duplicate id {iid}")
                seen.add(iid)
            if item.get("confidence") not in ("verified", "strongly-inferred", "tentative"):
                errors.append(f"{label}: invalid confidence")
            evidence = item.get("evidence")
            if not isinstance(evidence, list) or not evidence or any(not isinstance(e, str) or not e.strip() for e in evidence):
                errors.append(f"{label}.evidence must be a non-empty array of strings")
            if collection == "relationships" and item.get("direction") != "source-to-target":
                errors.append(f"{label}.direction must be source-to-target")
            if collection == "components" and item.get("ownership") not in ("project", "external", "managed"):
                errors.append(f"{label}: invalid ownership")
            if collection == "boundaries":
                members = item.get("members")
                if not isinstance(members, list) or any(not isinstance(m, str) for m in members):
                    errors.append(f"{label}.members must be an array of strings")
            if collection == "runtime_flows":
                steps = item.get("steps")
                if not isinstance(steps, list) or not steps:
                    errors.append(f"{label}.steps must be a non-empty array")
                else:
                    for n, step in enumerate(steps, 1):
                        if not isinstance(step, dict) or any(not isinstance(step.get(k), str) or not step[k].strip() for k in ("source", "target", "label")) or type(step.get("order")) is not int or step["order"] != n:
                            errors.append(f"{label}: steps need sequential order, source, target and label")
    return errors

def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/architecture/generated").resolve()
    errors, warnings = [], []
    if not root.is_dir():
        print(f"ERROR: output directory does not exist: {root}")
        return 2

    model_path = root / "architecture-model.json"
    if not model_path.exists():
        errors.append(f"Missing {model_path}")
        model = None
    else:
        try:
            model = json.loads(model_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            errors.append(f"Invalid JSON in {model_path}: {e}")
            model = None

    if model is None and model_path.is_file() and not errors:
        errors.append("Model must be a JSON object")
    if model is not None:
        shape_errors = check_shape(model)
        errors.extend(shape_errors)
        if shape_errors:
            model = None

    if model is not None:
        required = ("schema_version","generated_at","project","actors","components","relationships","boundaries","runtime_flows","findings","unknowns")
        for key in required:
            if key not in model:
                errors.append(f"architecture-model.json missing top-level key: {key}")

        actors = model.get("actors", [])
        components = model.get("components", [])
        rels = model.get("relationships", [])
        all_nodes = actors + components
        ids = []
        for item in all_nodes:
            iid = item.get("id")
            if not iid:
                errors.append("Actor/component missing id")
                continue
            if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", iid):
                errors.append(f"Invalid id '{iid}': use lowercase kebab-case")
            ids.append(iid)
            if item.get("confidence") not in CONFIDENCE:
                errors.append(f"{iid}: invalid/missing confidence")
            if not item.get("name"):
                errors.append(f"{iid}: missing name")
            if not item.get("evidence"):
                warnings.append(f"{iid}: no evidence listed")

        if len(ids) != len(set(ids)):
            errors.append("Duplicate actor/component IDs found")

        node_ids = set(ids)
        degree = {x: 0 for x in node_ids}
        seen_rels = set()
        for rel in rels:
            rid = rel.get("id")
            if not rid:
                errors.append("Relationship missing id")
                continue
            if rid in seen_rels:
                errors.append(f"Duplicate relationship id: {rid}")
            seen_rels.add(rid)
            src, dst = rel.get("source"), rel.get("target")
            if src not in node_ids:
                errors.append(f"{rid}: unknown source '{src}'")
            if dst not in node_ids:
                errors.append(f"{rid}: unknown target '{dst}'")
            if src in degree: degree[src] += 1
            if dst in degree: degree[dst] += 1
            if not rel.get("label"):
                errors.append(f"{rid}: missing relationship label")
            if rel.get("confidence") not in CONFIDENCE:
                errors.append(f"{rid}: invalid/missing confidence")
            if not rel.get("evidence"):
                warnings.append(f"{rid}: no evidence listed")
            if rel.get("kind") in {"sync-request","async-message","auth","notification"} and not rel.get("protocol"):
                warnings.append(f"{rid}: protocol/mechanism missing")

        for cid, deg in degree.items():
            if deg == 0:
                warnings.append(f"{cid}: isolated node with no relationships")

        for c in components:
            ctype = c.get("type")
            if ctype and ctype not in COMPONENT_TYPES:
                warnings.append(f"{c.get('id')}: non-standard component type '{ctype}'")
            if ctype in {"frontend","backend","service","database","queue","worker","storage","auth","ai"} and not c.get("technology"):
                warnings.append(f"{c.get('id')}: technology not listed")

        for b in model.get("boundaries", []):
            for member in b.get("members", []):
                if member not in node_ids:
                    errors.append(f"Boundary {b.get('id','<unknown>')}: unknown member '{member}'")

        for flow in model.get("runtime_flows", []):
            for step in flow.get("steps", []):
                if step.get("source") not in node_ids:
                    errors.append(f"Flow {flow.get('id')}: unknown source {step.get('source')}")
                if step.get("target") not in node_ids:
                    errors.append(f"Flow {flow.get('id')}: unknown target {step.get('target')}")

    ddir = root / "diagrams"
    if not ddir.is_dir():
        errors.append(f"Missing diagrams directory: {ddir}")
    else:
        sources = list(ddir.glob("*.mmd")) + list(ddir.glob("*.d2"))
        if not sources:
            errors.append("No .mmd or .d2 diagram sources found")
        for src in sources:
            svg = src.with_suffix(".svg")
            if not svg.is_file():
                errors.append(f"Missing rendered SVG for {src.name}")
            else:
                try:
                    svg_text = svg.read_text(encoding="utf-8")
                    if "<!DOCTYPE" in svg_text.upper() or "<!ENTITY" in svg_text.upper():
                        raise ValueError("DTD/entity declarations are not supported")
                    element = ET.fromstring(svg_text)
                    if element.tag != "{http://www.w3.org/2000/svg}svg":
                        raise ValueError("Expected SVG root with SVG namespace")
                except (OSError, ValueError, ET.ParseError) as exc:
                    errors.append(f"Invalid SVG {svg.name}: {exc}")
            if src.suffix == ".mmd":
                text = src.read_text(encoding="utf-8", errors="replace")
                if "classDef" not in text:
                    warnings.append(f"{src.name}: no semantic classDef styling found")
                if "legend" not in text.lower():
                    warnings.append(f"{src.name}: no obvious in-diagram legend marker")
                for i, line in enumerate(text.splitlines(), start=1):
                    s = line.strip()
                    if "-->" in s and "|" not in s and not s.startswith(("%%", "class ", "linkStyle ")):
                        warnings.append(f"{src.name}:{i}: arrow may be unlabeled: {s[:120]}")

    md_files = list(root.glob("*.md"))
    if not md_files:
        errors.append("Missing OVERVIEW.md or DEEP_DIVE.md")
    else:
        if not any(p.name in {"OVERVIEW.md", "DEEP_DIVE.md"} for p in md_files):
            errors.append("No standard OVERVIEW.md or DEEP_DIVE.md found")
        for md in md_files:
            text = md.read_text(encoding="utf-8", errors="replace")
            if "Verification" not in text:
                warnings.append(f"{md.name}: missing Verification section")
            for match in re.finditer(r"\]\(([^)]+\.svg)\)", text):
                target = (md.parent / match.group(1)).resolve()
                if not target.is_relative_to(root):
                    errors.append(f"{md.name}: SVG link escapes output directory")
                elif not target.is_file():
                    errors.append(f"{md.name}: broken SVG link {match.group(1)}")

    if model is not None:
        mode = model["project"]["mode"]
        document = "OVERVIEW.md" if mode == "overview" else "DEEP_DIVE.md"
        stems = ["project-overview"] if mode == "overview" else ["01-system-context", "02-container-landscape"]
        if not (root / document).is_file():
            errors.append(f"{mode} mode requires {document}")
        for stem in stems:
            if not any((ddir / (stem + ext)).is_file() for ext in (".mmd", ".d2")):
                errors.append(f"{mode} mode requires diagram {stem}")

    print(f"Architecture package: {root}")
    for w in warnings: print(f"WARNING: {w}")
    for e in errors: print(f"ERROR: {e}")
    print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except OSError as exc:
        print(f"ERROR: Cannot read architecture package: {exc}")
        raise SystemExit(2)
