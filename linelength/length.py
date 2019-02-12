import os
import sys
with open(sys.argv[1]) as fin:
	lines = fin.readlines()
	lines.sort(key=lambda x:len(x))
	for line in lines:
		print line.rstrip("\n")
