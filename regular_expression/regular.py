#!/usr/bin/python 
#!coding:utf-8
import re
line='adf dfd;dsfef;jfadiohfiusad,dfiejfdada'
result=re.split(r'[;,\s]',line)
print("result",result)
result2=re.sub(r'[;,\s]',' ',line)
print("result2",result2)

newline="AC analytices ACummulations"
result3=re.match(r'AC',newline)
print("result3",result3.group())

result6=re.search(r'AC',newline)
print("result6",result6.group())

result4=re.findall(r'AC',newline)
print("result4",result4)

result5=re.finditer(r'AC',newline)
for item in result5:
	print("result5.item",item.group())


newline2="'故宫'和'长城'是来北京的人都会去的地方"
p3=re.compile(r"'(.*?)'")
result7=p3.finditer(newline2)
for item in result7:
	#print ("result7.item %s"%(item.group().encode("utf-8")))
	print(item.group(0))
	print(item.group(1))
