"""Offline regression tests: no host account, renderer, or network required."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PORTABLE = ROOT / "portable" / "visualize-project"
VALIDATOR = PORTABLE / "scripts" / "validate_architecture.py"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


installer = load_module("installer", ROOT / "install.py")


def fixture(root):
    """Synthetic structural fixture, not a renderer or factual accuracy test."""
    model = json.loads((PORTABLE / "assets" / "architecture-model.example.json").read_text())
    (root / "architecture-model.json").write_text(json.dumps(model), encoding="utf-8")
    diagrams = root / "diagrams"
    diagrams.mkdir(exist_ok=True)
    (diagrams / "project-overview.mmd").write_text(
        'flowchart LR\nclient -->|Calls API| api\nclassDef service fill:#fff\n', encoding="utf-8")
    (diagrams / "project-overview.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"><text x="10" y="20">Structural fixture only</text></svg>', encoding="utf-8")
    (root / "OVERVIEW.md").write_text(
        '# Fixture\n![Diagram](diagrams/project-overview.svg)\n## Verification\nStructural fixture only.\n', encoding="utf-8")
    return model


def run_validator(root, script=VALIDATOR):
    return subprocess.run([sys.executable, str(script), str(root)], capture_output=True, text=True)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.model = fixture(self.root)

    def save(self, model):
        (self.root / "architecture-model.json").write_text(json.dumps(model), encoding="utf-8")

    def test_valid_package(self):
        result = run_validator(self.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_malformed_types_rejected_without_tracebacks(self):
        models = [None, [], 1, "text"]
        for key in self.model:
            bad = copy.deepcopy(self.model)
            bad[key] = None
            models.append(bad)
        for collection in ("actors", "components", "relationships", "boundaries", "runtime_flows"):
            for value in (None, [], 4, {"id": [], "confidence": {}}):
                bad = copy.deepcopy(self.model)
                bad[collection] = [value]
                models.append(bad)
        for model in models:
            with self.subTest(model=model):
                self.save(model)
                result = run_validator(self.root)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_dangling_endpoint_and_missing_evidence(self):
        for field, value in (("target", "missing"), ("evidence", [])):
            with self.subTest(field=field):
                model = copy.deepcopy(self.model)
                model["relationships"][0][field] = value
                self.save(model)
                self.assertEqual(run_validator(self.root).returncode, 1)

    def test_invalid_svg_and_mode_contract(self):
        svg = self.root / "diagrams" / "project-overview.svg"
        for text in ("", "not SVG", "<html/>", '<!DOCTYPE svg><svg/>'):
            with self.subTest(text=text):
                svg.write_text(text)
                self.assertEqual(run_validator(self.root).returncode, 1)
        fixture(self.root)
        self.model["project"]["mode"] = "deep"
        self.save(self.model)
        self.assertEqual(run_validator(self.root).returncode, 1)

    def test_link_cannot_escape_package(self):
        (self.root / "OVERVIEW.md").write_text('## Verification\n![x](../outside.svg)')
        result = run_validator(self.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("escapes output directory", result.stdout)

    def test_missing_root(self):
        self.assertEqual(run_validator(self.root / "missing").returncode, 2)


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dest = self.root / "skill"
        self.wrapper = ROOT / "targets" / "codex" / "SKILL.md"

    def test_all_targets_install_and_validate_from_unrelated_directory(self):
        distribution = self.root / "clean distribution"
        shutil.copytree(ROOT, distribution, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for target in ("cursor", "claude", "codex"):
            with self.subTest(target=target):
                result = subprocess.run([sys.executable, str(distribution / "install.py"), "--target", target,
                                         "--scope", "project", "--project-root", str(self.root)],
                                        cwd=self.root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                dest = self.root / f".{target}" / "skills" / "visualize-project"
                self.assertEqual((dest / "SKILL.md").read_bytes(), (ROOT / "targets" / target / "SKILL.md").read_bytes())
                for source in PORTABLE.rglob("*"):
                    if source.is_file() and "__pycache__" not in source.parts and source.name != "SKILL.md":
                        self.assertEqual(source.read_bytes(), (dest / source.relative_to(PORTABLE)).read_bytes())
                output = self.root / target
                output.mkdir()
                fixture(output)
                self.assertEqual(run_validator(output, dest / "scripts" / "validate_architecture.py").returncode, 0)

    def test_existing_install_requires_force(self):
        installer.install(PORTABLE, self.wrapper, self.dest)
        marker = self.dest / "custom.txt"
        marker.write_text("keep")
        with self.assertRaises(ValueError):
            installer.install(PORTABLE, self.wrapper, self.dest)
        self.assertEqual(marker.read_text(), "keep")
        installer.install(PORTABLE, self.wrapper, self.dest, True)
        self.assertFalse(marker.exists())

    def test_copy_failure_preserves_previous_install(self):
        self.dest.mkdir()
        (self.dest / "custom.txt").write_text("keep")
        with patch.object(installer.shutil, "copytree", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                installer.install(PORTABLE, self.wrapper, self.dest, True)
        self.assertEqual((self.dest / "custom.txt").read_text(), "keep")

    def test_publish_failure_rolls_back(self):
        self.dest.mkdir()
        (self.dest / "custom.txt").write_text("keep")
        rename = Path.rename

        def fail_publish(path, target):
            if path.parent.name.startswith(".visualize-stage-"):
                raise OSError("publish failed")
            return rename(path, target)

        with patch.object(Path, "rename", fail_publish):
            with self.assertRaises(OSError):
                installer.install(PORTABLE, self.wrapper, self.dest, True)
        self.assertEqual((self.dest / "custom.txt").read_text(), "keep")

    def test_missing_wrapper_preserves_previous_install(self):
        self.dest.mkdir()
        (self.dest / "custom.txt").write_text("keep")
        with self.assertRaises(ValueError):
            installer.install(PORTABLE, self.root / "missing", self.dest, True)
        self.assertEqual((self.dest / "custom.txt").read_text(), "keep")

    def test_linked_destination_is_rejected(self):
        with patch.object(Path, "is_symlink", return_value=True):
            with self.assertRaisesRegex(ValueError, "linked destination"):
                installer.install(PORTABLE, self.wrapper, self.dest, True)
        self.assertFalse(self.dest.exists())

    def test_backup_is_preserved_for_manual_recovery(self):
        backup = self.dest.with_name("skill.backup")
        backup.mkdir()
        (backup / "custom.txt").write_text("keep")
        with self.assertRaisesRegex(ValueError, "Recovery backup"):
            installer.install(PORTABLE, self.wrapper, self.dest)
        self.assertEqual((backup / "custom.txt").read_text(), "keep")


class DistributionTests(unittest.TestCase):
    def test_wrappers_share_portable_body(self):
        body = (PORTABLE / "SKILL.md").read_text(encoding="utf-8").split("# Visualize Project", 1)[1].strip()
        for target in ("cursor", "claude", "codex"):
            wrapper = (ROOT / "targets" / target / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(wrapper.split("# Visualize Project", 1)[1].strip(), body)


if __name__ == "__main__":
    unittest.main()
