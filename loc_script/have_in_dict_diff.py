#!/usr/bin/env python
# coding=utf-8 
'''
Created on 2014/10/09

@author: fanyange
'''
import json
import sys
import os

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
        if len(terms) !=2:
            continue

        #print "$%s$"%(terms[0])
        num_dict[terms[0]]=terms[1]
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
   



def treate_file(dict_path,input_path,out_path,not_path):
    #file_lst=get_files(input_dir)
	
    #cat_dict=get_catalogs(file_lst,cat_dir)
    #print "catalog size:%d\n"%(len(cat_dict))
    have_dict=load_dict(dict_path)
    print "size:%d\n"%(len(have_dict))
    label_dict=dict()
    label_dict["hotel"]="LOC.HOTEL"
    label_dict["restaurant"]="LOC.CATER"
    label_dict["scenic_spot"]="LOC.SCENE"
    out_fp=open(out_path,"w")
	#file_dict[names[0]]=fp
    fp=open(input_path,"r")
    not_fp=open(not_path,"w")
    #remove_fp=open(remove_path,"w")
    
    same_total=0
    diff_total=0
    not_total=0
    while 1:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue

        terms=line.split("\t")
        if len(terms)!=2:
            print line
            continue
        if have_dict.has_key(terms[0]):
            #print "contain:%s\n"%(line)
            if have_dict[terms[0]]==terms[1]:
                same_total=same_total+1
                continue
            else:
                out_fp.write("%s\t%s\n"%(line,have_dict[terms[0]]))
                diff_total=diff_total+1
                continue
        not_fp.write("%s\n"%(line))
        not_total=not_total+1
        #out_fp.write("%s\t%s\t%s\n"%(items[3],entity_type,back_str))

    fp.close()
    out_fp.close()
    not_fp.close()
    print "same number:%d,diff number:%d,not in number:%d"%(same_total,diff_total,not_total)
    #remove_fp.close()


    print "success"
        


if __name__=="__main__":
    treate_file(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])



