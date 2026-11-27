"""Regression fixtures only: no mathematical certificate is executed."""
import copy
import unittest
from validate_audit_receipts import validate

REV = "a" * 40
ROWS = [{"id": "MF-TEST", "tool": "tools/example.py"}]
BASE = dict(record_id="MF-TEST", revision=REV, certificate="tools/example.py",
            audit_id="fixture-1", verdict="PASS", auditor="fixture",
            environment="fixture", command="not executed", executed_at="2026-11-27T00:00:00Z",
            output_sha256="b"*64, exit_code=0, expected_marker_observed=True)

class AuditReceiptTests(unittest.TestCase):
    def test_valid_structure(self):
        self.assertEqual(validate([BASE], ROWS, REV), 1)

    def test_invalid_fields(self):
        for key, value in [
            ("record_id", "unknown"), ("revision", "c"*40),
            ("certificate", "other.py"), ("audit_id", ""),
            ("verdict", "APPROVED"), ("auditor", ""), ("environment", ""),
            ("command", ""), ("executed_at", ""), ("output_sha256", "invalid"),
            ("exit_code", True), ("exit_code", 1), ("expected_marker_observed", False),
            ("expected_marker_observed", 1)]:
            with self.subTest(key=key, value=value):
                receipt = dict(BASE, **{key: value})
                with self.assertRaises(ValueError):
                    validate([receipt], ROWS, REV)

    def test_duplicate(self):
        with self.assertRaises(ValueError):
            validate([BASE, copy.deepcopy(BASE)], ROWS, REV)

    def test_nonexecution(self):
        for verdict in ("NOT_EXECUTED", "SOURCE_REPORTED"):
            receipt = {k: BASE[k] for k in ("record_id", "revision", "certificate", "audit_id")}
            receipt["verdict"] = verdict
            self.assertEqual(validate([receipt], ROWS, REV), 1)
            with self.assertRaises(ValueError):
                validate([dict(receipt, exit_code=0)], ROWS, REV)

    def test_unpinned(self):
        with self.assertRaises(ValueError):
            validate([], ROWS, "main")

if __name__ == "__main__":
    unittest.main()
