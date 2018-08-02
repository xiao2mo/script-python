#coding: utf8
"""
用于处理词表中经常包含的附属信息，
比如，将 "时间简史:第二版" 处理为
"时间简史"
"时间简史:第二版"
"""
from __future__ import print_function
import sys
import re
import numpy as np
pt = re.compile(r'(：)|(\()|(:)|(（)|(【)')

def split_candi(s):
    out_l = [s, ]
    pos1 = s.find(':')
    pos2 = s.find('：')
    pos3 = s.find('（')
    pos4 = s.find('(')
    pos5 = s.find('【')
    pos6 = s.find('[')

    l_pos = [pos1, pos2, pos3, pos4, pos5, pos6]
    l_pos = [pos for pos in l_pos if pos >= 0]
    if len(l_pos) > 0:
        pos = np.min(l_pos)
        s1 = s[:pos]
        out_l.append(s1)
    return out_l

for line in sys.stdin:
    line = line.rstrip('\n')
    toks = line.split('\t')
    assert(len(toks) == 2)
    term, tag = toks
    l = split_candi(term)

    out_l = ['{}\t{}'.format(i, tag) for i in l]
    print('\n'.join(out_l))
