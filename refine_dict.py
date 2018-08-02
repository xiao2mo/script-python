#coding: utf8

import argparse
import sys
import re
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="dict type", default="STATION", type=str)
parser.add_argument("-i", "--input", help="input multiple dict, split by \",\"", default=None, type=str)
parser.add_argument("-o", "--output", help="output single dict ", default=None, type=str)
args = parser.parse_args()

pt_1 = re.compile(ur"^.*?(地铁)|(火车)站$")
pt_2 = re.compile(ur"^.*?\(?(国内出发)|(港澳台到达)|(国际出发)|(国际到达)|(国内到达)|(候机楼)|(机场)|(出发厅)|(航站楼)\)?$")
pt_3 = re.compile(ur"^.*?机场(前)?站([a-zA-Z0-9]\+口)?$")
pt_4 = re.compile(ur"^.*?(机场)|(火车站).*?\(?(停车场)|(停车楼)|(.{0,6}门)|(出口)|(入口)\)?$")
pt_5 = re.compile(ur"^.*?(地铁)|(火车)站(.{1,4}口)?$")

def main():
    fout = open(args.output, 'w')
    with open(args.input, 'r') as fin:
        for line in fin:
            toks = line.rstrip('\n').rsplit('\t', 1)
            if len(toks) != 2:
                continue
            term, tag = toks
            uterm = term.decode('utf8')
            m = pt_1.match(uterm)
            if m is not None:
                out_s = '{}\tLOC.STATION'.format(term)
                fout.write(out_s + '\n')
                continue
            m = pt_2.match(term)
            if m is not None:
                out_s = '{}\tLOC.STATION'.format(term)
                fout.write(out_s + '\n')
                continue
            m = pt_3.match(term)
            if m is not None:
                out_s = '{}\tLOC.STATION'.format(term)
                fout.write(out_s + '\n')
                continue
            m = pt_4.match(term)
            if m is not None:
                out_s = '{}\tLOC.STATION'.format(term)
                fout.write(out_s + '\n')
                continue
            m = pt_5.match(term)
            if m is not None:
                out_s = '{}\tLOC.STATION'.format(term)
                fout.write(out_s + '\n')

if __name__ == '__main__':
    main()
