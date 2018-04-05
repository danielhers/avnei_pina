import sys
from argparse import ArgumentParser

import spacy
from tqdm import tqdm

from count_ngrams import NgramCounter


class TagNgramCounter(NgramCounter):
    def __init__(self, *args, lang=None, **kwargs):
        self.cache = {}
        self.nlp = None
        self.get_nlp(lang)
        super().__init__(*args, suffix="grams_tag", **kwargs)

    def get_nlp(self, model=None):
        while not self.nlp:
            print("Loading spaCy model '%s'... " % model, end="", flush=True)
            try:
                self.nlp = spacy.load(model)
            except OSError:
                spacy.cli.download(model)
        return self.nlp

    def gen_ngrams(self, filename, n):
        for doc in self.annotate(filename):
            doc = [t for t in doc if t.orth_.strip()]
            for i in range(len(doc) - max(n, 1) + 1):
                yield tuple(t.tag_ for t in doc[i:i + n]) if n else (doc[i].orth_, doc[i].tag_)

    def annotate(self, filename):
        annotated = self.cache.get(filename)
        if annotated is None:
            self.cache[filename] = annotated = list(tqdm(self.get_nlp().pipe(self.get_lines(filename)),
                                                         desc="Annotating " + filename, unit=" lines",
                                                         file=sys.stdout))
        return annotated


def main(args):
    TagNgramCounter(args.ngram_order, args.text, args.out_dir, lang=args.lang)


if __name__ == "__main__":
    argparser = ArgumentParser()
    NgramCounter.add_args(argparser)
    argparser.add_argument("-l", "--lang", default="en")
    main(argparser.parse_args())
