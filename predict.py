#!/usr/bin/python3

import sys
import csv

def ngram(L, n, C):
    T = tuple(L[-n+1:])
    try:
        return max(C[T])[1]
    except:
        print("Not found: " + str(T))

def predict(L, n, counts_file, m):
    while len(L) < m:
        L.append(ngram(L, n, C))
    return L

if len(sys.argv) < 4:
    print("Usage: %s counts m word ..." % sys.argv[0])
    sys.exit(1)
with open(sys.argv[1]) as f:
    C = {}
    for l in csv.reader(f, delimiter="\t"):
        t = l[0].split() 
        C.setdefault(tuple(t[:-1]), []).append((int(l[1]), t[-1]))
print(" ".join(predict(list(sys.argv[3:]), 1+len(next(iter(C.keys()))), C, int(sys.argv[2]))))
