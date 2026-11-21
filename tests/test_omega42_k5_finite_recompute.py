import unittest
from tools.omega42_k5_finite_recompute import analyze_depth

class K5FiniteRecomputationTests(unittest.TestCase):
    def test_depth_one(self):
        r = analyze_depth(1)
        self.assertEqual(r["orbitCount"], 5)
        self.assertEqual(r["periods"], {"1": 1, "8": 1, "24": 3})
        self.assertTrue(r["lambdaDistinctAcrossOrbits"])
        self.assertTrue(r["k1MatchesLongestPeriod"])
        self.assertTrue(r["k2SeedUnique"])

    def test_depth_two(self):
        r = analyze_depth(2)
        self.assertEqual(r["orbitCount"], 41)
        self.assertEqual(r["periods"], {"1": 1, "8": 1, "24": 3, "72": 9, "216": 27})
        self.assertTrue(r["lambdaDistinctAcrossOrbits"])
        self.assertTrue(r["k1MatchesLongestPeriod"])
        self.assertTrue(r["k2SeedUnique"])

    def test_depth_three(self):
        r = analyze_depth(3)
        self.assertEqual(r["totalStates"], "531441")
        self.assertEqual(r["orbitCount"], 365)
        self.assertEqual(r["periods"], {
            "1": 1, "8": 1, "24": 3, "72": 9,
            "216": 27, "648": 81, "1944": 243
        })
        self.assertTrue(r["lambdaDistinctAcrossOrbits"])
        self.assertTrue(r["lambdaConstantOnEveryOrbit"])
        self.assertTrue(r["allStatesVisited"])
        self.assertTrue(r["k1MatchesLongestPeriod"])
        self.assertEqual(r["k2SeedOccurrencesAmongLongest"], 1)

    def test_rejects_unbounded_depth(self):
        with self.assertRaises(ValueError):
            analyze_depth(4)

if __name__ == "__main__":
    unittest.main()
