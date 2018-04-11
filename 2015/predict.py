#!/usr/bin/python3

import csv
import sys
from argparse import ArgumentParser
from operator import itemgetter

from tqdm import tqdm
from glob import glob
import re


def predict(tokens, counts_by_order):
    for n in range(len(tokens) + 1, 0, -1):
        counts = counts_by_order.get(n)
        if not counts:
            continue
        prefixes = [(t, c) for t, c in counts.items() if t[:-1] == tokens[len(tokens) + 1 - n:]]
        print("%d %s" % (n, sorted(prefixes, key=itemgetter(1), reverse=True)))
        if not prefixes:
            continue
        return max(prefixes, key=itemgetter(1))[0][-1], n
    return None, None


def load_counts(patterns):
    counts_by_order = {}
    for pattern in patterns:
        for filename in glob(pattern) or [pattern]:
            m = re.search(r"\d+", filename)
            order = int(m.group(0)) if m else None
            with open(filename, encoding="utf-8") as f:
                for key, count in tqdm(csv.reader(f), desc="Reading " + filename, unit=" lines"):
                    ngram = tuple(key.split())
                    counts_by_order.setdefault(len(ngram) if order is None else order, {})[ngram] = int(count)
    return counts_by_order


def main(args):
    counts_by_order = load_counts(args.counts)
    tokens = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            tokens = line.split()
        token, n = predict(tuple(tokens), counts_by_order)
        if token:
            tokens.append(token)
            print("[l=%d n=%d] %s" % (len(tokens), n, " ".join(tokens)))


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("counts", nargs="+")
    main(argparser.parse_args())
