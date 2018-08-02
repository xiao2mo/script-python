#!/usr/bin/env python
# coding=utf-8
import os
import sys
film1=set()
fout=open(sys.argv[3],"w")
for line in sys.argv[1]:
    item=line.rstrip("\n")
    film1.add(item)

for line in sys.argv[2]:
    item =line.rstrip("\n")
    print item
    for film in film1:
        print film
        if item == film:
           continue
        fout.write(item)
        fout.write("\n")

