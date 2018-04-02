from argparse import ArgumentParser
from collections import Counter

import os
import csv
import sys
from tqdm import tqdm
from glob import glob


def gen_ngrams(filename, n):
    with open(filename, encoding="utf-8") as f:
        for line in filter(None, tqdm(f, desc="Reading " + filename, unit=" lines", file=sys.stdout)):
            tokens = line.strip().replace("“", "").replace("”", "").replace(" ", "").replace("，", "") \
                if "zh" in filename else \
                line.lower().replace('"', "").replace("'", "").replace(",", "").replace("-", "").strip().split()
            for i in range(len(tokens) - n + 1):
                yield tuple(tokens[i:i + n])


def write_counts(counts, filename):
    with open(filename, "w", encoding="utf-8") as f:
        csv.writer(f).writerows(tqdm(((" ".join(k), v) for k, v in counts.most_common()),
                                     desc="Writing " + filename, unit=" lines", file=sys.stdout))


def count(text, order, out_dir):
    counts = Counter(gen_ngrams(text, n=order))
    os.makedirs(out_dir, exist_ok=True)
    basename, _ = os.path.splitext(os.path.basename(text))
    write_counts(counts, os.path.join(out_dir, basename + ".%dgrams.csv" % order))


def main(args):
    for n in args.ngram_order:
        for pattern in args.text:
            for filename in glob(pattern) or pattern:
                count(filename, n, args.out_dir)


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("text", nargs="+")
    argparser.add_argument("-o", "--out-dir", default="counts")
    argparser.add_argument("-n", "--ngram-order", nargs="+", type=int, default=(2,))
    main(argparser.parse_args())
