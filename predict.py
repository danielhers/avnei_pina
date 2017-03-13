#!/usr/bin/python3

import sys
import csv
from itertools import product


def ngram(L, n, C):
    T = L[-n+1:]
    return sorted(set(t for l in product(*T) if l in C for t in max(C[l].items())[1]))


def predict(L, n, C, m):
    P = [[l] for l in L]
    while len(P) < m:
        P.append(ngram(P, n, C))
    return P


if len(sys.argv) < 4:
    print("Usage: %s counts m word ..." % sys.argv[0])
    sys.exit(1)
with open(sys.argv[1]) as f:
    C = {}
    for l in csv.reader(f, delimiter="\t"):
        t = l[0].split() 
        C.setdefault(tuple(t[:-1]), {}).setdefault(int(l[1]), []).append(t[-1])
P = predict(sys.argv[3:], 1+len(next(iter(C.keys()))), C, int(sys.argv[2]))
print(" ".join(map("/".join, P)))
