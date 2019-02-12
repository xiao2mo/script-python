#!/usr/bin/python
#!coding:utf-8
'''
Ahthour:caoshengming@trio.ai
Func: test of Map function
Date: 2018年08月17日15:23:44
'''
import sys
import os
def maptest(x):
    return x*x
print(map(maptest,[1,2,3,4,5]))

def format_name(s):
    s1=s[0:1].upper()+s[1:].lower()
    return s1
print(map(format_name,['amid','aMilong','aMy','meLision']))

l2=map(lambda x,y:x**y,[1,2,3],[1,2,3])
print(l2)

l3=map(lambda x,y:(x**y,x+y),[1,2,3],[1,2,3])
print(l3)


s='1234'
print("type of %s is %s"%(s,type(s)))

l=map(int,'1234')
print("type of %s is %s"%(l,type(l)))
print(l)


#zip 函数的另一种替代方法
l1=[1,2,4]
l2=[5,6,7]
x=map(None,l1,l2)
print(x)

