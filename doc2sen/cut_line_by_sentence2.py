#!/usr/bin/env python
# coding=utf-8 
'''
Created on 2014/10/09

@author: fanyange
'''
import json
import sys
import os
import re

class item:
    term_num=0
    doc_num=0
    def __init__(self,tnum,dnum):
        self.term_num=tnum
        self.doc_num=dnum


def load_ok_words(path):
    fp=open(path,"r")

    word_dict=dict()
    while 1:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue
        terms = line.split("\t")
        if len(terms)!=3:
            continue
        word_dict[terms[0]]=terms[1]+"\t"+terms[2]
    return word_dict


def load_dict(dict_path):
    fp=open(dict_path,"r")

    num_dict=dict()
    index=0
    while 1:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue
        terms = line.split("\t")
        if len(terms) < 3:
            continue

        num_dict[terms[1]]=1
        #index=index+1
    fp.close()
    return num_dict
def change_encode(str,fromencode,toencode):
    try:
        u=str.decode(fromencode)
        s=u.encode(toencode)
        return (True,s)
    except:
        return (False,str)

def get_files(path):
	lst=[]
	for dirpath,dirnames,filenames in os.walk(path):
		for file in filenames:
			fullpath=os.path.join(dirpath,file)
			lst.append(file)
			#print fullpath
	return lst


def get_catalogs(file_lst,cat_dir):
	cat_dict=dict()
	for i in range(len(file_lst)):
		names=file_lst[i].split(".")
		if len(names) != 2:
			continue
		cat_path=cat_dir+"/"+file_lst[i]

		fp=open(cat_path)
		while 1:
			line = fp.readline()
			if not line:
				break
			line = line.strip()
			if line == "":
				continue
			items=line.split("\t")
			if len(items)<2:
				print line
				continue
			cat_dict[items[0]]=items[1].decode("gbk").encode("utf-8")
		fp.close()
	return cat_dict


def is_filter(str2):
    flag=False

    if len(str2)<=3:
        return True

    all_flag=True

    for i in range(len(str2)):
        if str2[i]>='0' and str2[i]<='9':
            all_flag=True
        else:
            all_flag=False
            break
    if all_flag==True:
        return True
    all_flag=True
    for i in range(len(str2)):
        if str2[i]>='a' and str2[i]<='z':
            all_flag=True
        elif str2[i]>='A' and str2[i]<='Z':
            all_flag=True
        else:
            all_flag=False
            break
    if all_flag==True:
        return True
    else:
        return False
   

def is_ok(lst):
    flag=True
    for i in range(len(lst)):
        if len(lst[i])>240:
            flag=False
            break
    return flag


def trim_line(src_str):
    total_len=len(src_str)
    i=0
    for i in range(total_len):
        if src_str[i]==' ' or src_str[i]=='\t':
            break

    res_str=""
    if i<total_len:
        res_str=src_str[i:total_len]
    return res_str

def treate_file(input_path,out_path,remove_path):
    #file_lst=get_files(input_dir)

	
    #cat_dict=get_catalogs(file_lst,cat_dir)
    #print "catalog size:%d\n"%(len(cat_dict))
    label_dict=dict()
    label_dict["hotel"]="LOC.HOTEL"
    label_dict["restaurant"]="LOC.CATER"
    label_dict["scenic_spot"]="LOC.SCENE"
    out_fp=open(out_path,"w")
	#file_dict[names[0]]=fp
    fp=open(input_path,"r")
    remove_fp=open(remove_path,"w")

    total_len=0
    total_num=0
    total_line=0
    #n=re.compile("")

    
    #str2="(；|？|。|！|;|!)"

    str2="(。)"
    n=re.compile(str2)
    
    while 1:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue

        #if line[0]=='@':
        #    new_line=trim_line(line)
        #    line=new_line
        #if line.startswith("消息对象:"):
        #    new_line=line[len("消息对象:"):len(line)]
        #    line=new_line
        line=line.strip()
        if line=="":
            continue


        #items=re.split(';；?？。\n\r',line)

        #items=re.split(';|；|?|？|。|\n|\r',line)
        items=n.split(line)
        #print items
        #print len(items)

        #if is_ok(items)==False:
        #    remove_fp.write("%s\n"%(line))
        #    continue
        for i in range(len(items)):
            items[i]=items[i].strip()
            if items[i]=="":
                continue
            if items[i] in str2:
                continue

            out_str=items[i]
            if (i+1) < len(items) and items[i+1] in str2:
                out_str=out_str+items[i+1]

            out_fp.write("%s\n"%(out_str))
            total_len=total_len+len(items[i])
            total_num=total_num+1
        total_line=total_line+1
        #out_fp.write("%s\t%s\t%s\n"%(items[3],entity_type,back_str))

    fp.close()
    out_fp.close()
    remove_fp.close()

    val=float(total_len)/total_num
    val2=float(total_num)/total_line

    print("total_num:%d total_len:%d average:%f\n"%(total_num,total_len,val))
    print("total_num:%d,total_line:%d average word number:%f"%(total_num,total_line,val2))


    print "success"
        


if __name__=="__main__":
    treate_file(sys.argv[1],sys.argv[2],sys.argv[3])



