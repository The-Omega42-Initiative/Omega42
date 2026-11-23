#!/usr/bin/env python3
"""Independent orbit BFS for the *lower* depth-r Fibonacci shear; standard library."""
from collections import deque, Counter


def valuation(a, b, k):
    j = 0
    while j < k and a % (3**(j+1)) == 0 and b % (3**(j+1)) == 0:
        j += 1
    return j


def predicted_sizes(k, r):
    sizes = [1]
    for n in range(1, k+1):
        h = min(r, n)
        sizes.extend([8 * 3**(2*n-h-1)] * 3**(h-1))
    return Counter(sizes)


def test(k, r):
    m = 3**k
    visited = set()
    observed = Counter()
    for a in range(m):
        for b in range(m):
            if (a, b) in visited:
                continue
            todo = deque([(a, b)])
            visited.add((a, b))
            size = 0
            labels = set()
            while todo:
                x, y = todo.popleft()
                size += 1
                j = valuation(x, y, k)
                if j == k:
                    labels.add(("zero",))
                else:
                    n = k-j
                    h = min(r, n)
                    d = 3**j
                    u, v = x//d, y//d
                    q = (u*u+u*v-v*v) % (3**h)
                    labels.add((j, q*q % (3**h)))
                for next_state in ((y, (x+y) % m),
                                   (x, (y + 3**r*x) % m)):
                    if next_state not in visited:
                        visited.add(next_state)
                        todo.append(next_state)
            assert len(labels) == 1, (k, r, a, b, labels)
            observed[size] += 1
    assert observed == predicted_sizes(k, r), (k, r, observed)
    expected_count = (3**r+1)//2 + (k-r)*3**(r-1)
    assert sum(observed.values()) == expected_count
    assert sum(size*count for size, count in observed.items()) == m*m
    print("PASS k=%d r=%d orbits=%d" % (k, r, expected_count))


if __name__ == "__main__":
    for k in range(1, 5):
        for r in range(1, k+1):
            test(k, r)
    print("DEPTH-R SHEAR CENSUS: PASS")
