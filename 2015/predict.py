#!/usr/bin/python3

import sys
import csv
from itertools import product


def argmax(l, C):
    return max(C[l].items())[1]


def select(T, C):
    return sorted(set(t for l in product(*T) if l in C for t in argmax(l, C)))


def ngram(L, n, C):
    return select(L[-n+1:], C)


def predict(L, n, C, m):
    P = [[l] for l in L]
    while len(P) < m:
        P.append(ngram(P, n, C))
    return P


def load_counts(filename):
    with open(filename) as f:
        C = {}
        for l in csv.reader(f, delimiter="\t"):
            t = l[0].split() 
            C.setdefault(tuple(t[:-1]), {}).setdefault(int(l[1]), []).append(t[-1])
    return C


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: %s counts m word ..." % sys.argv[0])
        sys.exit(1)
    C = load_counts(sys.argv[1])
    P = predict(sys.argv[3:], 1+len(next(iter(C.keys()))), C, int(sys.argv[2]))
    print(" ".join(map("/".join, P)))
