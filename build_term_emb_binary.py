#coding: utf8
"""
将ascii的word2vec 数据，转化为numpy格式的二进制数据.

示例：
python script/build_term_emb_binary.py -i vocab/term.emb -o ${DEST_DIR}/term.emb.np
"""
import numpy as np
import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input multiple dict, split by \",\"", default=None, type=str)
parser.add_argument("-o", "--output", help="output single dict ", default=None, type=str)
args = parser.parse_args()

_PAD = "_PAD"
_UNK = "_UNK"
_START_VOCAB = [_PAD, _UNK]

def dump_emb(fname, np_fname, start_vocab=_START_VOCAB):
    l = []
    for _ in start_vocab:
        rnd_arr = np.random.random((1, 128)).tolist()
        rnd_arr = rnd_arr[0]
        l.append(rnd_arr)
    with open(fname, 'r') as fin:
        for line in fin:
            emb = line.rstrip('\n').split()
            emb = [float(i) for i in emb]
            l.append(emb)
    m = np.array(l)
    print(m.shape)
    m.dump(np_fname)

def word2vec_2_np(word2vec_ascii_fname, vocab_fname, emb_fname, start_vocab=_START_VOCAB):
    pass

def main():
    dump_emb(args.input, args.output)

if __name__ == '__main__':
    main()
