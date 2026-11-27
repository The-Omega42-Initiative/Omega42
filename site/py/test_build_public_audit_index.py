"""Synthetic publication tests; no certificate execution or real consent."""
import unittest
from build_public_audit_index import build_index
from test_validate_audit_receipts import BASE, REV, ROWS

ROWS = [dict(row, status="EXACT") for row in ROWS]
APPROVAL = dict(audit_id=BASE["audit_id"], revision=REV,
                verdict="PASS", public_consent=True,
                review_status="HUMAN_APPROVED")

class PublicIndexTests(unittest.TestCase):
    def test_no_approval_no_publication(self):
        result = build_index(ROWS, [BASE], [], REV)
        self.assertEqual(result["records"]["MF-TEST"]["audits"], [])

    def test_allowlist(self):
        result = build_index(ROWS, [BASE], [APPROVAL], REV)
        self.assertEqual(result, {"revision": REV, "records": {
            "MF-TEST": {"inherited_status": "EXACT", "audits": [{
                "verdict": "PASS", "review_status": "HUMAN_APPROVED",
                "evidence_status": "REVIEWED_RECEIPT_NOT_LOCAL_EXECUTION"
            }]}}})

    def test_reject_invalid_approval(self):
        for key, value in [
            ("audit_id", "unknown"), ("revision", "c"*40),
            ("verdict", "FAIL"), ("public_consent", False),
            ("public_consent", 1), ("review_status", "PENDING")
        ]:
            with self.subTest(key=key, value=value):
                with self.assertRaises(ValueError):
                    build_index(ROWS, [BASE], [dict(APPROVAL, **{key: value})], REV)

    def test_duplicate_approval(self):
        with self.assertRaises(ValueError):
            build_index(ROWS, [BASE], [APPROVAL, APPROVAL], REV)

    def test_invalid_receipt_even_without_approval(self):
        with self.assertRaises(ValueError):
            build_index(ROWS, [dict(BASE, revision="c"*40)], [], REV)

if __name__ == "__main__":
    unittest.main()
