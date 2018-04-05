import string
from argparse import ArgumentParser
from collections import Counter

import os
import csv
import sys
from tqdm import tqdm
from glob import glob


class NgramCounter:
    def __init__(self, orders, patterns, out_dir, suffix="grams"):
        self.suffix = suffix
        for n in orders:
            for pattern in patterns:
                for filename in glob(pattern) or pattern:
                    self.count(filename, n, out_dir)

    def get_lines(self, filename):
        with open(filename, encoding="utf-8") as f:
            for line in filter(None, tqdm(f, desc="Reading " + filename, unit=" lines", file=sys.stdout)):
                line = line.lower().strip().translate(str.maketrans({key: None for key in string.punctuation}))
                yield line.replace("“", "").replace("”", "").replace(" ", "").replace("，", "") \
                    if "zh" in filename else line

    def gen_ngrams(self, filename, n):
        for line in self.get_lines(filename):
            tokens = line.split()
            for i in range(len(tokens) - n + 1):
                yield tuple(tokens[i:i + n])

    def save_counts(self, counts, filename):
        with open(filename, "w", encoding="utf-8") as f:
            csv.writer(f).writerows(tqdm(((" ".join(k), v) for k, v in counts.most_common()),
                                         desc="Writing " + filename, unit=" lines", file=sys.stdout))

    def count(self, text, order, out_dir):
        counts = Counter(self.gen_ngrams(text, n=order))
        os.makedirs(out_dir, exist_ok=True)
        basename, _ = os.path.splitext(os.path.basename(text))
        self.save_counts(counts, os.path.join(out_dir, basename + ".%d%s.csv" % (order, self.suffix)))

    @staticmethod
    def add_args(p):
        p.add_argument("text", nargs="+")
        p.add_argument("-o", "--out-dir", default="counts")
        p.add_argument("-n", "--ngram-order", nargs="+", type=int, default=(2,))


def main(args):
    NgramCounter(args.ngram_order, args.text, args.out_dir)


if __name__ == "__main__":
    argparser = ArgumentParser()
    NgramCounter.add_args(argparser)
    main(argparser.parse_args())
