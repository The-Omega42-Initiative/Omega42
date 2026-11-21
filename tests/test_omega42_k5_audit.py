import copy
import json
import unittest
from pathlib import Path
from tools.omega42_k5_audit import audit

FIXTURE = Path("tests/fixtures/omega42-k5-proof-obligations.json")

class K5AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_fixture_has_valid_dependency_graph(self):
        result = audit(self.data)
        self.assertTrue(result["valid"], result["errors"])
        self.assertEqual(result["obligationCount"], 12)
        self.assertFalse(result["proofValidityCertified"])

    def test_rejects_depth_convention_drift(self):
        data = copy.deepcopy(self.data)
        data["convention"]["relation"] = "n=d"
        result = audit(data)
        self.assertFalse(result["valid"])
        self.assertTrue(any("n=2d" in e for e in result["errors"]))

    def test_rejects_unknown_dependency(self):
        data = copy.deepcopy(self.data)
        data["obligations"][0]["dependsOn"] = ["MISSING"]
        result = audit(data)
        self.assertFalse(result["valid"])
        self.assertTrue(any("unknown dependency" in e for e in result["errors"]))

    def test_rejects_dependency_cycle(self):
        data = copy.deepcopy(self.data)
        data["obligations"][0]["dependsOn"] = ["ALG-002"]
        result = audit(data)
        self.assertFalse(result["valid"])
        self.assertTrue(any("cycle" in e for e in result["errors"]))

    def test_rejects_unrecognized_status(self):
        data = copy.deepcopy(self.data)
        data["obligations"][0]["status"] = "proved-by-ci"
        result = audit(data)
        self.assertFalse(result["valid"])
        self.assertTrue(any("invalid status" in e for e in result["errors"]))

if __name__ == "__main__":
    unittest.main()
