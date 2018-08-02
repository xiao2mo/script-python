#!/usr/bin/env python
# coding=utf-8
import os
import sys
fout=open("zhidao.new","w")
for line in open(sys.argv[1]):
    if line=="\n":
        continue
    else:
        fout.write(line)
fout.close()

