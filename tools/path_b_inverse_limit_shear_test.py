#!/usr/bin/env python3
"""Finite projections of inverse-limit 3-adic shear orbit-closure theorem."""
from collections import Counter, deque


def val(a, b, k):
    j = 0
    while j < k and a % 3**(j+1) == 0 and b % 3**(j+1) == 0:
        j += 1
    return j


def label(a, b, k, r):
    j = val(a, b, k)
    if j == k:
        return ("zero",)
    h = min(r, k-j)
    d = 3**j
    u, v = a//d, b//d
    q = (u*u+u*v-v*v) % 3**h
    return j, q*q % 3**h


def test(k, r):
    m = 3**k
    fibers = {}
    for a in range(m):
        for b in range(m):
            fibers.setdefault(label(a, b, k, r), set()).add((a, b))
    assert len(fibers) == (3**r+1)//2+(k-r)*3**(r-1)
    for key, points in fibers.items():
        if key == ("zero",):
            assert points == {(0, 0)}
            continue
        j = key[0]
        n = k-j
        h = min(r, n)
        assert len(points) == 8*3**(2*n-h-1)
        # Check transitivity by explicit BFS on A and lower B_r.
        seed = next(iter(points))
        reached = {seed}
        queue = deque([seed])
        while queue:
            a, b = queue.popleft()
            for nxt in ((b, (a+b) % m), (a, (b+3**r*a) % m)):
                assert nxt in points
                if nxt not in reached:
                    reached.add(nxt)
                    queue.append(nxt)
        assert reached == points, (k, r, key, len(reached), len(points))
        # Relative finite mass agrees with Haar cylinder mass at level k.
        assert len(points)*3**(h-1) == 8*3**(2*n-2)
    if r < k:
        deeper = {p: label(*p, k, r+1) for p in
                  ((a,b) for a in range(m) for b in range(m))}
        for key, points in fibers.items():
            children = Counter(deeper[p] for p in points)
            n = k-key[0] if key != ("zero",) else 0
            assert len(children) == (3 if n >= r+1 else 1)
            assert len(set(children.values())) == 1
    print("PASS k=%d r=%d fibers=%d" % (k, r, len(fibers)))


if __name__ == "__main__":
    for k in range(1, 5):
        for r in range(1, k+1):
            test(k, r)
    print("INVERSE LIMIT FINITE PROJECTIONS: PASS")
