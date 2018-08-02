#coding: utf8
'''
training crf格式 -> 单行格式，
mode=raw, ner使用原字符串，不加wrap
mode=ner, ner使用[NOR][NER]的方式进行wrap
'''
from __future__ import print_function
#from config import args
import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="mode [raw|ner]", default="ner", type=str)
parser.add_argument("-i", "--input", help="input crf file path", default=None, type=str)
parser.add_argument("-o", "--output", help="output single dict ", default=None, type=str)
args = parser.parse_args()


def collapse_crf(l, numCol=4):
    l = [s.rsplit(' ', numCol - 1) for s in l]
    l = l[1:-1]
    ws, gs = [t[0] for t in l], [t[-1] for t in l]
    c_gs = collapse_sen(ws, gs)
    return c_gs

def extract_entities(ws, tags):
    ne = []
    tmp_l = []
    start = -1
    prv_tag_type = None
    prv_alphabet = False
    cur_alphabet = False
    for i, (w, tag) in enumerate(zip(ws, tags)):
        if i == 0:
            prv_alphabet = False
        if w.isalnum():
            cur_alphabet = True
        if tag == 'O':
            tag_type = 'O'
            if len(tmp_l) > 0:
                t = (''.join(tmp_l), prv_tag_type, start, len(tmp_l))
                ne.append(t)
                tmp_l = []
                prv_tag_type = tag_type
            else:
                pass
        else:
            tag_type = tag[2:]

        if prv_tag_type is None:
            prv_tag_type = tag_type

        if tag.startswith('B-') or ((tag.startswith('M-') or tag.startswith('E-')) and prv_tag_type != tag_type):
            if len(tmp_l) > 0:
                t = (''.join(tmp_l), prv_tag_type, start, len(tmp_l))
                ne.append(t)
                tmp_l = []
                prv_tag_type = tag_type
            start = i
            if prv_alphabet and cur_alphabet:
                tmp_l.append(' ')
            tmp_l.append(w)
            prv_tag_type = tag_type
        elif tag != 'O':
            if prv_alphabet and cur_alphabet:
                tmp_l.append(' ')
            tmp_l.append(w)

        prv_alphabet = cur_alphabet
    if len(tmp_l) > 0:
        t = (''.join(tmp_l), prv_tag_type, start, len(tmp_l))
        ne.append(t)
    return ne

def collapse_sen(ws, tags):
    nes = extract_entities(ws, tags)

    out_l = []
    id = 0
    prv_alphabet = False
    cur_alphabet = False
    while id < len(ws):
        if id == 0:
            prv_alphabet = False
        found = False
        word = ws[id]
        cur_alphabet = word.isalnum()

        for term, ne, start, n in nes:
            if id == start:
                s = '[NOR]{}[{}]'.format(term, ne)
                out_l.append(s)
                id += n
                found = True
                prv_alphabet = False
                break
        if not found:
            if prv_alphabet and cur_alphabet:
                out_l.append(' ')
            out_l.append(ws[id])
            id += 1
            prv_alphabet = cur_alphabet
    return ''.join(out_l)

def data_iter():
    with open(args.input, 'r') as fin:
        l = []
        for line in fin:
            line = line.rstrip('\n')
            if len(line) < 1:
                if len(l) > 0:
                    yield l
                l = []
            else:
                l.append(line)
        if len(l) > 0:
            yield l
def main():
    fout = open(args.output, 'w')
    for l in data_iter():
        sent = collapse_crf(l, numCol=4)
        #print(sent)
        fout.write(sent + '\n')
    fout.close()

if __name__ == '__main__':
    main()
