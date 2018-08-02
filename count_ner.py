#-*-coding:utf-8-*-
import sys
import re

def count_ner(data_path):

    f=open(data_path,"r")
    category_dict=dict()
    all_ner_num=0
    while 1:
        line = f.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue
        items=re.findall("(\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM){1}\.{1}\w+\]+)",line)

        for i in items:
            all_ner_num+=1
            if category_dict.has_key(i[0]):
                category_dict[i[0]]+=1
            else:
                category_dict[i[0]]=1

    print (category_dict)
    print ("Ner总数目： %d 个\n"%all_ner_num)
    for k,v in category_dict.iteritems():
        print ("%s：%d 个 , 占Ner总数目的%0.3f%%"%(k,v,100*float(v)/float(all_ner_num)))

    f.close()




if __name__=="__main__":
    #dataPath="./trio.txt"
    count_ner(sys.argv[1])
