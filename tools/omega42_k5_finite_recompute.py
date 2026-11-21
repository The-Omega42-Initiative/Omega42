#!/usr/bin/env python3
"""Independent finite recomputation for canonical Ω42 depths 1..3.

This is an exhaustive finite checker, not an all-depth proof. It directly
enumerates each state space, walks every orbit, checks Λ constancy and
distinctness, and reproduces K1/K2 finite criteria.
"""
import json
import sys
from collections import Counter

def v3_capped(value, cap):
    if value == 0:
        return cap
    value = abs(value)
    result = 0
    while result < cap and value % 3 == 0:
        value //= 3
        result += 1
    return result

def invariant(state, exponent):
    a, b = state
    r = min(v3_capped(a, exponent), v3_capped(b, exponent))
    if r == exponent:
        return (r, 0)
    q_modulus = 3 ** (exponent - r)
    q = a * a + a * b - b * b
    if q % (9 ** r):
        raise AssertionError("norm is not divisible by 9^r")
    c = (q // (9 ** r)) % q_modulus
    return (r, min(c, (-c) % q_modulus))

def analyze_depth(depth):
    if not isinstance(depth, int) or isinstance(depth, bool) or not 1 <= depth <= 3:
        raise ValueError("depth must be an integer from 1 through 3")
    exponent = 2 * depth
    modulus = 3 ** exponent
    total = modulus * modulus
    seen = bytearray(total)
    invariant_to_orbit = {}
    periods = Counter()
    orbit_records = []
    seed = (2 % modulus, 5 % modulus)

    for a in range(modulus):
        for b in range(modulus):
            if seen[a * modulus + b]:
                continue
            key = invariant((a, b), exponent)
            if key in invariant_to_orbit:
                raise AssertionError(f"Λ collision between distinct orbits: {key}")
            invariant_to_orbit[key] = len(orbit_records)

            x, y = a, b
            period = 0
            first_coordinates = set()
            seed_occurrences = 0
            while True:
                index = x * modulus + y
                if seen[index]:
                    if (x, y) != (a, b):
                        raise AssertionError("orbit traversal met a previously visited state")
                    break
                seen[index] = 1
                first_coordinates.add(x)
                if (x, y) == seed:
                    seed_occurrences += 1
                if invariant((x, y), exponent) != key:
                    raise AssertionError("Λ changed along an orbit")
                x, y = y, (x + y) % modulus
                period += 1
                if period > total:
                    raise AssertionError("orbit exceeded finite state-space bound")

            periods[period] += 1
            orbit_records.append({
                "period": period,
                "firstCoordinateCount": len(first_coordinates),
                "seedOccurrences": seed_occurrences
            })

    visited_count = sum(seen)
    if visited_count != total:
        raise AssertionError("orbit traversal did not cover the full state space")
    longest_period = max(item["period"] for item in orbit_records)
    longest = [item for item in orbit_records if item["period"] == longest_period]
    k1 = [item for item in orbit_records if item["firstCoordinateCount"] == modulus]
    k2_seed_occurrences = sum(item["seedOccurrences"] for item in longest)

    return {
        "status": "EXECUTED",
        "depth": depth,
        "genericExponent": exponent,
        "modulus": str(modulus),
        "totalStates": str(total),
        "orbitCount": len(orbit_records),
        "periods": {str(k): periods[k] for k in sorted(periods)},
        "lambdaDistinctAcrossOrbits": len(invariant_to_orbit) == len(orbit_records),
        "lambdaConstantOnEveryOrbit": True,
        "allStatesVisited": visited_count == total,
        "longestPeriod": longest_period,
        "longestOrbitCount": len(longest),
        "k1QualifyingOrbitCount": len(k1),
        "k1MatchesLongestPeriod": (
            len(k1) == len(longest) and all(item["period"] == longest_period for item in k1)
        ),
        "k2SeedOccurrencesAmongLongest": k2_seed_occurrences,
        "k2SeedUnique": k2_seed_occurrences == 1
    }

def main():
    depths = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [1, 2, 3]
    results = [analyze_depth(depth) for depth in depths]
    print(json.dumps({
        "schema": "omega42.k5.finite-recomputation.v1",
        "scope": "exhaustive finite state spaces only; not an all-depth proof",
        "results": results
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
