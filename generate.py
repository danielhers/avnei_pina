import sys
import nltk
import random
from collections import Counter

if len(sys.argv) < 2:
    print "Usage: %s counts ..." % sys.argv[0]
    sys.exit(0)

counts = {}
for f in sys.argv[1:]:
    c = Counter()
    print "Reading '%s'..." % f
    with open(f) as fh:
        for line in fh:
            text, count = line.split("\t")
            ngram = tuple(text.split())
            n = len(ngram)
            c[ngram] = count
    counts[n] = c

ns = sorted(counts.keys(), reverse=True)
tokens = []

while True:
    try:
        line = raw_input("Enter beginning of sentence:\n> ")
    except EOFError:
        break
    tokens = nltk.word_tokenize(line.lower()) or tokens
    if ns[0] > 1:
        pad = ["<s>"]   # (ns[0] - 2) *
        tokens = pad + tokens
    for n in ns:
        c = counts[n]
        if n == 1:
            ngrams = c
        else:
            suffix = tuple(tokens[-n+1:])
            ngrams = {ngram: count for ngram, count in c.items()
                      if ngram[:-1] == suffix}
        if ngrams:
            break   # no need to back-off to smaller ns
    if not ngrams:
        continue    # nothing found for any n
    # ngram = max(ngrams, key=c.get)
    max_count = max(ngrams.values())
    ngram = random.choice([t for t, count in ngrams.items()
                           if count == max_count])
    tokens.append(ngram[-1])
    print " ".join([token for token in tokens if token != "<s>"])
