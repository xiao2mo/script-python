#coding: utf8
"""
Analyze and make statistics of term distribution in ner.
"""
from __future__ import print_function
import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input raw crf_data", default=None, type=str)
parser.add_argument("-ne", "--ners", help="target ners, concate with \",\"", default="LOC.TAG", type=str)
args = parser.parse_args()

def build_pt_list():
    ners = args.ners.split(',')
    pt_l = []
    for ner in ners:
        pt_tpl = r'\[NOR\]([^\[\]]+)\[({})\]'.format(ner)
        pt = re.compile(pt_tpl)
        pt_l.append(pt)
    return pt_l

def extract_ne(s, pt_l):
    out_l = []
    for pt in pt_l:
        m = pt.search(s)
        if m is not None:
            k = m.group(1)
            v = m.group(2)
            out_l.append((k,v))
    return out_l

def main():
    pt_l = build_pt_list()
    d = {}
    with open(args.input, "r") as fin:
        for line in fin:
            line = line.rstrip('\n')
            l = extract_ne(line, pt_l)
            for term, ner in l:
                print("{}\t{}".format(ner, term))

if __name__ == '__main__':
    main()