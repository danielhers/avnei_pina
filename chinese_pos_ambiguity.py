#!/usr/bin/python
# -*- coding: utf-8 -*-

import codecs
from collections import defaultdict, Counter

words = []
trans = Counter()
with codecs.open("CoNLL2009-ST-Chinese-trial.words-pos.txt", "r", "utf-8") as f:
    for line in f:
        prev = "<s>"
        for pair in line.split():
            word, pos = pair.split("/")
            words.append((word, pos))
            trans[(prev, pos)] += 1
            prev = pos

counts = defaultdict(Counter)
for word, pos in words:
    counts[word][pos] += 1

with codecs.open("chinese-statistics.txt", "w", "utf-8") as f:
    for word, c in sorted(counts.iteritems(), key=lambda(word, c): sum(c.values())):
        #if len(c) > 1:
            f.write("%-20s %s\n" % (", ".join(["%s: %d" % (x, y) for x, y in c.iteritems()]), word))
            
my_pos = ["<s>", "NN", "NR", "VV", "DT", "LC", "JJ", "PU"]
print "   " + " ".join(my_pos)
for pos1 in my_pos:
    print pos1, 
    for pos2 in my_pos:
        print trans[(pos1, pos2)],
    print
