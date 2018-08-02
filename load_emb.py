#coding: utf8
import numpy as np
import sys

def load_emb_np(fname):
    m = np.load(filename)
    print("Load embedding of size: {} x {}".format(m.shape[0], m.shape[1]))
    return m.tolist()

if __name__ == '__main__':
    load_emb_np(sys.argv[1])
