#coding: utf8
from __future__ import print_function
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

allkeys=set()
fin = open(sys.argv[1], 'r')
fout=open("train.json","w")
lines = fin.readlines()
s_line = ''.join(lines)

d = json.loads(s_line)  # str to dict
print(d.keys())
for key in d.keys():
  allkeys.add(key)

for key in allkeys:
  num=d[key]["train_no"]
  print(num)
  fromcity=d[key]["start_station"]
  tocity=d[key]["end_station"]
  starttime=d[key]["start_time"]
  endtime=d[key]["end_time"]

  milejsondict=[]
  allinfo=""
  #print(type(d[key]["stops_info"]))  #  it is a list
  try:
    if len(d[key]["stops_info"])>0:
      for idx,item in enumerate(d[key]["stops_info"]):
        mileinfo=json.dumps(item,ensure_ascii=False)   #dict to str for output
        if idx==0:
          allinfo="["+mileinfo
        elif idx==len(d[key]["stops_info"])-1:
          allinfo+=mileinfo+"]"
        else:
          allinfo+=","+mileinfo
    else:
      allinfo="[]"
  except Exception as e:
    allinfo="[]"
  #json2=json.dumps(json.loads(''.join(d[key]["stops_info"])),ensure_asci=False).decode("utf-8")
  out_str='{}\t{}\t{}\t{}\t{}\t{}\n'.format(num,fromcity,tocity,starttime,endtime,allinfo)
  fout.write(out_str)

