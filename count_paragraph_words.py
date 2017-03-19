import sys

if len(sys.argv) < 2:
    print "Usage: %s filename" % sys.argv[0]
    sys.exit(0)

f = sys.argv[1]
with open(f) as fh:
    paragraphs = fh.read().split("\n\n")

features = []
for i, paragraph in enumerate(paragraphs):
    text = paragraph.strip()
    tokens = text.split()
    if not tokens: continue
    ntokens = len(tokens)
    ntypes = len(set(tokens))
    ratio = round(float(ntypes)/ntokens, 3)
    features.append((ratio, ntokens, ntypes, i, text[:20] + "..."))

print "ratio\ttokens\ttypes\tindex\ttext"
for t in sorted(features):
    print "\t".join([str(f) for f in t])
