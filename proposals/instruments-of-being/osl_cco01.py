"""CCO-01 exact optimization for candidates sharing one fixed mode per harmonic."""
from itertools import combinations
def capacity(candidates):
    return len(set().union(*map(set,candidates)))
def greedy(candidates,budget):
    if not 0<=budget<=len(candidates): raise ValueError("invalid budget")
    selected=[]; covered=set()
    for _ in range(budget):
        i=max((i for i in range(len(candidates)) if i not in selected),key=lambda i:(len(set(candidates[i])-covered),-i))
        selected.append(i); covered.update(candidates[i])
    return tuple(selected),len(covered)
def optimal(candidates,budget):
    if not 0<=budget<=len(candidates): raise ValueError("invalid budget")
    return max(((s,capacity([candidates[i] for i in s])) for s in combinations(range(len(candidates)),budget)),key=lambda x:x[1])
def selftest():
    c=[{1,2,4,5},{1,2,3},{4,5,6}]
    assert greedy(c,2)[1]==5
    assert optimal(c,2)[1]==6
if __name__=="__main__": selftest()
