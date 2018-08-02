#!/usr/bin/env python
# coding=utf-8
import os
import sys
itemdict=set()
fout=open("result.txt","w")
for item in open(sys.argv[1]):
    term,_=item.split(",",1)
    itemdict.add(term)

for item in open(sys.argv[2]):
    term,_=item.split(",",1)
    if term in itemdict:
        continue
    else:
        fout.write(item)
