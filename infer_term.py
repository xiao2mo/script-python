#coding: utf8
"""
将char-level的训练数据，使用wordseg的边界进行term的推导，并作为新的一列feature添加进crf文件中。
比如,
<S> O O             <S> O O O
中 B B-LOC          中 B 中山路 B-LOC
山 M M-LOC   ===>   山 M 中山路 M-LOC
路 E E-LOC          路 E 中山路 E-LOC
<E> O O             <E> O O O
"""
from __future__ import print_function
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input char level crf file", default=None, type=str)
parser.add_argument("-o", "--output", help="output term level crf file", default=None, type=str)
parser.add_argument("-m", "--mode", help="input feature mode [3col|4col]", default="3col", type=str)
args = parser.parse_args()


def sen_iter(fname):
    with open(fname, "rb") as f:
        l = []
        for line in f:
            line = line.rstrip('\n')
            if not line:
                if len(l) < 1:
                    continue
                yield l
                l = []
                continue

            toks = line.split(' ')
            assert(len(toks) >= 3)
            l.append(toks)

        if len(l) > 0:
            yield l
            l = []

def conll_collapse(l):
    ls = ['|'.join(t) for t in l]
    return ' '.join(ls)

def extract_term(l):
    chars = [t[0] for t in l]
    segpos = [t[1] for t in l]
    labels = [t[-1] for t in l]
    terms = []
    i, start = 0, 0
    while i < len(chars):
        if i == 0:
            terms.append('O')
            i += 1
            continue
        elif i == len(chars) - 1:
            terms.append('O')
            i += 1
            continue

        pos = segpos[i]
        if pos in ['ALPHABET', 'DIGIT', 'S']:
            start = i
            term = ''.join(chars[start:i+1])
            for j in range(start, i+1):
                terms.append(term)
        elif pos in ['B']:
            start = i
        elif pos in ['E']:
            term = ''.join(chars[start:i+1])
            for j in range(start, i+1):
                terms.append(term)
        i += 1
    assert(len(terms) == len(chars))
    out_l = []

    for char, pos, label, term in zip(chars, segpos, labels, terms):
        s = '{} {} {} {}'.format(char, pos, term, label)
        out_l.append(s)
    return out_l

def extract_term_wt_keyword_fea(l):
    chars = [t[0] for t in l]
    segpos = [t[1] for t in l]
    keyword_feas = [t[2] for t in l]
    labels = [t[-1] for t in l]
    terms = []
    i, start = 0, 0
    while i < len(chars):
        if i == 0:
            terms.append('O')
            i += 1
            continue
        elif i == len(chars) - 1:
            terms.append('O')
            i += 1
            continue

        pos = segpos[i]
        if pos in ['ALPHABET', 'DIGIT', 'S']:
            start = i
            term = ''.join(chars[start:i + 1])
            for j in range(start, i + 1):
                terms.append(term)
        elif pos in ['B']:
            start = i
        elif pos in ['E']:
            term = ''.join(chars[start:i + 1])
            for j in range(start, i + 1):
                terms.append(term)
        i += 1
    assert (len(terms) == len(chars))
    out_l = []

    for char, pos, fea, label, term in zip(chars, segpos, keyword_feas, labels, terms):
        s = '{} {} {} {} {}'.format(char, pos, term, fea, label)
        out_l.append(s)
    return out_l

def main():
    fout = open(args.output, 'w')
    for l in sen_iter(args.input):
        if len(l) < 3:
            sys.stderr.write("conll sentence format error:{}".format(conll_collapse(l)))
            sys.exit(-1)
        if args.mode == '3col':
            out_l = extract_term(l)
        elif args.mode == '4col':
            out_l = extract_term_wt_keyword_fea(l)
        else:
            sys.stderr.write("mode invalid {}, valid mode include [3col,4col]".format(args.mode))
            sys.exit(-1)
        fout.write('\n'.join(out_l) + '\n\n')
    fout.close()

if __name__ == '__main__':
    main()
