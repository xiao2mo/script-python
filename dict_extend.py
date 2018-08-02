#coding: utf8
"""
词典扩充工具。
1. 对于XXXX(附属信息）这样的词典，增加一列XXXX, 从而扩大词典的召回范围.
"""
import sys
import re

pt1 = re.compile(ur'\(.*?\)')
pt2 = re.compile(ur'（.*?）')

def rule_1(s):
    us = s.decode('utf8')
    m = pt1.search(us)
    out_l = []
    if m is not None:
        beg, end = m.span()
        us1 = us[:beg]
        if len(us1) > 2:
            s_extend = us1.encode('utf8')
            out_l.append(s_extend)
        us2 = us[end:]
        if len(us2) > 2:
            s_extend = us2.encode('utf8')
            out_l.append(s_extend)
    m = pt2.search(us)
    if m is not None:
        beg, end = m.span()
        us1 = us[:beg]
        if len(us1) > 2:
            s_extend = us1.encode('utf8')
            out_l.append(s_extend)
        us2 = us[end:]
        if len(us2) > 2:
            s_extend = us2.encode('utf8')
            out_l.append(s_extend)

    return out_l

def main():
    with open(sys.argv[1], 'r') as fin:
        for line in fin:
            line = line.rstrip('\n')
            print(line)
            toks = line.split('\t')
            if len(toks) < 2:
                continue
            term, tag = toks[:2]
            l = rule_1(term)
            if len(l) > 0:
                for t in l:
                    print('{}\t{}'.format(t, tag))


if __name__ == '__main__':
    main()
