#coding: utf8
import numpy as np
import argparse
import sys
import re
import random
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input labeled data", default=None, type=str)
parser.add_argument("-o", "--output", help="output labeled data prefix", default=None, type=str)
parser.add_argument("-ts", "--test_size", help="test set size", default=10000, type=int)
parser.add_argument("-vs", "--valid_size", help="validation set size", default=20000, type=int)
args = parser.parse_args()

pt = re.compile(r'\[NOR\](.*?)\[((LOC)|(ORG)|(ENT)|(PROD)|(APP)|(NUM)|(TIME)).*?\]')
target_ner_set = set(['LOC', 'ORG', 'ENT', 'PROD', 'APP', 'NUM'])

d_sentence = {}
d_ner = {}
d_term = {}

def sentence_iter(fname):
    with open(fname, 'r') as fin:
        for line in fin:
            line = line.rstrip('\n')
            raw_sentence = pt.sub(r'\1', line)
            d_sentence[raw_sentence] = d_sentence.get(raw_sentence, 0) + 1
            l_term = []
            for m in pt.finditer(line):
                term = m.group(1)
                # l_term.append(term)
            yield line, raw_sentence

def dumpList2File(l, fname):
    with open(fname, 'w') as fout:
        fout.write('\n'.join(l))
    return

def main():
    l = []
    for label_sentence, raw_sentence in sentence_iter(args.input):
        l.append((label_sentence, raw_sentence))
    random.shuffle(l)
    visited = set()
    l_test = []
    for i, (label_sentence, raw_sentence) in enumerate(l):
        if len(l_test) > args.test_size:
            break
        if raw_sentence in visited:
            continue
        l_test.append(label_sentence)
        visited.add(raw_sentence)
        del l[i]

    l_valid = [t[0] for t in l[-args.valid_size-1:]]
    l_train = [t[0] for t in l[:-args.valid_size]]

    train_fname = args.output + ".train.raw"
    valid_fname = args.output + ".valid.raw"
    test_fname = args.output + ".test.raw"

    dumpList2File(l_train, train_fname)
    dumpList2File(l_valid, valid_fname)
    dumpList2File(l_test, test_fname)

if __name__ == '__main__':
    main()
