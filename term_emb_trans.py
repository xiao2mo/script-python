#!/usr/bin/python
#!coding:utf-8
import os
import sys
import numpy as np
m=np.load(sys.argv[1])
print("Load embedding of size: {} x {}".format(m.shape[0], m.shape[1]))
embeddings = []
for line in m:
    #ori = line.tolist().rstrip("\n")
    ori = line
    embeddings.append(ori)
#embeddings.append(m.tolist())
for line in open(sys.argv[2]):
    newterm = line.rstrip("\n")
    rnd_arr = np.random.random((1,128)).tolist()
    embeddings.append(rnd_arr[0])
newemb = np.array(embeddings)
newemb.dump("term.emb.np.new")
print("new embedding of size: {} x {}".format(len(embeddings), len(embeddings[0])))
