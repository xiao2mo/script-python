from elasticsearch import Elasticsearch
import sys
import json
import argparse
reload(sys)
sys.setdefaultencoding('utf8')

parser=argparse.ArgumentParser()
parser.add_argument("-time","--filtertime",default="all",type=str)
args=parser.parse_args()


es = Elasticsearch("http://10.0.0.11:8405")
# es1 = Elasticsearch("http://10.0.2.16:28405")
# res = es1.search(index="video_douban_20180416",doc_type=data_type,body={"from": i * size,"size": size})
def extract_detail(size, data_type, total):
	result = []
	for i in range(total/size + 1):
		res = es.search(index="video_douban",doc_type=data_type,body={"from": i * size,"size": size})
		if res==None:
			return
		for infos in res['hits']['hits']:
			out_str=""
			info = infos['_source']
			uid = infos['_source']['details']['uid']
			releaseTime = info['details']['releaseTime']
			douban_id = info['details']['DoubanId']
			name = info['details']['name']
			out_str='{}\t{}\t{}'.format(douban_id.strip(),name.strip(),releaseTime.strip())
			if args.filtertime=="all":
				print out_str
			elif releaseTime>=args.filtertime:
#				print name.strip(), douban_id.strip(), releaseTime.strip(print out_str
				print out_str
				#print name.strip()
			else:
				continue
	# print info['details']['DoubanId'],"\t", data_type

# tv1 = extract_detail(5000, 'tv', 24139)
movie1 = extract_detail(5000, 'movie', 100000)
# variety1 = extract_detail(5000, 'variety', 9890)
# comic1 = extract_detail(5000, 'comic', 12453)
# unknown1 = extract_detail(5000, 'unknown', 121)
