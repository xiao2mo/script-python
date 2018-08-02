#!/usr/bin/python 
#!coding:utf-8
import re
line='adf dfd;dsfef;jfadiohfiusad,dfiejfdada'
result=re.split(r'[;,\s]',line)
print(result)
result2=re.sub(r'[;,\s]',' ',line)
print(result2)
