#!/usr/bin/python 
#!coding:utf-8
'''
Author:Melison@trio.ai
Date:2018年07月24日14:32:09
'''
import os
import sys
import re
fout=open(sys.argv[2],"w")
with open(sys.argv[1],"r") as fin:
    for line in fin:
        line=line.strip("\n")
        #termdict=[]
        p=re.finditer('《(.*?)》',line)
        if p is not None:
            line=line
            for item in p:
                termdict=[]
                newline=line.replace("《"+item.group(1)+"》","ENT")
                termdict.append(item.group(1))
                #print(newline)
            	out_str='{}\t{}\n'.format(newline," ".join(termdict))
            #if "ENT" in out_str:
            	fout.write(out_str)
        else:
            print("not find")
            continue
            #fout.write(line)
            #fout.write("\n")



