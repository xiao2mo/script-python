# -*-coding=utf-8 -*-
'''
Created on 2014/10/09

@author: fanyange
'''
import json
import sys
import os
import re




def load_dict(standard_path):
    fp=open(standard_path,"r")

    num_dict=dict()
    line_dict=dict()
    contain_items_dict=dict()
    contain_raw_dict=dict()
    index=0
    groundTrue_all_category_dict=dict()
    while 1:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue
        new_str=re.sub("\[NOR\]","",line)

        new_str3 = re.sub("\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM)\.([A-Z]|\.|_)*\]", "", new_str)


        contain_raw_dict[new_str3.decode("utf-8")] = line.decode("utf-8")

        # print line
        contain_items=[]
        items1 = re.findall("((\[NOR\]+)[^\[]+(\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM){1}\.{1}\w+\]+))", line)
        for j in items1:

            contain_items.append(j[0]+str(line.find(j[0])))


        contain_items_dict[new_str3]=contain_items

        items=re.findall("(\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM){1}\.{1}\w+\]+)",line)
        allitems=[]
        for i in items:
            allitems.append(i[0])
            if groundTrue_all_category_dict.has_key(i[0]):
                groundTrue_all_category_dict[i[0]]+=1
            else:
                groundTrue_all_category_dict[i[0]]=1
    # print line
    # print contain_items
    # print ("******")

    fp.close()

    return contain_items_dict,groundTrue_all_category_dict,contain_raw_dict











def treate_file(standard_path,tag_path):

    true_contain_items_dict,groundTrue_all_category_dict,contain_raw_dict=load_dict(standard_path)

    fp=open(tag_path,"r")
    ferr=open('./error_log.txt','w+')


    all_NER_count=0
    all_wrong_NER_count=0
    all_right_NER_count=0
    wrong_line=0
    all_line=0
    while 1:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue
        all_line+=1

        new_str=re.sub("\[NOR\]","",line)
        new_str3=re.sub("\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM)\.([A-Z]|\.|_)*\]","",new_str)


        if not contain_raw_dict.has_key(new_str3.decode("utf-8")):
            print ("该条数据格式有Bug： %s"%line)
            continue

        if contain_raw_dict[new_str3.decode("utf-8")]!=line.decode("utf-8"):
            s1=contain_raw_dict[new_str3.decode("utf-8")]


            ferr.write("trio: "+s1.encode('utf-8')+'\n')
            ferr.write("----------\n")
            wrong_line+=1
            ferr.write("mada: "+line+'\n\n')
            ferr.write("\n\n\n")

        tag_contain_items = []
        items1 = re.findall("((\[NOR\]+)[^\[]+(\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM){1}\.{1}\w+\]+))", line)
        for j in items1:
            tag_contain_items.append(j[0]+str(line.find(j[0])))

        if not true_contain_items_dict.has_key(new_str3):
            print ("该源句子不在目标文件中  %s" %(line))
            continue

        true_contain_items=true_contain_items_dict[new_str3]


        max_count=max(len(tag_contain_items),len(true_contain_items))


        for i in tag_contain_items:
            if i in true_contain_items:
                all_right_NER_count+=1
            all_wrong_NER_count+=1


        all_NER_count=all_NER_count+max_count


    print ("总数据条数: %d"% all_line)
    print ("错误的数据条数: %d"% wrong_line)
    print ("正确的数据条数：%d"%(all_line-wrong_line))
    print ("正确条数／总数据条数的准确度：%0.3f%%"%(float(all_line-wrong_line)/float(all_line)*100))
    all_accuracy=float(all_right_NER_count)/float(all_NER_count)*100

    print ('\n')
    print ('正确的NER个数：%d'%(all_right_NER_count))
    print ("总的NER个数：%d"%(all_NER_count))
    print ("正确的NER个数／总的NER个数：all_accuracy= %0.3f%% "%(all_accuracy))
    print("\n")
    print ("******************")
    print ("groundTrue_all_category_dict:\n")
    print (groundTrue_all_category_dict)

    fp.close()
    ferr.close()

    print "success"
        


if __name__=="__main__":
    groundTruePath="./trio.txt"
    othersTagPath="./mada.txt"
    # treate_file(sys.argv[1],sys.argv[2])
    treate_file(groundTruePath,othersTagPath)



