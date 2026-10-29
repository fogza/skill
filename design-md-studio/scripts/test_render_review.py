"""Behavioral checks: run with python3 -m unittest discover -s scripts."""

import copy
import json
from pathlib import Path
import tempfile
import unittest

from render_review import check_sources, prepare, render


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project"
        self.root.mkdir()
        self.design = self.root / "DESIGN.md"
        self.design.write_text("# Existing design\n", encoding="utf-8")
        self.data = {
            "title": "Review", "project_root": str(self.root), "sources": ["DESIGN.md"],
            "tokens": [{"id":"background","path":"colors.background","group":"colors","value":"#ffffff","origin":"observed"}],
            "bindings": {"light":{"background":"background"}}
        }

    def test_render_is_read_only_and_has_stable_revision(self):
        original = self.design.read_bytes()
        state = render(self.data, Path(self.temp.name) / "review.html")
        self.assertEqual(original, self.design.read_bytes())
        self.assertEqual(state["base_revision"], prepare(self.data)["base_revision"])
        self.assertEqual(["DESIGN.md"], [p.name for p in self.root.iterdir()])

    def test_detects_changed_and_missing_source(self):
        state = prepare(self.data)
        check_sources(state)
        self.design.write_text("# Concurrent edit\n")
        with self.assertRaisesRegex(ValueError, "Source changed"):
            check_sources(state)
        self.design.unlink()
        with self.assertRaises(ValueError):
            check_sources(state)

    def test_empty_project_and_prose_are_supported(self):
        self.data.update(sources=[], tokens=[], bindings={})
        self.assertEqual([], prepare(self.data)["tokens"])
        self.data["tokens"] = [{"id":"brief","path":"Overview","group":"prose","value":"Unknown audience","origin":"proposed"}]
        self.assertEqual("Unknown audience", prepare(self.data)["tokens"][0]["value"])

    def test_rejects_duplicate_ids_and_broken_bindings(self):
        self.data["tokens"].append(copy.deepcopy(self.data["tokens"][0]))
        with self.assertRaisesRegex(ValueError,"Duplicate"):
            prepare(self.data)
        self.data["tokens"].pop()
        self.data["bindings"]["light"]["background"] = "missing"
        with self.assertRaisesRegex(ValueError,"Unknown preview"):
            prepare(self.data)

    def test_rejects_paths_outside_project(self):
        (Path(self.temp.name) / "outside").write_text("private")
        for relative in ("../outside", str(self.design)):
            self.data["sources"] = [relative]
            with self.assertRaises(ValueError):
                prepare(self.data)
        (self.root / "linked").symlink_to(Path(self.temp.name) / "outside")
        self.data["sources"] = ["linked"]
        with self.assertRaises(ValueError):
            prepare(self.data)

    def test_no_project_output_or_overwrite(self):
        with self.assertRaisesRegex(ValueError,"outside project"):
            render(self.data, self.root / "review.html")
        path = Path(self.temp.name) / "existing.html"
        path.write_text("keep")
        with self.assertRaises(FileExistsError):
            render(self.data, path)
        self.assertEqual("keep", path.read_text())
        with self.assertRaises(ValueError):
            render(self.data, Path(self.temp.name) / "DESIGN.md")

    def test_escapes_script_terminators_without_corrupting_data(self):
        attack = '</script><script>globalThis.bad=true</script>'
        self.data["title"] = attack
        path = Path(self.temp.name) / "safe.html"
        render(self.data, path)
        html = path.read_text()
        self.assertNotIn(attack, html)
        embedded = html.split("const data = ",1)[1].split(";\n",1)[0]
        self.assertEqual(attack, json.loads(embedded)["title"])

    def test_invalid_payload_and_nonfinite_values(self):
        self.data["tokens"][0]["value"] = float("nan")
        with self.assertRaises(ValueError):
            prepare(self.data)
        self.data["tokens"][0]["value"] = "#fff"
        self.data["bindings"] = []
        with self.assertRaises(ValueError):
            prepare(self.data)

    def test_original_and_proposal_are_independent(self):
        token = self.data['tokens'][0]
        token.update(original_value='#eeeeee',original_path='colors.old-background',value='#ffffff')
        actual=prepare(self.data)['tokens'][0]
        self.assertEqual('#eeeeee',actual['original_value'])
        self.assertEqual('#ffffff',actual['value'])

    def test_preparing_an_existing_snapshot_is_idempotent(self):
        first=prepare(self.data)
        self.assertEqual(first,prepare(first))


if __name__ == "__main__":
    unittest.main()
