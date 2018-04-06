#!/usr/bin/python3

import sys
from argparse import ArgumentParser
from operator import itemgetter

from predict import load_counts


def predict(tokens, counts_by_order):
    tags = []
    for i in range(len(tokens)):
        print(i)
        lex_counts = counts_by_order.get(0)
        scores = lex_score = {t: c for ((w, t), c) in lex_counts.items() if w == tokens[i]} if lex_counts else {}
        print("  %d %s" % (0, sorted(lex_score.items(), key=itemgetter(1), reverse=True)))
        trans_score = {}
        for n in range(len(tags) + 1, 0, -1):
            counts = counts_by_order.get(n)
            if not counts:
                continue
            trans_score = {t[-1]: c for t, c in counts.items() if t[:-1] == tuple(tags[len(tags) + 1 - n:])}
            print("  %d %s" % (n, sorted(trans_score.items(), key=itemgetter(1), reverse=True)))
            if trans_score:
                break
        if trans_score:
            scores = {x: lex_score[x] * trans_score[x] for x in set(lex_score) & set(trans_score)}
            print("    %s" % (sorted(scores.items(), key=itemgetter(1), reverse=True)))
        tags.append(max(scores, key=scores.get))
    return tags


def main(args):
    counts_by_order = load_counts(args.counts)
    for line in sys.stdin:
        tags = predict(tuple(line.strip().split()), counts_by_order)
        print("[l=%d] %s" % (len(tags), " ".join(tags)))


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("counts", nargs="+")
    main(argparser.parse_args())
