from elasticsearch import Elasticsearch
import sys
import json
reload(sys)
sys.setdefaultencoding('utf8')
es = Elasticsearch("http://10.0.0.11:8405/")
# es1 = Elasticsearch("http://10.0.2.16:28405")      
# res = es1.search(index="video_douban_20180416",doc_type=data_type,body={"from": i * size,"size": size})
def extract_detail(size, data_type, total):
	result = []
	for i in range(total/size + 1):
		res = es.search(index="worldcup",doc_type=data_type,body={"from": i * size,"size": size})
		for infos in res['hits']['hits']:
			info = infos['_source']
			uid = infos['_source']['details']['id']
			name = info['details']['chineseFullName']
			print("id is: ",uid)
			print(name+"\n")
			print("-----------------")
			print(info)
			print("-----------------")
			
# tv1 = extract_detail(5000, 'tv', 24139)
movie1 = extract_detail(100, 'football_player', 1000)
# variety1 = extract_detail(5000, 'variety', 9890)
# comic1 = extract_detail(5000, 'comic', 12453)
# unknown1 = extract_detail(5000, 'unknown', 121)
