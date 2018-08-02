#!/bin/python
#!coding:utf-8
import glob
for name in glob.glob('globtest/*'): # only * ? [] available
	print(name)

