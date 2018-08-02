#coding: utf8
import sys
import re

pt = re.compile(r'[BI]-(.*?)$')
d = {}
for line in sys.stdin:
    toks = line.rstrip('\n').split('\t')
    if len(toks) != 2:
        continue
    tags = toks[1]
    tags = tags.split(' ')
    for tag in tags:
        m = pt.search(tag)
        if m is None:
            continue
        d[m.group(1)] = d.get(m.group(1), 0) + 1

for k,cnt in d.items():
    print(k + ' ')
