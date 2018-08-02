#coding: utf8
from __future__ import print_function
import sys

def sen_iter(fname):
    l = []
    with open(fname, 'r') as fin:
        for line in fin:
            line = line.rstrip('\n')
            if line:
                l.append(line)
            else:
                if len(l) > 0:
                    yield l
                l = []
    if len(l) > 0:
        yield l

def file2sentences(fname):
    sentences = []
    for l in sen_iter(fname):
        l = [s.rsplit(' ', 3) for s in l]
        l = [(i[0], i[-1]) for i in l]
        sentences.append(l)
    return sentences

def main():
    fdebug = open('debug.log', 'w')
    sens_1 = file2sentences(sys.argv[1])
    sens_2 = file2sentences(sys.argv[2])
    for sen_1, sen_2 in zip(sens_1, sens_2):
        if len(sen_1) != len(sen_2):
            continue
        out_l = [[s1[0], s1[1], s2[1]] for s1, s2 in zip(sen_1, sen_2)]
        out_l = [' '.join(l) for l in out_l]
        print('\n'.join(out_l))
        print()
    fdebug.close()

if __name__ == '__main__':
    main()
