#!/usr/bin/python3

import sys
from itertools import product
from functools import reduce
from operator import mul

from predict import load_counts, select


def common(xs):
    return set(xs[0]).intersection(*xs[1:])


def prod(items):
    dicts = [{tuple(v): k for k, v in d} for d in items]
    return [(reduce(mul, (d[i] for d in dicts)), i) for i in common(dicts)]
    

def select2(T, C):
    return max(prod([c[(t,)].items() for l in product(*T) for t, c in zip(l, C)]))[1]


def tag1(L, Cwt):
    return [select([[l]], Cwt) for l in L]


def tag2(L, Cwt, Ct2):
    T = [select([[L[0]]], Cwt)]
    for l in L[1:]:
        T.append(select2(([l], T[-1]), (Cwt, Ct2)))
    return T


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: %s word_tag tag_ngram word ..." % sys.argv[0])
        sys.exit(1)
    Cwt, Ct2 = map(load_counts, sys.argv[1:3])
    for T in tag1(sys.argv[3:], Cwt), tag2(sys.argv[3:], Cwt, Ct2):
        print(" ".join(map("/".join, T)))
