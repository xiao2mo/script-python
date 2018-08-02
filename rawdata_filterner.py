#coding: utf8
"""
对[NOR].*[NER1.NER2]的raw data进行处理，对选中的NER type，从标注预料中去除。
"""
import sys
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input char level crf file", default=None, type=str)
parser.add_argument("-o", "--output", help="output term level crf file", default=None, type=str)
parser.add_argument("-n", "--ners", help="nertype2, seperated by comma", default="LOC_TAG", type=str)
args = parser.parse_args()

def main():
    if args.input is None or args.output is None:
        sys.stderr.write("Usage: exe -i input_file -o output_file -n 'nertypes'\n")
        sys.exit(-1)
    ners = args.ners.split(',')
    pt_list = []
    # for ner in args.ners.split(','):
    #     s_pt = r'\[NOR\]([^[]+)\[{}\]'.format(ner)
    #     pt = re.compile(s_pt)
    #     pt_list.append(pt)
    pt = re.compile(r'\[NOR\]([^[]+)\[LOC.CATER\]')
    pt_list.append(pt)
    fout = open(args.output, 'w')
    with open(args.input, 'r') as fin:
        for line in fin:
            line = line.rstrip('\n')
            for pt in pt_list:
                line = pt.sub(r'\1', line)
            fout.write(line + '\n')
    fout.close()

if __name__ == '__main__':
    main()
