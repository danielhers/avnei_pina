import sys
import nltk
from collections import Counter

if len(sys.argv) < 4:
    print "Usage: %s n text output" % sys.argv[0]
    sys.exit(0)

n = int(sys.argv[1])
c = Counter()

f = sys.argv[2]
print "Reading '%s'..." % f
with open(f) as fh:
    for line in fh:
        pad = ["<s>"]   # (n - 1) *
        tokens = pad + nltk.word_tokenize(line.lower()) + pad
        for i in range(len(line) + n - 1):
            ngram = tuple(tokens[i:i+n])
            c[ngram] += 1

f = sys.argv[3]
print "Writing %d-grams to '%s'..." % (n, f)
with open(f, "w") as fh:
    for ngram, count in c.items():
        fh.write("%s\t%d\n" % (" ".join(ngram), count))
