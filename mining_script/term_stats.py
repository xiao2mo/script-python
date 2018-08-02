#coding: utf8
import sys
d = {}
for line in sys.stdin:
    line = line.rstrip('\n')
    toks = line.split(' ')
    for tok in toks:
        d[tok] = d.get(tok, 0) + 1

sorted_l = sorted(d.items(), key=lambda x:x[1], reverse=True)
for term, cnt in sorted_l:
    print('{}\t{}'.format(term, cnt))
