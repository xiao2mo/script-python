#!/usr/bin/env python
# coding=utf-8
'''
Author:csm
Func:embdding char segment
'''
import os
import sys
fout=open("test.new","w")
for line in open(sys.argv[1]):
    for char in line.decode("utf-8"):
        fout.write(char.encode("utf-8"))
        if char!="\n":
            fout.write(" ")
fout.close()

