#coding: utf8
import json
import sys
import requests

cnt = 0
ner2_ner1_map_ = {}

ner2_ner1_map_["ADDR"] = "LOC";
ner2_ner1_map_["CATER"] = "LOC";
ner2_ner1_map_["HOTEL"] = "LOC";
ner2_ner1_map_["SCENE"] = "LOC";
ner2_ner1_map_["ADMIN"] = "LOC";
ner2_ner1_map_["LOC_TAG"] = "LOC";
ner2_ner1_map_["STATION"] = "LOC";
ner2_ner1_map_["CATER"] = "LOC";
ner2_ner1_map_["FILM"] = "ENT";
ner2_ner1_map_["TV"] = "ENT";
ner2_ner1_map_["MUSIC"] = "ENT";
ner2_ner1_map_["COMIC"] = "ENT";
ner2_ner1_map_["ENT_OTHER"] = "ENT";
ner2_ner1_map_["SCHOOL"] = "ORG";
ner2_ner1_map_["HOSPITAL"] = "ORG";
ner2_ner1_map_["GOV"] = "ORG";
ner2_ner1_map_["EXPRESS_VENDOR"] = "ORG";
ner2_ner1_map_["PROD_NAME"] = "PROD";
ner2_ner1_map_["PROD_BRAND"] = "PROD";
ner2_ner1_map_["PROD_TAG"] = "PROD";
ner2_ner1_map_["PROD_OTHER"] = "PROD";
ner2_ner1_map_["APP_NAME"] = "APP";
ner2_ner1_map_["APP_SERVICE"] = "APP";
ner2_ner1_map_["GAME"] = "APP";
ner2_ner1_map_["DATE"] = "TIME";
ner2_ner1_map_["DAY"] = "TIME";
ner2_ner1_map_["CLOCK"] = "TIME";
ner2_ner1_map_["TIME_OTHER"] = "TIME";
ner2_ner1_map_["PHONE_NUM"] = "NUM";
ner2_ner1_map_["FLIGHT_NUM"] = "NUM";
ner2_ner1_map_["TRAIN_NUM"] = "NUM";
ner2_ner1_map_["BUS_NUM"] = "NUM";
ner2_ner1_map_["PERSON_NAME"] = "PERSON";
ner2_ner1_map_["URL"] = "NUM";
ner2_ner1_map_["EMAIL"] = "NUM";
ner2_ner1_map_["EXPRESS_CODE"]="NUM";

ner2_ner1_map_["BOOK"]="LIT";
ner2_ner1_map_["TAOBAO_PROD_ID"]="NUM";
ner2_ner1_map_["STOCK_CODE"]="STOCK";
ner2_ner1_map_["STOCK_NAME"]="STOCK";


for line in sys.stdin:
    line = line.decode('utf8')[0:100].encode('utf8')
    cnt += 1
    if cnt % 100 == 0:
        sys.stderr.write('cnt:{}\n'.format(cnt))

    line = line.rstrip('\n')
    line = line.replace('\t', ' ')
    d = {'userId':'trio',
         'query':line,
         'longitude':'116.43217',
         'latitude':'39.99409'}
    s_json = json.dumps(d, ensure_ascii=False)
    res = requests.post('http://10.0.2.207:8099/nlp/segmentation', data=s_json)

    if res.status_code != 200:
        sys.stderr.write(res.reason + '\t' + line + '\n')
        continue

    res_json = res.text
    d_res = json.loads(res_json)
    if d_res.has_key('result_list') and len(d_res['result_list']) > 0 and d_res['result_list'][0].has_key('term_list'):
        ner_list = d_res['result_list'][0]['term_list']
        out_l = []
        tmp = line
        result = ""
        for ner_term in ner_list:
            if ner_term['ner'] == 'O':
                continue
            old = ner_term['token'].encode('utf8')
            ner = ner_term['ner'].encode('utf8')
            if ner2_ner1_map_.has_key(ner):
                ner = ner2_ner1_map_[ner]+'.'+ner
            ner = '[NOR]{}{}'.format(old, '['+ner+']')
            pos = tmp.find(old)
            if pos < 0:
                continue
            result = result + tmp[0:pos]+ner
            tmp = tmp[pos+len(old):] 
        print result+tmp
    else:
        sys.stderr.write('parse result_list failed' + '\t' + line + '\n')
