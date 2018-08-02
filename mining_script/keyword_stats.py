#coding: utf8
import sys
import jieba
d = {}
for line in sys.stdin:
    line = line.strip()
    if len(line) < 1:
        continue
    toks = jieba.cut(line)
    for tok in toks:
        d[tok] = d.get(tok, 0) + 1

sorted_l = sorted(d.items(), key=lambda x:x[1], reverse=True)
for uk,cnt in sorted_l:
    k = uk.encode('utf8')
    print '{}\t{}'.format(k,cnt)
