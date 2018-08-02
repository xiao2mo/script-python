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
   



def treate_file(input_path,out_path,out_path2):
    #file_lst=get_files(input_dir)
	
    #cat_dict=get_catalogs(file_lst,cat_dir)
    #print "catalog size:%d\n"%(len(cat_dict))
    label_dict=dict()
    label_dict["hotel"]="LOC.HOTEL"
    label_dict["restaurant"]="LOC.CATER"
    label_dict["scenic_spot"]="LOC.SCENE"
    out_fp=open(out_path,"w")
    out_fp2=open(out_path2,"w")
	#file_dict[names[0]]=fp
    fp=open(input_path,"r")
    #remove_fp=open(remove_path,"w")
    #p=re.compile(r'\[NOR\](其他|比如|第[^\]]*家|[^\]]*菜|日租公寓|有吃有喝|别具一格|古朴|乡土人情|流连忘返|山水和|保税区|市区|一家餐厅|客满|乡土气息|[^\]]*肉|咖啡机|[^\]]*汤|[^\]]*洞天|贝壳沙滩|外滩|天天吃[^\]]*|菜大妈|栈道|山峰|瀑布|草原|峡谷|沙滩|车站|游船|和餐厅|黑猪肉|江南|旅途中|看日落|.公里|留下|山脚下|汉堡包|各种小吃|小店|小村庄|清新|花花草草|吃吃看|砂锅酸辣粉|炒冰|办理会员卡|内城|蔬菜沙拉|風景|[^\]]*和果子|布景|花草茶|寻味|速食|韩国食品|一条鱼|转角处|城内|印迹|吃饭的地方|小丑鱼|啤酒鸭|水煮鸡|好多鱼|花园里|有点特色|美团外卖|椰林|风景线|城中|小海鲜|好有味|不亦乐乎|约坐|湖光山色|[^\]]*骨面|泼水节|突突车|好吃点|大马路|那家面包店|观光巴士|一碗米线|[^\]]*西米露|你的奶茶|还好吃|[^\]]*小鱿鱼|[^\]]*牛肉面|油泼面|有一家餐厅|草莓蛋糕|[^\]]*啤酒|[^\]]*茶|中式料理|吃吃吃|悠闲时光|[^\]]*饭|[^\]]*吃|[^\]]*美味|一番滋味|鸽子汤|曲径通幽|白云[^\]]*|[^\]]*风情|预订[^\]]*|想吃[^\]]*|江景|24小时营业|[^\]]*营业|[^\]]*后面|小鱼小虾|氧吧|情愫|卤味|友好|大瀑布|南部|温泉|金灿|源动力|地方特色|合作|凤凰|日全食|走走停停|摩托艇|小家碧玉|乐呵呵|宏伟|[^\]]*肠|美食天堂|雾凇|一群羊|出水口|腐乳|云霄|小山丘|行政中心|恋恋不舍|清风徐来|入川|[^\]]*车站|烟花三月|在岛上|人间仙境|咖啡因|[^\]]*冰糕|[^\]]*外卖|[^\]]*出炉|海鲜烧烤|游客中心|经典菜|之窗|头盘|街景|沿河|五彩斑斓|锅贴|旅行的意义|吃饭时间|吃个东西|混沌面|馄饨面|乡村小镇|[^\]]*俯瞰|[^\]]山[^\]]水|[^\]]*饼|路过[^\]]*|来来往往|在[^\]]*|品茗|一人一碗|豌杂面|一家[^\]]*|饱饱|[^\]]*来了|[^\]]*看|园里|滑翔伞|携程网|馄饨|我的蛋糕|天水一色|歌舞表演|[^\]]*山色|年初.|佳肴|牛扒|饱口福|百转千回|骨汤|饭吧|辣不辣|没够|舌尖上的中国|资源|到东北|米糕|观景平台|吃喝玩乐|沙茶面|青稞|丰美|古城|真好吃|泡椒凤爪|火车站|地铁站口|一番风味|浮潜)\[(LOC|ORG)\.(CATER|SCENE|HOTEL|ADMIN|TAG|ADDR|SCHOOL)(\.SCENE|\.CATER|\.HOTEL)?\]')
    
    p=re.compile(r'\[NOR\](.+)\[LOC.\w+.{0,1}\w+\]')
    total=0
    all_dict=dict()
    
    while 1:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue

        #new_str=re.sub("\[LOC.\w+.{0,1}\w+\]","",line)
        #new_str2=re.sub("\[NOR\]","",new_str)
        #lst=re.findall(r'\[NOR\](.*)\[LOC.\w+.{0,1}\w+\]',line,re.M)
       
        #print line
        lst=line.split("[NOR]")
        if len(lst)>0:
            for i in range(len(lst)):
                 
                items=lst[i].split("[LOC")
                if len(items)==2:
                    #print items[0]
                    if items[1].find("]")>0:
                        back=items[1][0:items[1].find("]")]
                        #print "LOC%s"%(back)
                        back="LOC"+back 
                        if all_dict.has_key(items[0]):
                            if all_dict[items[0]].has_key(back):
                                all_dict[items[0]][back]=all_dict[items[0]][back]+1
                            else:
                                all_dict[items[0]][back]=1
                        else:
                            next_dict=dict()
                            next_dict[back]=1
                            all_dict[items[0]]=next_dict

        else:
            continue
        #print lst
        
        total=0


        #new_str=re.sub("\[LOC.\w+.*\w*\]\[NOR\]|\[LOC.\w+\]\[NOR\]","",line)
        #print line
        #print new_str
        #    continue
        #out_fp.write("** %s\n"%(line))
        #out_fp.write("%s\n"%(new_str2))

        #lst=p.findall(line)
        #if len(lst)==0:
        #    continue
        #print lst
        #for i in range(len(lst)):
        #    out_fp.write("%s\t%s\n"%(lst[i][0],lst[i][2]))

        #out_fp.write("%s\t%s\t%s\n"%(items[3],entity_type,back_str))

    fp.close()

    for k,v in all_dict.items():
        if len(v)==1:
            for k2,v2 in v.items():
                #out_fp.write("%s\t%s\t%d\n"%(k,k2,v2))
                out_fp.write("%s\t%s\n"%(k,k2))
        else:
            max_k=""
            max_v=0
            #for k2,v2 in v.items():
            #    out_fp2.write("%s\t%s\t%d\n"%(k,k2,v2))
            #    if v2>max_v:
            #        max_v=v2
            #        max_k=k2
            #print v
            lst=sorted(v.iteritems(), key=lambda d: d[1],reverse=True) 
            #print lst
            #print v
            res=lst[0][0]
            for i in range(1,len(lst)):
                res=res+"\t"+lst[i][0]
            out_fp2.write("%s\t%s\n"%(k,res))
           
    out_fp.close()
    out_fp2.close()
    print "total merge:%d"%(total)


    print "success"
        


if __name__=="__main__":
    treate_file(sys.argv[1],sys.argv[2],sys.argv[3])


