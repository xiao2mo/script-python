#coding: utf8
import sys
d = {}
for line in sys.stdin:
    line = line.rstrip('\n')
    toks = line.split(' ')
    if len(toks) < 2:
        continue
    for tok0, tok1 in zip(toks, toks[1:]):
        bigram = '{}_{}'.format(tok0, tok1)
        d[bigram] = d.get(bigram, 0) + 1

sorted_l = sorted(d.items(), key=lambda x:x[1], reverse=True)
sorted_l = [t for t in sorted_l if t[1] >= 10]
for term, cnt in sorted_l:
    print('{}\t{}'.format(term, cnt))
