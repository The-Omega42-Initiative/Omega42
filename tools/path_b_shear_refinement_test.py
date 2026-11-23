#!/usr/bin/env python3
"""Independent BFS verification of depth-shear partition refinements, k<=4."""
from collections import defaultdict, deque


def partition(k, r):
    m = 3**k
    assigned = {}
    components = []
    for a in range(m):
        for b in range(m):
            seed = (a, b)
            if seed in assigned:
                continue
            index = len(components)
            q = deque([seed])
            assigned[seed] = index
            members = []
            while q:
                x, y = q.popleft()
                members.append((x, y))
                for z in ((y, (x+y) % m), (x, (y+3**r*x) % m)):
                    if z not in assigned:
                        assigned[z] = index
                        q.append(z)
            components.append(members)
    return assigned, components


def shell(state, k):
    a, b = state
    j = 0
    while j < k and a % (3**(j+1)) == 0 and b % (3**(j+1)) == 0:
        j += 1
    return j


def test(k):
    partitions = {r: partition(k, r) for r in range(1, k+1)}
    for r in range(1, k+1):
        assigned, comps = partitions[r]
        assert len(assigned) == 3**(2*k)
        expected = (3**r+1)//2 + (k-r)*3**(r-1)
        assert len(comps) == expected, (k, r, len(comps), expected)
    for r in range(2, k+1):
        old_map, old_comps = partitions[r-1]
        new_map, new_comps = partitions[r]
        parent_to_children = defaultdict(lambda: defaultdict(int))
        for state, parent in old_map.items():
            parent_to_children[parent][new_map[state]] += 1
        for parent, children in parent_to_children.items():
            members = old_comps[parent]
            j = shell(members[0], k)
            n = k-j
            expected_children = 1 if n < r else 3
            assert len(children) == expected_children, (k, r, j, children)
            assert len({size for size in children.values()}) == 1
            assert sum(children.values()) == len(members)
        increment = 2 * 3**(r-2) * (k-r+1)
        assert len(new_comps)-len(old_comps) == increment
        print("PASS k=%d r=%d parent=%d child=%d" %
              (k, r, len(old_comps), len(new_comps)))


if __name__ == "__main__":
    for k in range(1, 5):
        test(k)
    print("SHEAR REFINEMENT: PASS")
