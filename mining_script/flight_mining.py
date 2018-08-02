#coding: utf8
import sys
import re

#pt = re.compile(r'(?![a-zA-Z]+)[a-zA-Z]{2}[0-9]{4}(?![a-zA-Z0-9]+)')
pt = re.compile(r'[a-zA-Z]{2}[0-9]{4}(?![a-zA-Z0-9]+)')

for line in sys.stdin:
    line = line.rstrip('\n')
    toks = line.split('\t')
    if len(toks) < 4:
        continue
    title, t_content, reply = toks[1],toks[2],toks[3]

    m = pt.search(title)
    if m is not None:
        print title

    m = pt.search(t_content)
    if m is not None:
        print t_content

