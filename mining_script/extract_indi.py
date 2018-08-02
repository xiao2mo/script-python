#!/usr/bin/python
#!coding:utf-8
import sys
import os
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')
jieba.load_userdict("t1.txt")  //加载需要的词表
termlist=set()
for item in open(sys.argv[1]):
    newitem=item.rstrip("\n")
    termlist.add(newitem)
for line in open(sys.argv[2]):
    newline = line.rstrip("\n")
    for item in termlist:
        #print("111")
        #print item
        keyword=item
        if item in newline:
            newlist=list(jieba.cut(newline))
            for (i,word) in enumerate(newlist):
                #print("222")
                if word=="" or word==" ":
                    continue
                #print word
                #print keyword
                #print word.decode('utf-8')
                #print keyword.decode('utf-8')
                if word.decode('raw_unicode_escape')==keyword.decode('raw_unicode_escape'):
                    if i>1 and i<len(newlist):
                        print newlist[i-1]
                        print newlist[i+1]
            
