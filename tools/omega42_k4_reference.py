#!/usr/bin/env python3
"""Independent, standard-library-only Ω42 arithmetic reference for K4."""
import json
from pathlib import Path
import sys

def mod(n, m):
    return n % m

def step(state, modulus):
    a, b = state
    return (b % modulus, (a + b) % modulus)

def valuation3(x, cap):
    x = abs(int(x))
    if x == 0:
        return cap
    r = 0
    while r < cap and x % 3 == 0:
        x //= 3
        r += 1
    return r

def invariant(state, depth):
    modulus = 9 ** depth
    n = 2 * depth
    a, b = (int(state[0]) % modulus, int(state[1]) % modulus)
    r = min(valuation3(a, n), valuation3(b, n))
    if r == n:
        return {"valuation": r, "normModulus": "1", "normUpToSign": "0", "zeroState": True}
    q = 3 ** (n-r)
    norm = a*a + a*b - b*b
    c = (norm // (9 ** r)) % q
    canonical = min(c, (-c) % q)
    return {"valuation": r, "normModulus": str(q), "normUpToSign": str(canonical), "zeroState": False}

def period(state, modulus):
    start = (int(state[0]) % modulus, int(state[1]) % modulus)
    current = start
    seen = set()
    while current not in seen:
        seen.add(current)
        current = step(current, modulus)
    if current != start:
        raise AssertionError("Fibonacci map unexpectedly had a transient")
    return len(seen)

def analyze(case):
    depth = int(case["depth"])
    modulus = 9 ** depth
    state = [int(case["state"][0]) % modulus, int(case["state"][1]) % modulus]
    inv = invariant(state, depth)
    return {
        "id": case["id"],
        "depth": depth,
        "state": [str(state[0]), str(state[1])],
        "modulus": str(modulus),
        **inv,
        "period": period(state, modulus)
    }

def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("tests/fixtures/omega42-k4-vectors.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    print(json.dumps([analyze(case) for case in data["cases"]], separators=(",", ":"), sort_keys=True))

if __name__ == "__main__":
    main()
