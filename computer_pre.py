# -*-coding=utf-8 -*-
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


def load_dict(standard_path):
    fp=open(standard_path,"r")

    num_dict=dict()
    line_dict=dict()
    contain_items_dict=dict()
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
        # new_str3=re.sub("\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM)\.([A-Z]|\.|_)*\]","",new_str)
        new_str3 = re.sub("\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM)+\.+\w+\]+", "", new_str)

        line_dict[new_str3]=line
        #items=re.search(r'\[(LOC|ORG|PROD|ENT|APP|PERSON|NNUM)\.([A-Z]|\.|_)*\]',line)

        # print new_str3
        # print line
        contain_items=[]
        items1 = re.findall("((\[NOR\]+)[^\[]+(\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM){1}\.{1}\w+\]+))", line)
        for j in items1:
            contain_items.append(j[0])
        # print contain_items
        # print contain_items
        # print type(contain_items)
        contain_items_dict[new_str3]=contain_items

        items=re.findall("(\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM){1}\.{1}\w+\]+)",line)
        allitems=[]
        for i in items:
            allitems.append(i[0])
            if groundTrue_all_category_dict.has_key(i[0]):
                groundTrue_all_category_dict[i[0]]+=1
            else:
                groundTrue_all_category_dict[i[0]]=1
        # print allitems,groundTrue_all_category_dict
    fp.close()
    # print all_category_dict
    return contain_items_dict,groundTrue_all_category_dict
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
   



def treate_file(standard_path,tag_path):
    #file_lst=get_files(input_dir)
	
    #cat_dict=get_catalogs(file_lst,cat_dir)
    #print "catalog size:%d\n"%(len(cat_dict))
    # label_dict=dict()
    # label_dict["hotel"]="LOC.HOTEL"
    # label_dict["restaurant"]="LOC.CATER"
    # label_dict["scenic_spot"]="LOC.SCENE"
    #out_fp=open(out_path,"w")
	#file_dict[names[0]]=fp
    true_contain_items_dict,groundTrue_all_category_dict=load_dict(standard_path)
    # sys.exit()
    fp=open(tag_path,"r")
    #remove_fp=open(remove_path,"w")
    #p=re.compile(r'\[NOR\](其他|比如|第[^\]]*家|[^\]]*菜|日租公寓|有吃有喝|别具一格|古朴|乡土人情|流连忘返|山水和|保税区|市区|一家餐厅|客满|乡土气息|[^\]]*肉|咖啡机|[^\]]*汤|[^\]]*洞天|贝壳沙滩|外滩|天天吃[^\]]*|菜大妈|栈道|山峰|瀑布|草原|峡谷|沙滩|车站|游船|和餐厅|黑猪肉|江南|旅途中|看日落|.公里|留下|山脚下|汉堡包|各种小吃|小店|小村庄|清新|花花草草|吃吃看|砂锅酸辣粉|炒冰|办理会员卡|内城|蔬菜沙拉|風景|[^\]]*和果子|布景|花草茶|寻味|速食|韩国食品|一条鱼|转角处|城内|印迹|吃饭的地方|小丑鱼|啤酒鸭|水煮鸡|好多鱼|花园里|有点特色|美团外卖|椰林|风景线|城中|小海鲜|好有味|不亦乐乎|约坐|湖光山色|[^\]]*骨面|泼水节|突突车|好吃点|大马路|那家面包店|观光巴士|一碗米线|[^\]]*西米露|你的奶茶|还好吃|[^\]]*小鱿鱼|[^\]]*牛肉面|油泼面|有一家餐厅|草莓蛋糕|[^\]]*啤酒|[^\]]*茶|中式料理|吃吃吃|悠闲时光|[^\]]*饭|[^\]]*吃|[^\]]*美味|一番滋味|鸽子汤|曲径通幽|白云[^\]]*|[^\]]*风情|预订[^\]]*|想吃[^\]]*|江景|24小时营业|[^\]]*营业|[^\]]*后面|小鱼小虾|氧吧|情愫|卤味|友好|大瀑布|南部|温泉|金灿|源动力|地方特色|合作|凤凰|日全食|走走停停|摩托艇|小家碧玉|乐呵呵|宏伟|[^\]]*肠|美食天堂|雾凇|一群羊|出水口|腐乳|云霄|小山丘|行政中心|恋恋不舍|清风徐来|入川|[^\]]*车站|烟花三月|在岛上|人间仙境|咖啡因|[^\]]*冰糕|[^\]]*外卖|[^\]]*出炉|海鲜烧烤|游客中心|经典菜|之窗|头盘|街景|沿河|五彩斑斓|锅贴|旅行的意义|吃饭时间|吃个东西|混沌面|馄饨面|乡村小镇|[^\]]*俯瞰|[^\]]山[^\]]水|[^\]]*饼|路过[^\]]*|来来往往|在[^\]]*|品茗|一人一碗|豌杂面|一家[^\]]*|饱饱|[^\]]*来了|[^\]]*看|园里|滑翔伞|携程网|馄饨|我的蛋糕|天水一色|歌舞表演|[^\]]*山色|年初.|佳肴|牛扒|饱口福|百转千回|骨汤|饭吧|辣不辣|没够|舌尖上的中国|资源|到东北|米糕|观景平台|吃喝玩乐|沙茶面|青稞|丰美|古城|真好吃|泡椒凤爪|火车站|地铁站口|一番风味|浮潜)\[(LOC|ORG)\.(CATER|SCENE|HOTEL|ADMIN|TAG|ADDR|SCHOOL)(\.SCENE|\.CATER|\.HOTEL)?\]')
    
    # p=re.compile(r'\[LOC.\w+\]\[NOR\]')
    # total=0


    all_accuracy=0
    linenum=0
    wrongLine=0

    while 1:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if line == "":
            continue
        linenum+=1
        #new_str=re.sub("\[LOC.\w+.{0,1}\w+\]","",line)
        #new_str2=re.sub("\[NOR\]","",new_str)
        #new_str3=re.sub("\[ORG.\w+.{0,1}\w+\]","",new_str2)
        new_str=re.sub("\[NOR\]","",line)
        new_str3=re.sub("\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM)\.([A-Z]|\.|_)*\]","",new_str);

        tag_contain_items = []
        items1 = re.findall("((\[NOR\]+)[^\[]+(\[(LOC|ORG|PROD|ENT|APP|PERSON|NUM){1}\.{1}\w+\]+))", line)
        for j in items1:
            tag_contain_items.append(j[0])
        # print tag_contain_items
        # print true_contain_items_dict
        if not true_contain_items_dict.has_key(new_str3):
            print ("该源句子不在目标文件中  %s" %(line))
            continue

        true_contain_items=true_contain_items_dict[new_str3]
        # print ("----------")
        # print true_contain_items

        max_count=max(len(tag_contain_items),len(true_contain_items))
        if max_count==0:
            all_accuracy+=1
            continue
        right_count=0
        for i in tag_contain_items:
            if i in true_contain_items:
                right_count+=1
        oneline_accuracy=(float(right_count)/float(max_count))*100
        all_accuracy+=oneline_accuracy
        # print ("oneline_accuracy %0.3f%%" %(oneline_accuracy))
        if (right_count!=max_count):
            wrongLine+=1
            # print line


        
        #new_str3=re.sub("\[ORG.\w+.\w+\]","",new_str2)

        #new_str=re.sub("\[LOC.\w+.*\w*\]\[NOR\]|\[LOC.\w+\]\[NOR\]","",line)
        #print line
        #print new_str
        #    continue
        #out_fp.write("** %s\n"%(line))
        # out_fp.write("%s\n"%(new_str3))

        #lst=p.findall(line)
        #if len(lst)==0:
        #    continue
        #print lst
        #for i in range(len(lst)):
        #    out_fp.write("%s\t%s\n"%(lst[i][0],lst[i][2]))

        #out_fp.write("%s\t%s\t%s\n"%(items[3],entity_type,back_str))
    print ("总数据条数: %d"% linenum)
    print ("错误的数据条数: %d"% wrongLine)
    print ("正确条数／总数据条数的准确度：%0.3f%%"%(float(linenum-wrongLine)/float(linenum)*100))
    all_accuracy=all_accuracy/float(linenum)
    print ("all_accuracy= %0.3f%% "%(all_accuracy))
    print("\n")
    print ("******************")
    print ("groundTrue_all_category_dict:\n")
    print (groundTrue_all_category_dict)

    fp.close()
    # out_fp.close()
    # print "total merge:%d"%(total)


    print "success"
        


if __name__=="__main__":
    groundTruePath="./groundTrue.txt"
    othersTagPath="./othersTag.txt"
    # treate_file(sys.argv[1],sys.argv[2])
    treate_file(groundTruePath,othersTagPath)



