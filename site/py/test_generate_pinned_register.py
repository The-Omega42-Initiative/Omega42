"""Regression tests for the pinned register renderer (no certificate execution)."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("generator", Path(__file__).with_name("generate_pinned_register.py"))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
REV = "a" * 40

def record():
    return dict(id="MF-1", statement="|x| < 3 & <script>alert(1)</script>",
                domain="finite", derivation="proof", tool="tools/test.py",
                check="PASS:", depends="none", does_not_follow="external claim",
                status="CONDITIONAL on AP-SPACE")

class RegisterTests(unittest.TestCase):
    def test_preservation(self):
        page = g.render([record()], REV)
        self.assertIn("|x| &lt; 3 &amp; &lt;script&gt;", page)
        self.assertIn("CONDITIONAL on AP-SPACE", page)
        self.assertIn(REV + "/tools/test.py", page)
        self.assertIn("not executed", page)
        self.assertNotIn("<script>alert(1)</script>", page)
    def test_deterministic(self):
        self.assertEqual(g.render([record()], REV), g.render([record()], REV))
    def test_duplicate(self):
        with self.assertRaises(ValueError):
            g.render([record(), record()], REV)
    def test_invalid_fields(self):
        for key, value in [("statement", ""), ("status", "PROPOSED"), ("tool", "../private.py"), ("id", "bad")]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                g.render([dict(record(), **{key: value})], REV)
    def test_unpinned(self):
        with self.assertRaises(ValueError):
            g.render([record()], "main")
    def test_empty(self):
        with self.assertRaises(ValueError):
            g.render([], REV)

if __name__ == "__main__":
    unittest.main()
