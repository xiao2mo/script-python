import sys
import os
alldict={}
count = 0
fout=open(sys.argv[2],"w")
for line in open(sys.argv[1]):
	item = line.rstrip("\n")
	if item not in alldict.keys():
		alldict[item] = 1
	else:
		alldict[item]+=1
	count+=1
'''
print sorted(alldict.items(), key=lambda alldict: alldict[1])

keys=alldict.keys()
keys.sort()
for key in sorted(alldict.keys()):
	item = key
	pr = alldict[item]*1.0/count
	out_str = "{}\t{}\n".format(item,pr)
	fout.write(out_str)
'''
alldict2 = sorted(alldict.items(), key=lambda alldict: alldict[1],reverse=True)
for key in alldict2:
	item = key[0]
	pr = alldict[item]*1.0/count
	out_str = "{}\t{}\n".format(item,pr)
	fout.write(out_str)
