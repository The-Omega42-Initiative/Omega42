import json
import unittest
from pathlib import Path
from tools.omega42_k4_reference import analyze

FIXTURE = json.loads(Path("tests/fixtures/omega42-k4-vectors.json").read_text(encoding="utf-8"))

class K4ReferenceTests(unittest.TestCase):
    def test_all_shared_vectors_match_expected(self):
        for case in FIXTURE["cases"]:
            result = analyze(case)
            expected = case["expected"]
            for key, value in expected.items():
                self.assertEqual(result[key], value, case["id"])

    def test_depths_and_normalization(self):
        self.assertEqual(sorted({c["depth"] for c in FIXTURE["cases"]}), [1, 2, 3])
        for case in FIXTURE["cases"]:
            result = analyze(case)
            self.assertEqual(result["state"], [str(int(case["state"][0]) % int(result["modulus"])),
                                               str(int(case["state"][1]) % int(result["modulus"]))])

if __name__ == "__main__":
    unittest.main()
