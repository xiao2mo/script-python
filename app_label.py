#coding: utf8
import sys
import re

def load_dict(fname):
    d = {}
    with open(fname, 'rb') as fin:
        for line in fin:
            line = line.rstrip('\n')
            toks = line.split('\t')
            term, tag = toks[0], toks[1]
            uterm = term.decode('utf8')
            d[uterm] = toks[1]
    sys.stderr.write('load dict {}\n'.format(len(d)))
    return d

d = load_dict('tmp/app.candi')

pt = re.compile(ur'【(.*?)】')
pt1 = re.compile(ur'\[(.*?)\]')

with open(sys.argv[1], 'r') as fin:
    for line in fin:
        line = line.rstrip('\n')
        s = line
        us = s.decode('utf8')
        hit = False
        m = pt.search(us)
        if m:
            beg, end = m.span()
            term = m.group(1)
            if d.has_key(term):
                tag = d[term]
                hit = True
                us = us[:beg] + '[NOR]' + m.group(0) + '[' + tag + ']' + us[end:]
        else:
            m = pt1.search(us)
            if m:
                beg, end = m.span()
                term = m.group(1)
                if d.has_key(term):
                    hit = True
                    tag = d[term]
                    us = us[:beg] + '[NOR]' + m.group(0) + '[' + tag + ']' + us[end:]

        if hit:
            s = us.encode('utf8')
            print(s)
    
