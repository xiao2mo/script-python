#!coding:utf-8
import sys
import os
alldict={}
fout=open("term_dict.stat","w")
for line in open(sys.argv[1]):
    item=line.rstrip("\n")
    #print(item)
    if item not in alldict:
        alldict[item]=1
    else:
        alldict[item]+=1

newdict=sorted(alldict.items(), key=lambda x:x[1])
for item in newdict:
    out_str="{}\t{}\n".format(item[0],item[1])
    fout.write(out_str)
